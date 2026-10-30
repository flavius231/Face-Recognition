import sys
import cv2 # Pentru a putea citi camera

from PyQt6.QtGui import QImage, QPixmap # Import uri pentru imagini
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication, # Pentru aplicatia main
    QHBoxLayout, # Pentru layout orizontal
    QVBoxLayout, # Pentru layout vertical
    QPushButton, # Pentru buton de tip push
    QWidget, # Pentru crearea de widget uri
    QLabel, # Pentru a putea afisa video ul
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Application Style
        self.setStyleSheet("""
            QMainWindow, QWidget { background-color: #0c0c0c; }
            QLabel { color: #00ff00; font-family: 'Courier New'; font-weight: bold; }
            QPushButton { 
                background-color: #000000; 
                color: #00ff00; 
                border: 1px solid #00ff00; 
                font-family: 'Courier New';
                padding: 8px;
            }
            QPushButton:hover { background-color: #003300; }
        """)




        # Variables:
        self.button_is_checked = False
            
        # Web Camera & Timer
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
            
        # 1. Layouts
        main_layout = QVBoxLayout()    # Vertical box (Sus - Jos)
        video_layout = QHBoxLayout()   # Horizontal box (Stânga - Dreapta)

        # 2. Widgets
        self.video1 = QLabel("Camera Laptop")
        self.video2 = QLabel("Imagine cu shader")
            
        self.button = QPushButton("Start")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.start_button)

        # 3. Asamblare (Layouts + Components)
        # Punem imaginile în layout-ul orizontal
        video_layout.addWidget(self.video1) 
        video_layout.addWidget(self.video2) 
        
        # Punem layout-ul cu imagini SUS, iar butonul JOS în layout-ul vertical
        main_layout.addLayout(video_layout) 
        main_layout.addWidget(self.button)
            
        # 4. Central Widget
        MainLayout = QWidget()
        MainLayout.setLayout(main_layout)
        self.setCentralWidget(MainLayout)

        # Window Settings
        self.setWindowTitle("Face Recognition")
        self.setFixedSize(QSize(1444, 840)) 
    
    # Auxiliary Functions
    def update_frame(self): # Takes camera image, converts to RGB and updates it to 60fps
        # 1. Citim cadrul de la cameră
        ret, frame = self.capture.read()
        
        if ret == True: # Dacă a citit cu succes
            # BGR in RGB
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 3. Extragem datele geometrice din imagine
            inaltime, latime, canale_culoare = frame_rgb.shape
            bytes_per_line = canale_culoare * latime
            
            # 4. Creăm imaginea pentru PyQt6
            q_image = QImage(frame_rgb.data, latime, inaltime, bytes_per_line, QImage.Format.Format_RGB888)
            
            # 5. O afișăm pe pânza noastră (Label-ul creat anterior)
            self.video1.setPixmap(QPixmap.fromImage(q_image))
        
    def start_button(self):
        self.timer.start(30)
        self.button_is_checked = True
        self.button.hide()
        self.button.setEnabled(False)
        print("Clicked!", self.button_is_checked)


app = QApplication(sys.argv)
window = MainWindow()
window.show() 
app.exec()