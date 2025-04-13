from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QFileDialog, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
import os
from PIL import Image

from PIL import ImageFilter
from PIL.ImageFilter import(
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
    GaussianBlur, UnsharpMask)


app = QApplication([])
workdir = ''

win = QWidget()
win.resize(700, 500)
win.setWindowTitle('Easy Editor')
lb_image = QLabel("Картинка")
btn_dir = QPushButton("Папка")
lw_list = QListWidget()
left_but = QPushButton("Лево")
right_but = QPushButton("Право")
glass_but = QPushButton("Зеркало")
sharp_but = QPushButton("Резкость")
blwh_but = QPushButton("Ч/б")
save_but = QPushButton("Сохранить")
throw_but = QPushButton("Сбросить фильтр")

row = QHBoxLayout()
col_1 = QVBoxLayout()
col_2 = QVBoxLayout()
col_1.addWidget(btn_dir)
col_1.addWidget(lw_list)
col_2.addWidget(lb_image, 95)
row_1 = QHBoxLayout()
row_1.addWidget(left_but)
row_1.addWidget(right_but)
row_1.addWidget(glass_but)
row_1.addWidget(sharp_but)
row_1.addWidget(blwh_but)
row_1.addWidget(save_but)
row_1.addWidget(throw_but)
col_2.addLayout(row_1)

row.addLayout(col_1, 20)
row.addLayout(col_2, 80)
win.setLayout(row)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
        
    def loadImage(self, filename):
        self.dir = workdir
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
    
    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = lb_image.width(), lb_image.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        lb_image.setPixmap(scaled_pixmap)
        lb_image.setVisible(True)



    def do_bw(self):
      
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)  

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showChosenImage(self):
        if lw_list.currentRow() >= 0:
            filename = lw_list.currentItem().text()
            self.loadImage(filename)
            image_path = os.path.join(workdir, self.filename)
            self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result

def showFilenameList():
    global lw_list
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    lw_list.clear()
    for filename in filenames:
        lw_list.addItem(filename)

workimage = ImageProcessor()
btn_dir.clicked.connect(showFilenameList)
lw_list.currentRowChanged.connect(workimage.showChosenImage)
blwh_but.clicked.connect(workimage.do_bw)
right_but.clicked.connect(workimage.do_right)
glass_but.clicked.connect(workimage.do_flip)
left_but.clicked.connect(workimage.do_left)
sharp_but.clicked.connect(workimage.do_sharpen)
win.show()
app.exec_()
