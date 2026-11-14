import sys
import pygame
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QProgressBar, QGroupBox
)
from PySide6.QtCore import QTimer, Qt

class GamePilot(QMainWindow): # our class inhereting from QMainWindow class
    # constructor
    def __init__(self):

        super().__init__() # super bcoz we are extending class QMainWindow

        self.setWindowTitle("GamePilot | Controller Studio")
        self.resize(850, 650) # width - 850 px, height - 650 px

        # initialize pygame and joystick module
        pygame.init()
        pygame.joystick.init()

        # Initialize a hidden display for pygame event processing
        pygame.display.set_mode((1,1), pygame.HIDDEN) # 1 by 1 pixel hidden display

        self.controller = None # stores the connected controller object
        self.signature = None # stores controller identification information
        self.axis_bars = [] # stores UI progress bars representing joystick axes
        self.axis_values = [] # stores numerical axis readings
        self.button_labels = [] # stores labels displaying button states
        self.hat_labels = [] # stores labels displaying d-pad/hat states

        self.setup_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_controller) # telling what to do when timer times out, that is call update_controller method
        self.timer.start(30) # 30 milliseconds update interval

    # function for creating the visual structure of the desktop application
    def setup_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        self.main_layout = QVBoxLayout(central) # vertical layout for the main window

        title = QLabel("GAMEPILOT")
        title.setStyleSheet(
            "font-size: 30px; font-weight: bold; color: #60a5fa;"
        )

        subtitle = QLabel("Controller Detection & Input Monitor")

        self.status = QLabel("Searching for controller...")
        self.status.setStyleSheet(
            "font-size: 15px; color: #f59e0b;"
        )

        self.name_label = QLabel("Controller: Not Connected")

        self.main_layout.addWidget(title)
        self.main_layout.addWidget(subtitle)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.status)
        self.main_layout.addWidget(self.name_label)

        self.info_group = QGroupBox("Live Controller Inputs")
        self.info_layout = QVBoxLayout(self.info_group)

        self.main_layout.addWidget(self.info_group)
        self.main_layout.addStretch()

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #111827;
                color: #f9fafb;
                font-size: 13px;
            }

            QGroupBox {
                border: 1px solid #374151;
                border-radius: 8px;
                margin-top: 12px;
                padding: 12px;
                font-weight: bold;
            }

            QProgressBar {
                background-color: #374151;
                border: none;
                border-radius: 4px;
                height: 15px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #3b82f6;
                border-radius: 4px;
            } 
        """)

    def clear_inputs(self):

        while self.info_layout.count():
            item = self.info_layout.takeAt(0)

            # we take widget as takeAt(0) removes it from the layout, not deleting it
            widget = item.widget()

            if widget:
                # bcoz del widget will not delete the widget, it will just remove the reference to it, so we use deleteLater() to schedule the widget for deletion
                widget.deleteLater()

        # clearing the lists storing the UI elements and data
        self.axis_bars.clear()
        self.axis_values.clear()
        self.button_labels.clear()
        self.hat_labels.clear()    
            
    def connect_controller(self):

        # resetting existing controller information, if present
        self.controller = None
        self.signature = None

        count = pygame.joystick.get_count() # get the number of connected joysticks/controllers

        if count == 0:
            self.status.setText("Controller disconnected")
            self.status.setStyleSheet("color: #ef4444;")
            self.name_label.setText("Controller: Not Connected")
            self.clear_inputs()
            return
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        self.controller = joystick

        self.signature = (
            joystick.get_name(),
            joystick.get_numaxes(),
            joystick.get_numbuttons(),
            joystick.get_numhats()
        )

        self.status.setText("Controller connected")
        self.status.setStyleSheet("color: #22c55e;")

        self.name_label.setText(
            f"Controller: {joystick.get_name()}"
        )

        self.create_input_display()

    def create_input_display(self):

        self.clear_inputs()

        if not self.controller:
            return

        # joystick axes
        axis_group = QGroupBox(
            f"Joystick Axes ({self.controller.get_numaxes()})"
        )    
        axis_layout = QGridLayout(axis_group)

        for i in range(self.controller.get_numaxes()):

            name = QLabel(f"Axis {i}")

            bar = QProgressBar()
            bar.setRange(-100, 100)
            bar.setValue(0)

            value = QLabel("0.00")
            value.setMinimumWidth(55)

            axis_layout.addWidget(name, i, 0) # col 0 for name, col 1 for bar, col 2 for value
            axis_layout.addWidget(bar, i, 1) # col 0 for name, col 1 for bar, col 2 for value
            axis_layout.addWidget(value, i, 2) # col 0 for name, col 1 for bar, col 2 for value

            self.axis_bars.append(bar)
            self.axis_values.append(value)

        self.info_layout.addWidget(axis_group)

        # buttons
        button_group = QGroupBox(
            f"Buttons ({self.controller.get_numbuttons()})"
        )

        button_layout = QGridLayout(button_group)

        for i in range(self.controller.get_numbuttons()):
            label = QLabel(f"Button {i}: RELEASED")
            label.setStyleSheet("color: #9ca3af;")

            button_layout.addWidget(
                label, i // 4, i % 4
            )

            self.button_labels.append(label)

        self.info_layout.addWidget(button_group)

        # d-pad / hats
        hat_group = QGroupBox(
            f"d-pad / hats ({self.controller.get_numhats()})"
        )    

        hat_layout = QHBoxLayout(hat_group)

        for i in range(self.controller.get_numhats()):

            label = QLabel(f"Hat {i}: (0, 0)")
            hat_layout.addWidget(label)
            self.hat_labels.append(label)

        if self.controller.get_numhats() == 0:
            hat_layout.addWidget(
                QLabel("No hat inputs detected")
            )

        self.info_layout.addWidget(hat_group)

    def update_controller(self):

        if not pygame.get_init() or not pygame.display.get_init():
            self.timer.stop()
            self.status.setText("Pygame subsystem not initialized")
            self.status.setStyleSheet("color: #ef4444;")
            return 

        try:
            pygame.event.pump() # process pygame events to update controller state

            if self.controller is None:
                if pygame.joystick.get_count() > 0:
                    self.connect_controller()
                return

            if not self.controller.get_init():
                self.connect_controller()
                return

            current = (
                self.controller.get_name(),
                self.controller.get_numaxes(),
                self.controller.get_numbuttons(),
                self.controller.get_numhats()
            )

            if current != self.signature:
                self.connect_controller()
                return

            # read joystick axes
            for i in range(len(self.axis_bars)):

                value = self.controller.get_axis(i)

                percentage = int(value * 100)

                self.axis_bars[i].setValue(percentage)
                self.axis_values[i].setText(
                    f"{value:.2f}"
                )

            # read buttons
            for i in range(len(self.button_labels)):

                pressed = self.controller.get_button(i)

                if pressed: 
                    self.button_labels[i].setText(
                        f"Button {i}: PRESSED"
                    )
                    self.button_labels[i].setStyleSheet(
                        "color: #22c55e; font-weight: bold;"
                    )         
                else: 
                    self.button_labels[i].setText(
                        f"Button {i}: RELEASED"
                    )
                    self.button_labels[i].setStyleSheet(
                        "color: #9ca3af;"
                    )

            # read D-pad / hats
            for i in range(len(self.hat_labels)):

                value = self.controller.get_hat(i)

                self.hat_labels[i].setText(
                    f"Hat {i}: {value}"
                )

        except  pygame.error:
            self.connect_controller() # if error happens try to reconnect the controller

    def closeEvent(self, event):

        pygame.quit()
        event.accept()


if __name__ == "__main__": # prevents application from launching automatically whenever another python file imports main.py
    app = QApplication(sys.argv) # command line arguments

    window = GamePilot()
    window.show()

    sys.exit(app.exec()) # app.exec() runs the event loops, when it ends it returns an exit code, sys.exit passes the exit code ot python's process termination status.                  