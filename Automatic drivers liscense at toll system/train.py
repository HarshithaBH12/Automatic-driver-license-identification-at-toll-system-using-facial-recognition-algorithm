import os
import cv2
import csv
import numpy as np
from PIL import Image
import pickle

# ---------------- Text-to-Speech Dummy ----------------
def text_to_speech(msg):
    print("TTS:", msg)

# ---------------- User Input ----------------
name = input("Enter Name: ")
license_no = input("Enter License Number: ")
dob = input("Enter Date of Birth / Date: ")
valid = input("Valid (Yes/No): ")
number_plate = input("Vehicle Number Plate: ")

if name == "" or license_no == "" or dob == "" or valid == "" or number_plate == "":
    print("Please fill all fields!")
    text_to_speech("Please fill all fields!")
    exit()

# ---------------- Paths ----------------
directory = f"{license_no}_{name}"
image_path = os.path.join("TrainingImage", directory)
os.makedirs(image_path, exist_ok=True)
os.makedirs("LicenseDetails", exist_ok=True)
csv_path = "LicenseDetails/license_details.csv"
os.makedirs("TrainingImageLabel", exist_ok=True)

# Save user info in CSV
with open(csv_path, "a+", newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow([name, license_no, dob, valid, number_plate])
text_to_speech(f"User info saved: {name}, {license_no}, {dob}, {valid}, {number_plate}")

# ---------------- Camera Setup ----------------
cap = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
sample_num = 0

print("\nCamera running... Press 'c' to capture, 'q' to quit.")

# ---------------- Main Loop ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    # Draw rectangles and overlay user info
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, f"Name: {name}", (x, y-80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.putText(frame, f"License No: {license_no}", (x, y-60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.putText(frame, f"DOB: {dob}", (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.putText(frame, f"Valid: {valid}", (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.putText(frame, f"Number Plate: {number_plate}", (x, y-0), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.putText(frame, f"Images Captured: {sample_num}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    cv2.imshow("Driving License Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c') and len(faces) > 0:  # Manual capture
        for (x, y, w, h) in faces:
            sample_num += 1
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(image_path, f"{name}_{license_no}_{sample_num}.jpg"), face_img)
        text_to_speech(f"Captured Image {sample_num}")
        print(f"Captured Image {sample_num}")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
text_to_speech("Camera closed.")
print(f"Total images captured: {sample_num}")

# ---------------- Train Model ----------------
train_choice = input("Shall we train the model now? (yes/no): ").lower()
if train_choice == "yes":
    print("Training started...")
    text_to_speech("Training started...")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces_list = []
    Ids = []

    # Map License No -> Numeric ID
    id_map = {}
    current_id = 0

    dirs = [os.path.join("TrainingImage", d) for d in os.listdir("TrainingImage")]
    for d in dirs:
        folder_name = os.path.basename(d)
        license_no_folder = folder_name.split("_")[0]
        if license_no_folder not in id_map:
            id_map[license_no_folder] = current_id
            current_id += 1
        numeric_id = id_map[license_no_folder]

        files = [os.path.join(d, f) for f in os.listdir(d)]
        for fpath in files:
            pilImage = Image.open(fpath).convert("L")
            imgNp = np.array(pilImage, "uint8")
            faces_list.append(imgNp)
            Ids.append(numeric_id)

    if len(faces_list) == 0:
        text_to_speech("No images found to train.")
        print("No images found to train.")
    else:
        recognizer.train(faces_list, np.array(Ids))
        recognizer.save("TrainingImageLabel/Trainner.yml")

        # Save ID mapping for prediction
        with open("TrainingImageLabel/id_map.pkl", "wb") as f:
            pickle.dump(id_map, f)

        text_to_speech("Training completed successfully!")
        print("Training completed successfully!")

else:
    text_to_speech("Training skipped.")
    print("Training skipped.")