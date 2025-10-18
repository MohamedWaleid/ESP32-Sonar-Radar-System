# ⚡ ESP32 Sonar Radar System

![Platform](https://img.shields.io/badge/Platform-ESP32-blue)
![Language](https://img.shields.io/badge/Language-Python%2FC++-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Build-Stable-brightgreen)
![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)
![Python Version](https://img.shields.io/badge/Python-3.12-blue)

A **real-time radar visualization system** using **ESP32** and **HC-SR04 Ultrasonic Sensor**, displaying detected objects smoothly on a **Python-based radar interface**.  
The system continuously scans the area, calculates distance, and visualizes objects on a dynamic radar GUI.

---

## 🛰️ System Overview

[ Ultrasonic Sensor + Servo ] ⇄ [ ESP32 Controller ] ⇄ [ Python GUI Radar Display ]

* **Real-time scanning** using servo rotation.  
* **Distance measurement** via ultrasonic sensor.  
* **Live visualization** of detected objects on a 2D radar.

---

## ⚙️ Hardware Components

| Component        | Description                             |
| ---------------- | --------------------------------------- |
| ESP32            | Main Wi-Fi microcontroller              |
| HC-SR04          | Ultrasonic distance sensor              |
| SG90 Servo Motor | Rotates the sensor to cover scanning arc|
| Jumper Wires     | For connections                         |
| Breadboard       | Optional for prototyping                |

---

## 🪛 Circuit Connection

| ESP32 Pin | Component Pin |
| ---------- | ------------- |
| GPIO5      | Servo Signal  |
| GPIO18     | Trigger (HC-SR04) |
| GPIO19     | Echo (HC-SR04) |
| 5V         | VCC           |
| GND        | GND           |

> ⚠️ **Note:** Ensure servo and sensor share the same GND to prevent jittering or unstable readings.

---

## 🧩 Software Setup

### 1️⃣ ESP32 Arduino Code

* Open the `.ino` file inside the `ESP32_Code` folder.
* Update your WiFi credentials:

```cpp
const char* ssid = "YourWiFiName";
const char* password = "YourWiFiPassword";
```

* Upload to ESP32 using **Arduino IDE**.

---

### 2️⃣ Python Visualization

* Install dependencies:

```bash
pip install pyserial pygame
```

* Update the COM port (Windows) or `/dev/ttyUSBx` (Linux/Mac) in the script:

```python
SERIAL_PORT = "COM5"  # or /dev/ttyUSB0
```

* Run the radar visualization:

```bash
python radar_visualizer.py
```

---

## 📡 System Behavior

| Component | Function |
| ---------- | -------- |
| Ultrasonic Sensor | Measures distance |
| Servo Motor | Rotates sensor for scanning |
| Python App | Displays live radar visualization |

---

## 🧠 Future Improvements

* Add **object tracking algorithm** for moving targets.  
* Integrate **Bluetooth/Wi-Fi data transmission**.  
* Support for **multiple sensors** for 360° coverage.  
* Add **sound alerts** for nearby obstacles.

---

## 📜 License

This project is licensed under the **MIT License** — see the `LICENSE` file.

---

### 👨‍💻 Developed by weLTon

✨ "Visualizing the unseen — in real time."

---

## 📸 Project Demonstration

### 🔹 Real-time Radar Display

Smooth radar interface showing detected objects.

![Radar Screenshot](assets/radar_gui.png)

### 🔹 Hardware Setup

ESP32 + HC-SR04 + Servo assembly.

![Hardware Setup](assets/hardware_setup.png)

---

✨ **A perfect blend of electronics, programming, and visualization!**
