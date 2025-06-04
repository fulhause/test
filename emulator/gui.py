"""PyQt5 GUI to display cylinder status and configuration."""

from __future__ import annotations

from typing import List

from PyQt5 import QtCore, QtWidgets

from .slmp_cylinder import Cylinder, CylinderEmulator, TwoPositionCylinder, ThreePositionCylinder


class CylinderWidget(QtWidgets.QWidget):
    """Widget showing a single cylinder."""

    def __init__(self, cylinder: Cylinder, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.cylinder = cylinder
        self.label = QtWidgets.QLabel(self)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.label)
        self.update_status()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(100)

    def update_status(self) -> None:
        sig = self.cylinder.two_position_signal
        self.label.setText(
            f"Pos: {self.cylinder.position:.2f} | Signals: {int(sig[0])},{int(sig[1])}"
        )


class EmulatorWindow(QtWidgets.QWidget):
    """Main emulator window."""

    def __init__(self, emulator: CylinderEmulator, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.emulator = emulator
        self.setWindowTitle("Cylinder Emulator")

        self.widgets: List[CylinderWidget] = [CylinderWidget(cyl) for cyl in emulator.cylinders]
        layout = QtWidgets.QVBoxLayout(self)
        for w in self.widgets:
            layout.addWidget(w)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.step)
        self.timer.start(50)

    def step(self) -> None:
        self.emulator.step_all(0.05)
        for w in self.widgets:
            w.update_status()


def main() -> None:
    cylinders = [TwoPositionCylinder(stroke_length=100.0, speed=10.0) for _ in range(2)]
    emulator = CylinderEmulator(cylinders)
    app = QtWidgets.QApplication([])
    win = EmulatorWindow(emulator)
    win.show()
    app.exec_()


if __name__ == "__main__":
    main()
