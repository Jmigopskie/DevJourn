import subprocess
import os
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QApplication, QHBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QFrame, QListWidget
from PyQt6.QtCore import QRect
import sys
from qasync import asyncSlot, QEventLoop
import asyncio

class MusicProcessor():
    @asyncSlot()
    async def converter(input):
        ytdlp_cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            input,
            '-o', '%(id)s.%(ext)s'
        ]

        try:
            await asyncio.create_subprocess_exec(ytdlp_cmd[0], *ytdlp_cmd[1:])
            print("Successfully Downloaded")
        except subprocess.CalledProcessError as e:
            print("Download Failed")

    @asyncSlot()
    async def play(song):
        ffmpeg_cmd = [
            'ffplay',
            song,
            '-nodisp',
            '-autoexit',

        ]
        await asyncio.create_subprocess_exec(ffmpeg_cmd[0], *ffmpeg_cmd[1:])


class Player(QMainWindow):
    def __init__(self, path):
        super().__init__()
        self.setWindowTitle("MusicPlayer")
        self.ui(path)

    def ui(self, path):
        self.resize(600, 600)
        widget = QWidget()
        self.setCentralWidget(widget)

        self.items = QVBoxLayout(widget)

        self.frame1 = QFrame()
        self.framehbox = QHBoxLayout()
        self.frame1.setLayout(self.framehbox)

        self.label = QLabel("Youtube Link:")
        self.linkInput = QLineEdit()
        self.linkInput.setPlaceholderText("Paste Here")
        self.play = QPushButton("▶️")
        self.download = QPushButton("DL")
        self.play.setFixedSize(100, 100)

        self.framehbox.addWidget(self.label)
        self.framehbox.addWidget(self.linkInput)
        self.framehbox.addWidget(self.download)
        self.framehbox.addWidget(self.play)

        self.frame2 = QFrame()
        self.framevbox = QVBoxLayout()
        self.frame2.setLayout(self.framevbox)

        self.songlists = QListWidget()
        self.load_songs(path)
        self.framevbox.addWidget(self.songlists)

        self.items.addWidget(self.frame2)
        self.items.addWidget(self.frame1)

        self.download.clicked.connect(self.dlsong)
        self.play.clicked.connect(self.playsong)


    def load_songs(self, path):
        if os.path.isdir(path):
            for file in os.listdir(path):
                self.songlists.addItem(file)

    @asyncSlot()
    async def dlsong(self):
        self.songlink = self.linkInput.text()

        self.download.setText("Waiting...")
        await MusicProcessor.converter(self.songlink)
        await asyncio.sleep(10)
        self.download.setText("DL")
        self.songlists.clear()
        self.load_songs(os.path.expanduser("~/MusicPlayer/songs"))

    @asyncSlot()
    async def playsong(self):
        selected_items = self.songlists.selectedItems()

        if selected_items:
            selected_song = selected_items[0].text()

            self.play.setText("Play")
            await MusicProcessor.play(os.path.join(os.path.expanduser("~/MusicPlayer/songs"), selected_song))
            self.play.setText("Pause")

        else:
            if "=" in self.linkinput.text():
                self.extractor = self.linkinput.text().split("=")
                self.song = self.extractor[1]


                self.play.setText("Play")
                await MusicProcessor.play(f"{self.song}.mp3")
                self.play.setText("Pause")

if __name__ == "__main__":
    app = QApplication([])

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    song_paths = os.path.expanduser("~/MusicPlayer/songs")
    MusicPlayer = Player(song_paths)
    MusicPlayer.show()

    with loop:
        loop.run_forever()
