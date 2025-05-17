import random
from datetime import datetime
from typing import Dict

class VehicleDataGenerator:
    def __init__(self, vehicle_id: str = "Tarzan-001"):
        self.vehicle_id = vehicle_id

    def generate_can_data(self) -> Dict:
        """Simulates CAN bus data with 5% chance of faults"""
        # Normal operating ranges
        base_temp = random.randint(80, 90)
        base_voltage = round(random.uniform(12.8, 13.2), 1)

        # Inject faults 5% of the time
        if random.random() > 0.95:
            temp = random.randint(100, 110)  # Overheating
            voltage = round(random.uniform(11.5, 12.5), 1)  # Low voltage
            fault_code = "P0217"  # Engine overheat code
        else:
            temp = base_temp
            voltage = base_voltage
            fault_code = "NONE"

        return {
            "timestamp": datetime.now().isoformat(),
            "vehicle_id": self.vehicle_id,
            "rpm": random.randint(800, 3000),
            "temp": temp,
            "voltage": voltage,
            "speed": random.randint(0, 120),
            "fault_code": fault_code
        }

if __name__ == "__main__":
    generator = VehicleDataGenerator()
    print("Sample CAN Data:")
    print(generator.generate_can_data())
