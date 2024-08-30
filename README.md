# eMAC: Elderly Monitoring and Control System

eMAC is an integrated fall detection system designed to enhance elder care through cutting-edge hardware and software components. By combining fall detection, touchless control, and health monitoring into one affordable, non-intrusive solution, eMAC empowers the elderly to live safely and independently.

## Features

### Hardware Components
- **ESP32-CAM Microcontroller**: Captures environmental input using its 2MP camera and streams data via WiFi.
- **Dual-Axis Motor System**: Enables precise camera adjustment for better coverage.
- **Secure P2P Connection**: Ensures safe data transmission to the cloud.
- **Custom 3D-Printed Housing**: Protects the hardware and optimizes functionality.
- **SG90 Servos & 5V Adapter**: Provides enhanced camera range and stable power.

### Software Stack
- **React Native Frontend**: User-friendly mobile application interface.
- **Supabase & PostgreSQL**: Efficient database management and data storage.
- **YOLOv10 Model**: A fine-tuned AI model trained on various fall scenarios, offering real-time fall detection.
- **WebRTC**: Facilitates secure, low-latency P2P connections for video streaming.

## System Architecture

1. **Data Capture**: The ESP32-CAM microcontroller captures real-time video input.
2. **Data Transmission**: Video is streamed to the cloud via a secure P2P connection using WebRTC.
3. **AI Processing**: The YOLOv10 model processes video data in the cloud, detecting falls with high accuracy.
4. **Response Mechanism**: Upon detecting a fall, the system triggers alerts and displays the nearest hospital, with an option to notify paramedics via the mobile app.



https://github.com/user-attachments/assets/599c937c-3e2a-474e-b302-0ebae2694cd3


## Challenges & Considerations

- **AI Model Training**: Ensuring that the YOLOv10 model accurately distinguishes between real falls and harmless movements.
- **Camera Mounting**: Requires a high vantage point with access to a stable power source.
