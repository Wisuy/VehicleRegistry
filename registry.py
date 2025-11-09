import json
from datetime import datetime
from vehicle import Vehicle

class VehicleRegistry:
    def __init__(self, filename="vehicles.json"):
        self.vehicles = []
        self.filename = filename
        self.load_from_file()

    def register_vehicle(self, vehicle):
        if any(v.reg_number == vehicle.reg_number for v in self.vehicles):
            raise ValueError("A vehicle with this registration number already exists.")
        self.vehicles.append(vehicle)
        self.save_to_file()

    def update_vehicle(self, reg_number, **kwargs):
        vehicle = self.find_by_reg_number(reg_number)
        if not vehicle:
            raise ValueError("Vehicle not found.")
        for key, value in kwargs.items():
            if hasattr(vehicle, key):
                if key in ["reg_date", "last_inspection"]:
                    value = datetime.strptime(value, "%Y-%m-%d")
                setattr(vehicle, key, value)
        self.save_to_file()

    def find_by_reg_number(self, reg_number):
        return next((v for v in self.vehicles if v.reg_number == reg_number), None)

    def find_by_owner(self, owner_name):
        return [v for v in self.vehicles if owner_name.lower() in v.owner.lower()]

    def record_inspection(self, reg_number, date_str):
        vehicle = self.find_by_reg_number(reg_number)
        if not vehicle:
            raise ValueError("Vehicle not found.")
        vehicle.last_inspection = datetime.strptime(date_str, "%Y-%m-%d")
        self.save_to_file()

    def remove_vehicle(self, reg_number):
        self.vehicles = [v for v in self.vehicles if v.reg_number != reg_number]
        self.save_to_file()

    def vehicles_registered_after(self, date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return [v for v in self.vehicles if v.reg_date > date]

    def vehicles_with_inspection_before(self, date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return [v for v in self.vehicles if v.last_inspection < date]

    def sort_by_type(self):
        return sorted(self.vehicles, key=lambda v: v.vehicle_type)

    def save_to_file(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([v.to_dict() for v in self.vehicles], f, indent=4)

    def load_from_file(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.vehicles = [Vehicle.from_dict(v) for v in data]
        except FileNotFoundError:
            self.vehicles = []
        except json.JSONDecodeError:
            print("⚠️ Warning: JSON file corrupted. Starting with empty registry.")
            self.vehicles = []

    def __iter__(self):
        return iter(self.vehicles)
