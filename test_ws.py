import asyncio
import websockets
import requests

# Get a JWT from the backend
response = requests.post("http://127.0.0.1:8000/token", data={"vehicle_id": "Tarzan-001"})
token = response.json()["access_token"]

async def test_ws():
    uri = "ws://127.0.0.1:8000/ws/vehicle-data"
    async with websockets.connect(uri) as websocket:
        await websocket.send(token)  # Send JWT as first message
        for _ in range(5):
            data = await websocket.recv()
            print(data)

asyncio.run(test_ws())
