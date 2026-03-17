import flwr as fl
import tenseal as ts
import torch
import numpy as np
import matplotlib.pyplot as plt
from flwr.common import Parameters, ndarrays_to_parameters

# ========== ✅ 1. Load CKKS Encryption Context ==========
try:
    with open("ckks_context_full.tenseal", "rb") as f:
        server_context = ts.context_from(f.read())

    print("🔐 CKKS context loaded from 'ckks_context.tenseal'")
except Exception as e:
    print(f" Failed to load CKKS context: {type(e).__name__}: {e}")
    exit(1)

# ========== 2. Global Metrics Tracking ==========
loss_per_round = []
accuracy_per_round = []
aggregated_weights = None

# ========== 3. Aggregate Fit ==========
def aggregate_fit(rnd, results, failures):
    global aggregated_weights
    print(f"\n📡 Aggregating Round {rnd}...")

    all_client_weights = []

    for i, (_, fit_res) in enumerate(results):
        # ⚠️ Ensure correct tensor_type
        if fit_res.parameters.tensor_type != "encrypted_ckks":
            
            continue

        # ⚠️ Ensure all tensors are bytes
        if not all(isinstance(t, bytes) for t in fit_res.parameters.tensors):
            
            continue

        decrypted_layers = []
        for j, ew_bytes in enumerate(fit_res.parameters.tensors):
            try:
                vec = ts.ckks_vector_from(server_context, ew_bytes)
                decrypted_tensor = torch.tensor(vec.decrypt(), dtype=torch.float32)
                decrypted_layers.append(decrypted_tensor)

            except Exception as e:
            
                continue

        expected_layers = len(results[0][1].parameters.tensors)
        if len(decrypted_layers) != expected_layers:
        
            continue

        all_client_weights.append(decrypted_layers)

    if not all_client_weights:
        print("❌ All decryption failed or tensors invalid.")
        return None, {}

    # 🔄 Average the decrypted weights
    aggregated_weights_temp = []
    for layers in zip(*all_client_weights):
        stacked = torch.stack(layers)
        avg = torch.mean(stacked, dim=0)
        aggregated_weights_temp.append(avg)

    aggregated_weights = aggregated_weights_temp

    # 🔐 Re-encrypt the aggregated weights
    encrypted_weights = [
        ts.ckks_vector(server_context, w.tolist()).serialize()
        for w in aggregated_weights
    ]

    # ✅ Sanity check
    assert all(isinstance(w, bytes) for w in encrypted_weights), "❌ Aggregated weights must be bytes"

    return Parameters(tensors=encrypted_weights, tensor_type="encrypted_ckks"), {"round": rnd}

# ========== 4. Aggregate Evaluate ==========
def aggregate_evaluate(rnd, results, failures):
    global aggregated_weights
    print(f"\n📊 Evaluating Global Model Performance for Round {rnd}...")

    total_loss, total_acc, total_samples = 0.0, 0.0, 0

    for i, (_, eval_res) in enumerate(results):
        try:
            if eval_res.status.code == fl.common.Code.OK:
                n = eval_res.num_examples
                loss = eval_res.loss
                acc = eval_res.metrics["accuracy"]
                total_loss += loss * n
                total_acc += acc * n
                total_samples += n
                print(f"📌 Client {i+1}: Loss = {loss:.4f}, Accuracy = {acc:.4f}")
        except Exception as e:
            print(f"⚠️ Skipping faulty evaluation from client {i}: {type(e).__name__}: {e}")

    if total_samples > 0:
        avg_loss = total_loss / total_samples
        avg_acc = total_acc / total_samples
        loss_per_round.append(avg_loss)
        accuracy_per_round.append(avg_acc)
        print(f"✅ Global Performance Round {rnd} → Loss: {avg_loss:.4f}, Accuracy: {avg_acc:.4f}")

        if aggregated_weights and (len(accuracy_per_round) == 1 or avg_acc > max(accuracy_per_round[:-1])):
            torch.save(aggregated_weights, "best_model.pt")
            print(f"🏆 New best model saved with Accuracy: {avg_acc:.4f}")

        return avg_loss, {"accuracy": avg_acc}

    print("❌ No valid evaluation results.")
    return 0.0, {"accuracy": 0.0}

# ========== 5. Custom Strategy ==========
class SecureFedAvg(fl.server.strategy.FedAvg):
    def aggregate_fit(self, rnd, results, failures):
        return aggregate_fit(rnd, results, failures)

    def aggregate_evaluate(self, rnd, results, failures):
        return aggregate_evaluate(rnd, results, failures)

    def initialize_parameters(self, client_manager):
        dummy = [np.zeros(1000, dtype=np.float32)]
        return ndarrays_to_parameters(dummy)

# ========== 6. Start Server ==========
num_rounds = 100
fl.server.start_server(
    server_address="0.0.0.0:9090",
    config=fl.server.ServerConfig(num_rounds=num_rounds),
    strategy=SecureFedAvg(
        fraction_fit=1.0,
        min_fit_clients=6,
        min_available_clients=6,
        on_fit_config_fn=lambda rnd: {"lr": 0.001},
        on_evaluate_config_fn=lambda rnd: {"val": True},
    )
)

# ========== 7. Plot Metrics ==========
def trim_list(lst, length):
    return lst[:length] if len(lst) > length else lst

loss_per_round = trim_list(loss_per_round, num_rounds)
accuracy_per_round = trim_list(accuracy_per_round, num_rounds)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(range(1, len(loss_per_round) + 1), loss_per_round, marker='o', color='red')
plt.title("Global Loss per Round")
plt.xlabel("Round")
plt.ylabel("Loss")

plt.subplot(1, 2, 2)
plt.plot(range(1, len(accuracy_per_round) + 1), accuracy_per_round, marker='o', color='blue')
plt.title("Global Accuracy per Round")
plt.xlabel("Round")
plt.ylabel("Accuracy")

plt.tight_layout()
plt.show()