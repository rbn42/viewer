#!/usr/bin/python
import sys
import os.path
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import PySide2

EXT = "jpg", "png", "bmp", "gif"


def bind(key, fun, window):
    print('bind:%s' % key)
    shortcut = QShortcut(window)
    shortcut.setKey(key)
    shortcut.activated.connect(fun)


class Viewer:

    def __init__(self, label, path):
        _file = None
        if not os.path.isdir(path):
            path, _file = os.path.split(path)
        self.root = path

        self.prepare_files()
        if not None == _file:
            self.index = self.files.index(_file)
        else:
            self.index = 0
        self.label = label
        bind('q', self.quit, label)
        bind('j', self._next, label)
        bind('space', self._next, label)
        bind('k', self._prev, label)

        self.blocked = False
        self.showindex()

    def prepare_files(self):
        files = os.listdir(self.root)
        self.files = []
        for n in files:
            for ext in EXT:
                if n.endswith('.' + ext):
                    self.files.append(n)
                    break
        self.files.sort()

    def _prev(self):
        self.index -= 1
        self.showindex()

    def showindex(self):
        self.index = max(0, self.index)
        self.index = min(len(self.files) - 1, self.index)
        path = self.files[self.index]
        path = os.path.join(self.root, path)
        self.showimage(path)

    def showimage(self, path):
        h = window.size().height()
        w = window.size().width()
        reader = QImageReader(path)  # , format="jpg")
        for _format in EXT:
            reader.setFormat(_format.encode())
            image = reader.read()
            if not None == image:
                break
        print(image.format())
        pix = QPixmap.fromImage(image)
        pix = pix.scaled(w, h, Qt.KeepAspectRatio)
        self.label.setPixmap(pix)

    def _next(self):
        self.index += 1
        self.showindex()

    def run(self, window):
        self.label = window
        print('init')
        self.label = QLabel("aasfd")
        self.label.show()
        self.bind('q', quit)
        self.bind('j', self._next)
        self.bind('k', self._prev)
        self.path = sys.argv[1]

    def quit(self):
        app.exec_()
        sys.exit()

app = QApplication(sys.argv)
window = QMainWindow(parent=None,
                     # flags=Qt.FramelessWindowHint
                     )
window.setWindowTitle("myviewer")
window.resize(800, 600)

label = QLabel("aasfd", window)
window.setCentralWidget(label)

window.show()


path = sys.argv[1]
viewer = Viewer(label, path)
viewer.quit()
