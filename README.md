# Cloud-Based Vehicle Telematics Anomaly Detection

A real-time telematics platform for simulating CAN-like vehicle data, streaming it securely, and detecting anomalies using machine learning. Built for hands-on experience with modern telematics, API security, and cloud deployment.

## Features

- **CAN-like Data Simulation:** Generates realistic vehicle telemetry (RPM, temperature, voltage, speed, etc.) with occasional injected faults.
- **Real-Time Streaming:** Streams live data to clients using FastAPI WebSocket endpoints.
- **JWT Authentication:** Secures API access and data transmission with industry-standard JWT tokens.
- **Anomaly Detection:** Uses an Isolation Forest model to flag abnormal vehicle behavior in real time.
- **Cloud Deployment:** Backend and ML inference deployed on AWS EC2 for scalable, remote access.
- **Dashboard Integration:** (Planned) Live dashboard for visualization and monitoring.

### Installation

1. **Clone the repository:**
    ```
    git clone https://github.com/Architrawat25/telematics-anomaly-detection.git
    cd telematics-anomaly-detection
    ```

2. **Set up a virtual environment:**
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

4. **Train the anomaly detection model (optional, if you want to retrain):**
    - Open `ml/model_training.ipynb` in Google Colab or Jupyter.
    - Run all cells to generate and save `anomaly_detector.joblib` in the `ml/` folder.

### Running Locally

1. **Start the FastAPI backend:**
    ```
    python -m uvicorn backend.main:app --reload
    ```

2. **Test the WebSocket stream:**
    - Use the provided `test_ws.py` script or any WebSocket client.
    - Obtain a JWT token by sending a POST request to `/token`.
    - Connect to `ws://localhost:8000/ws/vehicle-data` and send the token as the first message.

### Deployment

- The backend can be deployed on AWS EC2 (Free Tier).
- After deployment, update security groups to allow HTTP/WebSocket traffic.

## Project Structure
├── backend/ # FastAPI app and JWT logic
├── simulator/ # CAN-like data generator
├── ml/ # Model training notebook and saved model
├── requirements.txt
└── test_ws.py # WebSocket test client


## Tech Stack

Python, FastAPI, WebSocket, JWT, Scikit-learn, Pandas, AWS


- [x] Real-time CAN-like data simulation
- [x] Secure streaming with JWT authentication
- [x] ML-based anomaly detection
- [x] AWS cloud deployment
- [ ] Dashboard integration (coming soon)

## Author

[Archit Rawat](https://github.com/Architrawat25)
