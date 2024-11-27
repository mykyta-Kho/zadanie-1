import os
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, 
)
from PySide6.QtGui import (QPixmap, QFont)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        image_path = os.path.join(base_path, "TUKE.jpg")
        
        # Default parameters
        self.min_value = 0
        self.max_value = 1000
        self.step = 10
        self.size = 25

        # Main Widget and Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        self.setWindowTitle("Khodniev")
        self.setGeometry(100, 100, 800, 600)

        # Left side: Image
        left_layout = QVBoxLayout()
        self.image_label = QLabel()
        pixmap = QPixmap(image_path) 
        if pixmap.isNull():
            print(f"Failed to load image from {image_path}")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(200, 200)
        left_layout.addWidget(self.image_label)
        main_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()

        # Helper function to add widgets with labels
        def add_widget_with_label(layout, widget, label_text):
            hbox = QHBoxLayout()
            label = QLabel(label_text)
            hbox.addWidget(label)
            hbox.addWidget(widget)
            layout.addLayout(hbox)

        self.predmet_label = QLabel("Programovacie techniky") 
        self.meno_label = QLabel("Mykyta Khodniev") 
        self.zadanie_label = QLabel("10. Vygenerujte pole 25 náhodných celých čísiel od 0 do 1000 s krokom 10, vypíšte najvyššie a najnižšieho  číslo a vypočítajte ich rozdiel, zobrazte graf hodnôt.") 
        
        self.predmet_font = QFont("Times", 25, QFont.Bold)
        self.meno_font = QFont("Times", 14)
        self.zadanie_font = QFont("Times", 10)
        self.zadanie_font.setItalic(True)
        self.predmet_label.setFont(self.predmet_font)
        self.meno_label.setFont(self.meno_font)
        self.zadanie_label.setFont(self.zadanie_font)
        self.zadanie_label.setWordWrap(True)
        
        right_layout.addWidget(self.predmet_label)
        right_layout.addWidget(self.meno_label)
        right_layout.addWidget(self.zadanie_label)
        

        # QLineEdit for parameters
        self.line_min = QLineEdit(str(self.min_value))
        self.line_max = QLineEdit(str(self.max_value))
        self.line_step = QLineEdit(str(self.step))
        self.line_size = QLineEdit(str(self.size))


        add_widget_with_label(right_layout, self.line_min, "Min. hodnota:")
        add_widget_with_label(right_layout, self.line_max, "Max. hodnota:")
        add_widget_with_label(right_layout, self.line_step, "Veľkosť kroku:")
        add_widget_with_label(right_layout, self.line_size, "Veľkosť poľa:")


        # QPushButton to generate plot
        self.button = QPushButton('Zobraziť graf')
        self.button.clicked.connect(self.on_button_clicked)
        add_widget_with_label(right_layout, self.button, "")

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setVisible(False)  
        right_layout.addWidget(self.canvas)

        # Add right layout to the main layout
        main_layout.addLayout(right_layout)

    def on_button_clicked(self):
        # Read parameters from QLineEdit
        try:
            self.min_value = int(self.line_min.text())
            self.max_value = int(self.line_max.text())
            self.step = int(self.line_step.text())
            self.size = int(self.line_size.text())

            self.array = np.random.choice(
                np.arange(self.min_value, self.max_value + 1, self.step), self.size, replace=True
                )
            self.update_plot()
        except ValueError:
            print("Zadajte platné celé čísla pre min, max a krok.")

    def update_plot(self):
        # Clear previous plot
        self.figure.clear()

        # Compute stats
        max_value = np.max(self.array)
        min_value = np.min(self.array)
        difference = max_value - min_value

        # Create new plot
        ax = self.figure.add_subplot(111)
        ax.plot(self.array, marker='o', linestyle='-', color='b', label='Hodnoty')
        ax.axhline(max_value, color='r', linestyle='--', label=f'Max: {max_value}')
        ax.axhline(min_value, color='g', linestyle='--', label=f'Min: {min_value}')
        ax.set_title(f'Rozdiel: {difference}')
        ax.set_xlabel('Index')
        ax.set_ylabel('Hodnota')
        ax.legend()
        ax.grid(True)

        # Show canvas and refresh
        self.canvas.setVisible(True)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec())