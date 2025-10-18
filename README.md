# 🛰️ ESP32-Sonar-Radar-System

![Platform](https://img.shields.io/badge/Platform-ESP32-blue)
![Language](https://img.shields.io/badge/Language-Python%20%7C%20Arduino-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

> **Detect. Measure. Visualize.**  
> A real-time sonar radar system using ESP32 and an ultrasonic sensor to detect and visualize object distances on a dynamic Python interface.

---

## 🚀 Overview
The **ESP32 Sonar Radar System** scans the environment using an ultrasonic sensor and visualizes detected objects on a live radar interface using Python.  
It combines IoT hardware control with dynamic data visualization to simulate real radar-like motion tracking.

---

## ⚙️ Features
- Real-time object detection using ultrasonic sensor  
- Radar-style visualization with smooth sweeping motion  
- Serial communication between ESP32 and Python  
- Adjustable scan speed and angle  
- Modern, interactive radar interface  

---

## 🧩 Hardware Requirements
| Component | Description |
|------------|--------------|
| ESP32 | Main microcontroller |
| HC-SR04 | Ultrasonic distance sensor |
| Servo Motor (SG90) | For radar rotation |
| Jumper Wires | Connections |
| USB Cable | Power & serial communication |

---

## 🖥️ Software Requirements
- Arduino IDE (for ESP32 code)
- Python 3.x  
- Libraries: `pyserial`, `pygame`

---

## 🧠 Circuit Diagram
![Circuit Diagram](assets/circuit-diagram.png)

---

## 🌀 Radar Visualization Preview
![Radar Demo](assets/preview.gif)

---

## 🧩 Project Structure
```
ESP32-Sonar-Radar-System/
│
├── ESP32/
│   └── esp32_sonar_radar.ino
│
├── Python/
│   └── radar_visualizer.py
│
├── assets/
│   ├── preview.gif
│   └── circuit-diagram.png
│
├── LICENSE
├── README.md
└── .gitignore
```

---

## ⚡ Getting Started

### 1️⃣ Upload the ESP32 Code
Open `esp32_sonar_radar.ino` in Arduino IDE → Select **ESP32 Dev Module** → Upload.

### 2️⃣ Run the Python Visualization
```bash
python radar_visualizer.py
```

### 3️⃣ Enjoy Real-Time Scanning
Watch the radar sweep detect objects and display them dynamically.

---

## 🧑‍💻 Author
**Mohamed Waleid**  
📍 Egypt  
💼 Embedded Systems & IoT Developer  
🔗 [GitHub Profile](https://github.com/MohamedWaleid)

---

## ⚖️ License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

⭐ If you like this project, give it a **star** on GitHub — it keeps the radar spinning! 😎
