import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLineEdit, QLabel, QFormLayout, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QDateEdit)
from PyQt5.QtCore import QDate
from datetime import date
from vehicle import Vehicle
from registry import VehicleRegistry

class VehicleRegistryGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.registry = VehicleRegistry()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Vehicle Registry")
        self.setGeometry(100, 100, 660, 500)

        layout = QVBoxLayout()

        self.add_button = QPushButton("Add Vehicle")
        self.add_button.clicked.connect(self.add_vehicle_dialog)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update Vehicle")
        self.update_button.clicked.connect(self.update_vehicle_dialog)
        layout.addWidget(self.update_button)

        self.search_button = QPushButton("Search Vehicle")
        self.search_button.clicked.connect(self.search_vehicle_dialog)
        layout.addWidget(self.search_button)

        self.show_all_button = QPushButton("Show All Vehicles")
        self.show_all_button.clicked.connect(self.show_all_vehicles)
        layout.addWidget(self.show_all_button)

        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        self.setLayout(layout)


    def add_vehicle_dialog(self):
        dialog = QWidget()
        dialog.setWindowTitle("Add Vehicle")
        form = QFormLayout()

        self.inputs = {}
        fields = ["vehicle_type", "brand", "engine_capacity", "color", 
                  "reg_number", "reg_date", "owner", "last_inspection"]
        for field in fields:
            if field == "vehicle_type":
                self.inputs[field] = QComboBox()
                self.inputs[field].addItems(["Car", "Truck", "Motorcycle"])
            elif field in ["reg_date", "last_inspection"]:
                self.inputs[field] = QDateEdit()
                self.inputs[field].setCalendarPopup(True) 
                self.inputs[field].setDate(QDate.currentDate()) 
            else:
                self.inputs[field] = QLineEdit()
            form.addRow(QLabel(field.replace("_", " ").title()), self.inputs[field])


        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(lambda: self.add_vehicle(dialog))
        form.addRow(submit_btn)

        dialog.setLayout(form)
        dialog.setFixedSize(400, 300)
        dialog.show()
        self.dialog = dialog

    def add_vehicle(self, dialog):
        try:
            v = Vehicle(
                self.inputs["vehicle_type"].currentText(),
                self.inputs["brand"].text(),
                int(self.inputs["engine_capacity"].text()),
                self.inputs["color"].text(),
                self.inputs["reg_number"].text(),
                self.inputs["reg_date"].date().toString("yyyy-MM-dd"),
                self.inputs["owner"].text(),
                self.inputs["last_inspection"].date().toString("yyyy-MM-dd")
            )
            self.registry.register_vehicle(v)
            QMessageBox.information(self, "Success", "Vehicle added successfully!")
            dialog.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def update_vehicle_dialog(self):
        dialog = QWidget()
        dialog.setWindowTitle("Update Vehicle")
        form = QFormLayout()

        self.update_reg_input = QLineEdit()
        form.addRow(QLabel("Registration Number"), self.update_reg_input)

        self.update_field_input = QLineEdit()
        form.addRow(QLabel("Field to update(lowercase)"), self.update_field_input)

        self.update_value_input = QLineEdit()
        form.addRow(QLabel("New Value"), self.update_value_input)

        submit_btn = QPushButton("Update")
        submit_btn.clicked.connect(lambda: self.update_vehicle(dialog))
        form.addRow(submit_btn)

        dialog.setLayout(form)
        dialog.setFixedSize(400, 200)
        dialog.show()
        self.dialog = dialog

    def update_vehicle(self, dialog):
        try:
            reg = self.update_reg_input.text()
            field = self.update_field_input.text()
            value = self.update_value_input.text()
            self.registry.update_vehicle(reg, **{field: value})
            QMessageBox.information(self, "Success", "Vehicle updated successfully!")
            dialog.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def search_vehicle_dialog(self):
        dialog = QWidget()
        dialog.setWindowTitle("Search Vehicle")
        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter registration number or owner name")
        layout.addWidget(self.search_input)

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_vehicle)
        layout.addWidget(search_btn)

        dialog.setLayout(layout)
        dialog.setFixedSize(400, 150)
        dialog.show()
        self.dialog = dialog

    def search_vehicle(self):
        query = self.search_input.text()
        vehicle = self.registry.find_by_reg_number(query)
        if vehicle:
            QMessageBox.information(self, "Search Result", str(vehicle))
        else:
            results = self.registry.find_by_owner(query)
            if results:
                QMessageBox.information(self, "Search Result", "\n".join(str(v) for v in results))
            else:
                QMessageBox.information(self, "Search Result", "No results found.")
        self.dialog.close()

    def show_all_vehicles(self):
        vehicles = self.registry.vehicles
        if not vehicles:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            QMessageBox.information(self, "Info", "No vehicles in the registry.")
            return

        headers = ["Reg Number", "Type", "Brand", "Color", "Engine(cc)", "Owner", "Reg Date", "Last Inspection"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(vehicles))

        for row, v in enumerate(vehicles):
            self.table.setItem(row, 0, QTableWidgetItem(v.reg_number))
            self.table.setItem(row, 1, QTableWidgetItem(v.vehicle_type))
            self.table.setItem(row, 2, QTableWidgetItem(v.brand))
            self.table.setItem(row, 3, QTableWidgetItem(v.color))
            self.table.setItem(row, 4, QTableWidgetItem(str(v.engine_capacity)))
            self.table.setItem(row, 5, QTableWidgetItem(v.owner))
            self.table.setItem(row, 6, QTableWidgetItem(str(v.reg_date.date())))
            self.table.setItem(row, 7, QTableWidgetItem(str(v.last_inspection.date())))

            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VehicleRegistryGUI()
    gui.show_all_vehicles()
    gui.show()
    sys.exit(app.exec_())
