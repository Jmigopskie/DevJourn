from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import sys

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Music Player")
        self.resize(300, 100)

        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_music)

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)

    def play_music(self):
        file_path = "file:///C:/Users/jmj11/Downloads/journal/MusicPlayer/Immortals.mp3"
        self.player.setSource(QUrl(file_path))
        self.player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec())
