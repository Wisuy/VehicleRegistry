from datetime import datetime

class Vehicle:
    ALLOWED_TYPES = ["car", "motorcycle", "truck"]

    def __init__(self, vehicle_type, brand, engine_capacity, color,
                 reg_number, reg_date, owner, last_inspection):
        if vehicle_type.lower() not in Vehicle.ALLOWED_TYPES:
            raise ValueError(f"Invalid vehicle type. Allowed types: {Vehicle.ALLOWED_TYPES}")
        self.vehicle_type = vehicle_type.lower()
        self.brand = brand
        self.engine_capacity = engine_capacity
        self.color = color
        self.reg_number = reg_number
        self.reg_date = datetime.strptime(reg_date, "%Y-%m-%d")
        self.owner = owner
        self.last_inspection = datetime.strptime(last_inspection, "%Y-%m-%d")

    def to_dict(self):
        return {
            "vehicle_type": self.vehicle_type,
            "brand": self.brand,
            "engine_capacity": self.engine_capacity,
            "color": self.color,
            "reg_number": self.reg_number,
            "reg_date": self.reg_date.strftime("%Y-%m-%d"),
            "owner": self.owner,
            "last_inspection": self.last_inspection.strftime("%Y-%m-%d"),
        }

    @staticmethod
    def from_dict(data):
        return Vehicle(
            data["vehicle_type"],
            data["brand"],
            data["engine_capacity"],
            data["color"],
            data["reg_number"],
            data["reg_date"],
            data["owner"],
            data["last_inspection"],
        )

    def __str__(self):
        return (f"{self.reg_number} | {self.vehicle_type} | {self.brand} | "
                f"{self.color} | {self.engine_capacity}cc | Owner: {self.owner} | "
                f"Registered: {self.reg_date.date()} | Last Inspection: {self.last_inspection.date()}")
