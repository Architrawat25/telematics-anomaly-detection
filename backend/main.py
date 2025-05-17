from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
import sys
import os
import asyncio
import joblib
import pandas as pd
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Add simulator directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'simulator'))
from data_generator import VehicleDataGenerator

# --- JWT Configuration ---
SECRET_KEY = "secretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()
generator = VehicleDataGenerator()

# --- Load ML Model ---
try:
    model_data = joblib.load("ml/anomaly_detector.joblib")
    model = model_data['model']
    features = model_data['features']
except FileNotFoundError:
    raise RuntimeError("ML model file not found. Train model first!")

# --- JWT Functions ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# --- Anomaly Detection ---
def is_anomaly(data: dict) -> bool:
    try:
        X = pd.DataFrame([[data[f] for f in features]], columns=features)
        prediction = model.predict(X)
        return bool(prediction[0] == -1)
    except KeyError as e:
        print(f"Missing feature in data: {e}")
        return False

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Telematics Backend Running"}

@app.post("/token")
def get_token(vehicle_id: str = "SUZUKI_DEMO_001"):
    return {"access_token": create_access_token({"vehicle_id": vehicle_id})}

@app.websocket("/ws/vehicle-data")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Receive and verify JWT
        token = await websocket.receive_text()
        payload = verify_token(token)
        if not payload:
            await websocket.close(code=1008)
            return

        # Stream data with anomaly detection
        while True:
            data = generator.generate_can_data()
            data["anomaly"] = is_anomaly(data)
            await websocket.send_json(data)
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {str(e)}")
        await websocket.close(code=1011)
