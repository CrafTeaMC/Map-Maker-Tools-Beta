import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

class HoverButton(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setStyleSheet("background-color: #1f6aa5; border-radius: 30px; font-size: 20px; min-width: 200px; min-height: 60px;")

    def enterEvent(self, event):
        self.setStyleSheet("background-color: #14567c; border-radius: 30px; font-size: 20px; min-width: 200px; min-height: 60px;")

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: #1f6aa5; border-radius: 30px; font-size: 20px; min-width: 200px; min-height: 60px;")

class ClickableImage(QLabel):
    def __init__(self, imagePath, url, parent=None):
        super(ClickableImage, self).__init__(parent)
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)  # Resmi yeniden boyutlandır
        self.setPixmap(pixmap)
        self.url = url

    def mousePressEvent(self, event):
        QDesktopServices.openUrl(QUrl(self.url))

class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CRAFTEA Map Maker Tools')
        self.setStyleSheet("background-color: rgb(36, 36, 36); color: white;")
        
        vbox = QVBoxLayout()

        hbox_top = QHBoxLayout()
        hbox_top.addStretch(1)
        discordLogo = ClickableImage('textures/discord-logo.png', 'https://discord.gg/pNEky6DdvG', self)
        hbox_top.addWidget(discordLogo)
        youtubeLogo = ClickableImage('textures/youtube-logo.png', 'https://www.youtube.com/@CrafTeaEnglish', self)
        hbox_top.addWidget(youtubeLogo)
        vbox.addLayout(hbox_top)

        label = QLabel('CRAFTEA')
        label.setFont(QFont('Arial', 30))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label)

        vbox.addStretch(1)

        hbox = QHBoxLayout()

        btn1 = HoverButton('Cinematic Generator', self)
        btn1.clicked.connect(lambda: os.startfile(os.path.join(os.getcwd(), 'cinematic', 'dist', 'generator.exe')))
        hbox.addWidget(btn1)

        btn2 = HoverButton('If Block Generator', self)
        btn2.clicked.connect(lambda: os.startfile(os.path.join(os.getcwd(), 'ifblock', 'dist', 'generator.exe')))
        hbox.addWidget(btn2)

        btn3 = HoverButton('Item Replace', self)
        btn3.clicked.connect(lambda: os.startfile(os.path.join(os.getcwd(), 'itemreplace', 'dist', 'generator.exe')))
        hbox.addWidget(btn3)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

def main():
    app = QApplication(sys.argv)
    ex = Launcher()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
