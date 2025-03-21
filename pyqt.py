import sys
import airsim
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox
)
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, QDateTime


class DroneUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interface.ui", self)  # Загружаем UI из файла


class DroneInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: lightgray;")
        self.setWindowTitle("Интерфейс БПЛА")
        self.setGeometry(100, 100, 900, 600)

        layout = QVBoxLayout()

        layout.addWidget(self.create_navigation_block())
        layout.addWidget(self.create_power_block())
        layout.addWidget(self.create_propeller_block())

        self.setLayout(layout)

        # Подключение к AirSim
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()

        # Таймер для обновления данных из AirSim
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Обновляем каждую секунду

    def create_navigation_block(self):
        group = QGroupBox("📍 Навигация и ориентация")
        layout = QGridLayout()

        self.label_compass = QLabel("Компас: ---")
        self.label_coords = QLabel("Координаты: ---")
        self.label_altitude = QLabel("Высота над уровнем моря: ---")
        self.label_tilt = QLabel("Отклонение от оси: ---")

        layout.addWidget(self.label_compass, 0, 0)
        layout.addWidget(self.label_coords, 0, 1)
        layout.addWidget(self.label_altitude, 1, 0)
        layout.addWidget(self.label_tilt, 1, 1)

        group.setLayout(layout)
        return group

    def create_power_block(self):
        group = QGroupBox("🔋 Питание и связь")
        layout = QGridLayout()

        self.label_voltage = QLabel("Вольтаж: --- В")
        self.label_battery = QLabel("Заряд батареи: --- %")
        self.label_signal = QLabel("Уровень связи: --- %")
        self.label_datetime = QLabel("Дата и время: ---")
        self.label_speed = QLabel ("Скорость коптера: ---")

        layout.addWidget(self.label_voltage, 0, 0)
        layout.addWidget(self.label_battery, 0, 1)
        layout.addWidget(self.label_signal, 1, 0)
        layout.addWidget(self.label_datetime, 1, 1)
        layout.addWidget(self.label_speed, 2, 0)

        group.setLayout(layout)
        return group

    def create_propeller_block(self):
        group = QGroupBox("⚙️ Обороты пропеллеров")
        layout = QHBoxLayout()

        self.prop1 = QLabel("Пропеллер 1: --- об/мин")
        self.prop2 = QLabel("Пропеллер 2: --- об/мин")
        self.prop3 = QLabel("Пропеллер 3: --- об/мин")
        self.prop4 = QLabel("Пропеллер 4: --- об/мин")

        layout.addWidget(self.prop1)
        layout.addWidget(self.prop2)
        layout.addWidget(self.prop3)
        layout.addWidget(self.prop4)

        group.setLayout(layout)
        return group

    def update_data(self):
        """Получение данных из AirSim и обновление интерфейса"""
        try:
            state = self.client.getMultirotorState()
            pos = state.kinematics_estimated.position
            orient = state.kinematics_estimated.orientation
            vel = state.kinematics_estimated.linear_velocity

            # Вывод в терминал
            print(f"\n[AirSim] Данные обновлены:")
            print(f"Координаты: X={pos.x_val:.2f}, Y={pos.y_val:.2f}, Z={pos.z_val:.2f}")
            print(f"Ориентация: Pitch={orient.x_val:.2f}, Roll={orient.y_val:.2f}, Yaw={orient.z_val:.2f}")
            print(f"Скорость: {vel.x_val:.2f} м/с")

            # Обновление UI
            self.label_coords.setText(f"Координаты: X={pos.x_val:.2f}, Y={pos.y_val:.2f}, Z={pos.z_val:.2f}")
            self.label_altitude.setText(f"Высота: {pos.z_val:.2f} м")
            self.label_tilt.setText(f"Отклонение: Pitch={orient.x_val:.2f}, Roll={orient.y_val:.2f}, Yaw={orient.z_val:.2f}")
            self.label_compass.setText(f"Компас (Yaw): {orient.z_val:.2f}°")
            self.label_speed.setText(f"Скорость: {vel.x_val:.2f} м/с")

        except Exception as e:
            print(f"Ошибка получения данных из AirSim: {e}")
        
        def update_time(self):
            now = QDateTime.currentDateTime()
            self.label_datetime.setText("Дата и время: " + now.toString("dd.MM.yyyy hh:mm:ss"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DroneInterface()
    window.show()
    sys.exit(app.exec_())