import subprocess
import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QPushButton, QWidget, QLabel, QLineEdit
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MusicPlayer")
        self.ui()

    def ui(self):
        self.resize(600, 600)

        widget = QWidget()
        self.setCentralWidget(widget)


        self.items = QHBoxLayout(widget)

        self.label = QLabel("Youtube Link:")
        self.linkInput = QLineEdit()
        self.linkInput.setPlaceholderText("Paste Here")
        self.play = QPushButton("▶️")
        self.download = QPushButton("DL")
        self.play.setFixedSize(100, 100)
        self.items.addWidget(self.label)
        self.items.addWidget(self.linkInput)
        self.items.addWidget(self.download)
        self.items.addWidget(self.play)

        self.download.clicked.connect(self.dlsong)
        self.play.clicked.connect(self.playsong)

    @asyncSlot()
    async def dlsong(self):
        self.songlink = self.linkInput.text()

        self.download.setText("Waiting...")
        await MusicProcessor.converter(self.songlink)
        await asyncio.sleep(10)
        self.download.setText("DL")

    @asyncSlot()
    async def playsong(self):
        self.extractor = self.linkInput.text().split("=")
        self.song = self.extractor[1]

        self.play.setText("⏸️")
        await MusicProcessor.play(f"{self.song}.mp3")
        await asyncio.sleep(200)
        os.remove(f"{self.song}.mp3")

if __name__ == "__main__":
    app = QApplication([])

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    MusicPlayer = Player()
    MusicPlayer.show()

    with loop:
        loop.run_forever()
