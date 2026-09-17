# 🚦 Automatic Driver License Identification at Toll System Using Facial Recognition

> 🤖 A smart toll gate automation system that combines facial recognition with driver's license verification for secure and automated toll gate access.

---

## 📌 Project Overview

This project proposes a smart toll gate automation system that combines **facial recognition** with **driver's license verification** to improve security and operational efficiency.

A camera captures the driver's face, and the **Raspberry Pi 3B+** processes the image using **Python, OpenCV, and the face_recognition library**.

After successful facial recognition, the system verifies the driver's license details using the available database. The verification checks important information such as the driver's identity, license status, age eligibility, and violation status.

If the driver is successfully verified, the Raspberry Pi sends a command through **UART** to the **Raspberry Pi Pico**. The Pico uses **PWM** to control a servo motor, which opens the toll gate.

If verification fails, the gate remains closed and the buzzer provides an alert.

The system is designed as a cost-effective and modular prototype that can be extended for smart highway and secure access applications.

---

## 🎯 Aim

To develop a secure and automated toll gate system that uses **facial recognition and driver's license verification** to authenticate drivers and control toll gate access.

---

## 🎯 Objectives

- 👤 Identify the driver using facial recognition.
- 🪪 Verify driver's license information.
- 🔍 Check license validity and related details.
- 🔞 Verify age eligibility.
- 🚨 Check traffic or violation status.
- 🚧 Automatically control the toll gate.
- 📡 Establish UART communication between Raspberry Pi and Raspberry Pi Pico.
- ⚙️ Control the servo motor using PWM.
- 🔊 Provide alerts using a buzzer.
- 💾 Maintain verification history.
- 📊 Provide a monitoring dashboard.
- 🚀 Provide a foundation for future smart highway applications.

---

## 🔄 Methodology

### 1️⃣ Image Capture

The **Pi Camera** captures the driver's face when the vehicle approaches the toll gate.

### 2️⃣ Image Processing

The captured image is processed using **OpenCV** to prepare the image for facial recognition.

### 3️⃣ Face Detection

The system detects the driver's face from the captured image.

### 4️⃣ Face Encoding

The detected face is converted into a numerical facial encoding using the **face_recognition** library.

### 5️⃣ Face Matching

The generated face encoding is compared with previously stored face encodings.

If a matching driver is found, the system proceeds to license verification.

### 6️⃣ License Verification

The driver's details are checked against the available license database.

The verification includes:

- 🪪 License number
- 👤 Driver name
- 📅 License validity
- 🔞 Age eligibility
- 🚨 Violation status
- 🚗 Vehicle number

### 7️⃣ Access Decision

If the facial recognition and license verification are successful, access is granted.

If verification fails, access is denied and the gate remains closed.

### 8️⃣ UART Communication

After successful verification, the Raspberry Pi sends a control command to the Raspberry Pi Pico through **UART communication**.

### 9️⃣ Servo Control

The Raspberry Pi Pico receives the command and generates a **PWM signal** to control the servo motor.

The servo moves the toll barrier to the required position.

### 🔟 Data Logging

The system stores important verification information such as:

- Driver name
- Vehicle number
- License number
- Status
- Date and time

---

## 🏗️ System Architecture

    📷 Pi Camera
          │
          ▼
    ┌────────────────────┐
    │  Raspberry Pi 3B+  │
    │                    │
    │ Python             │
    │ OpenCV             │
    │ Face Recognition   │
    │ License Verification│
    └─────────┬──────────┘
              │
             UART
              │
              ▼
    ┌────────────────────┐
    │  Raspberry Pi Pico  │
    └─────────┬──────────┘
              │
             PWM
              │
              ▼
    ┌────────────────────┐
    │    Servo Motor     │
    └─────────┬──────────┘
              │
              ▼
          🚧 Toll Gate

---

## 🔁 Complete System Flow

    🚗 Vehicle Approaches
             ↓
       📷 Face Capture
             ↓
       🔍 Face Detection
             ↓
       👤 Face Recognition
             ↓
       🪪 License Verification
             ↓
        ⚖️ Decision
          ↙     ↘
       ❌          ✅
     Failed       Valid
       ↓            ↓
    🔊 Buzzer      📡 UART
       ↓            ↓
    🚫 Gate      Raspberry Pi
     Closed          Pico
                     ↓
                    PWM
                     ↓
               ⚙️ Servo Motor
                     ↓
                🚧 Gate Opens

---

## 🛠️ Technologies Used

### 💻 Software

- 🐍 Python
- 👁️ OpenCV
- 👤 face_recognition
- 🌐 Flask
- 💾 SQLite
- 📄 CSV
- 🌐 HTML
- 🎨 CSS
- 📡 REST API
- 🔢 NumPy

### 🔌 Hardware

- 🍓 Raspberry Pi 3B+
- 🔌 Raspberry Pi Pico
- 📷 Pi Camera
- ⚙️ Servo Motor
- 🔊 Buzzer
- 📡 UART

---

## 👁️ Facial Recognition

The facial recognition module is responsible for identifying the driver.

The basic process is:

    📷 Capture Image
          ↓
    🔍 Detect Face
          ↓
    🔢 Generate Face Encoding
          ↓
    💾 Load Stored Encodings
          ↓
    ⚖️ Compare Encodings
          ↓
    ✅ Match / ❌ No Match

If a matching face is found, the system continues with driver's license verification.

---

## 💾 Pickle

The project uses **Pickle** to store and load the generated face encodings.

The process is:

    Driver Images
          ↓
    Face Detection
          ↓
    Face Encoding
          ↓
    Pickle Storage
          ↓
    Encodings File
          ↓
    Face Recognition

This allows previously generated face encodings to be loaded during recognition.

---

## 🪪 License Verification

After recognizing the driver, the system checks the driver's license information.

The system can verify:

- 👤 Driver identity
- 🪪 License number
- 📅 License validity
- 🔞 Age eligibility
- 🚨 Violation status
- 🚗 Vehicle information

The license information is obtained from the available dataset/database used by the project.

---

## 🌐 API Integration

The project dashboard uses an API to retrieve current driver-related information.

**API** stands for **Application Programming Interface**.

The API provides a communication layer between the data source and the Flask application.

The data flow is:

    External Data
          ↓
         API
          ↓
    Flask Application
          ↓
    SQLite Database
          ↓
       Dashboard

The Python **requests** library is used to communicate with the API and receive data in JSON format.

---

## 📊 Dashboard

The project includes a **Flask-based web dashboard** for monitoring the system.

### 📋 Current Data

Displays the current driver information received from the API.

### 🗂️ All Data

Displays the available records stored in the system.

### 🕒 History

Displays previously recorded verification activities.

### 📌 Status

The dashboard displays the status associated with each driver record.

- 🟢 **Activated / Active** → The record is authorized according to the available data.
- 🔴 **Deactivated** → The record is not authorized according to the available data.

---

## 🌐 Frontend

The frontend of the dashboard uses:

- HTML
- CSS
- Jinja Templates

The frontend is responsible for displaying the dashboard and driver information.

### 🎨 Frontend Responsibilities

- Display current data
- Display history
- Display driver information
- Display verification status
- Provide a simple monitoring interface

---

## ⚙️ Backend

The backend is developed using **Python and Flask**.

### Backend Responsibilities

- Receive API data
- Process driver information
- Perform database operations
- Maintain verification history
- Serve dashboard pages
- Provide JSON responses
- Connect different system components

---

## 🗃️ Database

The project uses **SQLite** for storing history records.

The history table contains:

| Field | Description |
|---|---|
| `id` | Unique record ID |
| `name` | Driver name |
| `status` | Verification status |
| `vehicle_number` | Vehicle registration number |
| `license_number` | Driving license number |
| `created_at` | Date and time of record |

The system checks whether a record already exists before storing it to reduce duplicate entries.

---

## 📡 UART Communication

**UART** stands for **Universal Asynchronous Receiver/Transmitter**.

UART is used for communication between the Raspberry Pi 3B+ and Raspberry Pi Pico.

The communication flow is:

    Raspberry Pi 3B+
           │
          UART
           │
           ▼
    Raspberry Pi Pico
           │
           ▼
      Servo Control

The Raspberry Pi sends the gate control command after successful verification.

---

## ⚙️ PWM Servo Control

**PWM** stands for **Pulse Width Modulation**.

The Raspberry Pi Pico uses PWM to control the position of the servo motor.

The servo motor is connected to the toll barrier mechanism.

    UART Command
         ↓
    Raspberry Pi Pico
         ↓
        PWM
         ↓
    Servo Motor
         ↓
      Gate Opens

---

## 🔊 Buzzer Alert

The buzzer provides an alert when verification is unsuccessful.

### ✅ Successful Verification

    Face Match
         ↓
    License Valid
         ↓
    Access Granted
         ↓
    UART Command
         ↓
    Servo Activated
         ↓
    🚧 Gate Opens

### ❌ Failed Verification

    Face/License Verification Failed
                 ↓
             🔊 Buzzer
                 ↓
          🚫 Gate Closed

---

## 🧠 Important Python Libraries

| Library | Purpose |
|---|---|
| 🐍 Flask | Web application and backend |
| 👁️ OpenCV | Image processing and computer vision |
| 👤 face_recognition | Face detection and face matching |
| 🔢 NumPy | Numerical and image data processing |
| 💾 SQLite3 | Database storage |
| 🌐 Requests | API communication |
| ⏰ datetime | Date and time handling |
| 📦 pickle | Saving and loading face encodings |
| 🔌 RPi.GPIO | Raspberry Pi GPIO control |

---

## 🖥️ RealVNC

**RealVNC** is used for remote access to the Raspberry Pi desktop.

It helps the development team:

- 🖥️ Access the Raspberry Pi remotely
- 🐍 Run Python programs
- 📷 Check the camera
- 🔍 Debug the application
- ⚙️ Monitor the system

RealVNC is a remote access tool and is not responsible for facial recognition.

---

## 🔐 Security

The system uses multiple verification steps instead of relying on a single identification method.

Security considerations include:

- 👤 Facial identification
- 🪪 License verification
- 🚨 Failed verification alerts
- 💾 Controlled database access
- 📝 Verification history

### 🔮 Future Security Improvements

Future versions can include:

- 🔐 Encryption
- 👁️ Liveness detection
- 🛡️ Anti-spoofing
- 🔑 Strong administrator authentication
- ☁️ Secure cloud storage
- 📜 Tamper-resistant logs

---

## 📈 Advantages

- ⚡ Real-time driver verification
- 👤 Facial authentication
- 🪪 Driver's license verification
- 🚫 Helps prevent unauthorized access
- 🤖 Reduces manual intervention
- 🚧 Automatic gate operation
- 📡 UART communication
- ⚙️ PWM-based servo control
- 🔊 Buzzer alerts
- 💾 History storage
- 📊 Monitoring dashboard
- 💰 Cost-effective prototype
- 📦 Modular architecture
- 🌐 Suitable for smart highway applications

---

## ⚠️ Limitations

The current prototype has some limitations:

- 💡 Recognition can be affected by lighting conditions.
- 📷 Camera angle and image quality can affect recognition.
- 🗃️ License verification depends on the available dataset/database.
- 🌐 Direct government database verification is not implemented in the current prototype.
- 🛡️ Advanced liveness detection is not currently implemented.
- 🚗 Large-scale multi-lane deployment requires additional infrastructure.

---

## 🚀 Future Scope

### 🚘 ANPR

Implement **Automatic Number Plate Recognition** to identify and verify the vehicle number plate.

Future verification can combine:

    👤 Driver Face
          +
    🪪 License
          +
    🚘 Number Plate
          ↓
    Multi-Level Verification

### 👁️ Liveness Detection

Add liveness detection to determine whether the captured face belongs to a real person rather than a photograph or video.

### ☁️ Cloud Integration

Connect multiple toll booths to a centralized cloud platform for:

- Centralized monitoring
- Data synchronization
- Traffic analytics
- Remote management

### 💳 Digital Payments

Integrate authorized digital payment systems such as UPI for automated toll payments.

### 🚦 Multi-Lane Support

Support multiple independent toll lanes so that a problem in one lane does not block the complete traffic flow.

### 🔄 Automatic Lane Diversion

Use sensors to detect congestion and redirect vehicles to another available lane.

### 🤖 Anomaly Detection

Use machine learning to identify unusual verification patterns and suspicious activities.

### 📊 Advanced Analytics

Generate analytics for:

- Traffic volume
- Verification failures
- Peak traffic hours
- Authorized entries
- Repeated failed attempts

---

## 🧪 Testing

The system can be evaluated using:

- 🎯 Face recognition accuracy
- ⏱️ Verification response time
- ❌ False acceptance cases
- 🚫 False rejection cases
- 🪪 License verification accuracy
- 🚧 Gate response
- 📡 UART communication reliability
- ⚙️ Servo response
- 🔊 Buzzer response
- 💾 Database logging

---

## 📁 Project Structure

    Automatic-Driver-License-Identification/
    │
    ├── 📂 dataset/
    │   └── driver_images/
    │
    ├── 📂 templates/
    │   └── index.html
    │
    ├── 📂 static/
    │   ├── css/
    │   └── js/
    │
    ├── 🐍 train.py
    ├── 🐍 face_recognition.py
    ├── 🐍 app.py
    ├── 🗃️ data_store.db
    ├── 📄 license_data.csv
    ├── 📦 encodings.pickle
    ├── 📄 requirements.txt
    └── 📖 README.md

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

    git clone <your-github-repository-url>

    cd Automatic-Driver-License-Identification

### 2️⃣ Create a Virtual Environment

    python -m venv venv

### 3️⃣ Activate the Environment

#### Windows

    venv\Scripts\activate

#### Linux / Raspberry Pi

    source venv/bin/activate

### 4️⃣ Install Dependencies

    pip install -r requirements.txt

---

## ▶️ Running the Project

Run the Flask application:

    python app.py

After starting the application, open the local Flask address displayed in the terminal.

---

## 🔄 Complete Working

The complete working of the project can be summarized as:

    🚗 Vehicle Approaches
             ↓
        📷 Camera Captures
             ↓
        👤 Face Detection
             ↓
       🔍 Face Recognition
             ↓
      🪪 License Verification
             ↓
        ⚖️ Access Decision
             ↓
       ┌─────┴─────┐
       ↓           ↓
      ❌           ✅
    Failed        Valid
       ↓           ↓
    🔊 Alert     📡 UART
       ↓           ↓
    🚫 Closed   Raspberry Pi Pico
                    ↓
                   PWM
                    ↓
               ⚙️ Servo Motor
                    ↓
                🚧 Gate Opens
                    ↓
                💾 History
                    ↓
                📊 Dashboard

---

## 📝 Research Work

The project was developed along with research and technical documentation activities including:

- 📚 Literature survey
- 📄 Technical paper preparation
- 🧪 Experimental testing
- 📊 Result analysis
- 📈 Comparison tables and graphs
- 📝 Patent documentation
- 🎤 Project presentations
- 🖥️ Prototype demonstration

---

## 📌 Conclusion

The project demonstrates a prototype for automated driver verification and toll gate control by combining **facial recognition, driver's license verification, Raspberry Pi processing, UART communication, Raspberry Pi Pico, PWM-based servo control, database logging, and a monitoring dashboard**.

The system provides an automated approach to driver authentication and toll gate access while reducing manual intervention.

The modular design provides a foundation for future enhancements such as **ANPR, liveness detection, cloud monitoring, digital payments, multi-lane processing, and intelligent traffic analytics**.

---

## ⭐ Core System Flow

    📷 CAPTURE
         ↓
    👤 RECOGNIZE
         ↓
    🪪 VERIFY LICENSE
         ↓
    ⚖️ MAKE DECISION
         ↓
    📡 UART COMMUNICATION
         ↓
    ⚙️ PWM CONTROL
         ↓
    🚧 OPEN / CLOSE GATE
         ↓
    💾 STORE HISTORY
         ↓
    📊 DASHBOARD

---

## ❤️ Built With

🐍 Python  
👁️ OpenCV  
👤 Face Recognition  
🌐 Flask  
💾 SQLite  
🍓 Raspberry Pi 3B+  
🔌 Raspberry Pi Pico  
📷 Pi Camera  
📡 UART  
⚙️ PWM  
🤖 IoT  
🚦 Computer Vision

---

## 👩‍💻 Author

### Harshitha B H

🎓 Information Science and Engineering

🏫 Cambridge Institute of Technology, Bangalore

---

## ⭐ Project

### Automatic Driver License Identification at Toll System Using Facial Recognition

> 🚦 Smart Verification • Secure Access • Automated Toll Management

⭐ If you find this project useful, consider giving the repository a star!
