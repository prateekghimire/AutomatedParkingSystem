# use PyQt to play an animated gif
# added buttons to start and stop animation
# tested with PyQt4.4 and Python 2.5
# also tested with PyQt4.5 and Python 3.0
# vegaseat
import sys 
# too lazy to keep track of QtCore or QtGui
from PyQt5.QtWidgets import QWidget,QApplication,QLabel,QSizePolicy,QPushButton,QVBoxLayout
from PyQt5.QtGui import QPixmap,QMovie
from PyQt5.QtCore import *
from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import * 

class Loading(QWidget,QMovie): 
    def __init__(self, parent=None): 
        super().__init__()
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("QMovie to show animated gif")
        
        # set up the movie screen on a label
        self.movie_screen = QLabel()
        # expand and center the label 
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, 
            QSizePolicy.Expanding)        
        self.movie_screen.setAlignment(Qt.AlignCenter) 
        btn_start = QPushButton("Start Animation")
        btn_start.clicked.connect(self.start) 
        btn_stop = QPushButton("Stop Animation")
        btn_stop.clicked.connect(self.stop)       
        main_layout = QVBoxLayout() 
        main_layout.addWidget(self.movie_screen)
        main_layout.addWidget(btn_start) 
        main_layout.addWidget(btn_stop)
        self.setLayout(main_layout) 
                
        # use an animated gif file you have in the working folder
        # or give the full file path
        self.movie = QMovie("loading.gif", QByteArray(), self) 
        self.movie.setCacheMode(QMovie.CacheAll) 
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 

        timer =QTimer(self)
        self.startAnimation()
        timer.singleShot(3000,self.stopAnimation)

        self.show()
        
        
    def start(self):
        """sart animnation"""
        self.movie.start()
        
    def stop(self):
        """stop the animation"""
        self.movie.stop()
app = QApplication(sys.argv) 
player = Loading() 
sys.exit(app.exec_())