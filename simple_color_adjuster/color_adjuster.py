import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout,
                                QGroupBox, QFormLayout, QSlider, QPushButton,
                                QWidget, QVBoxLayout, QLabel, QFileDialog)
from PIL import Image, ImageEnhance
from PIL.ImageQt import ImageQt
from qdarktheme import load_stylesheet

class ImageColorController(QGroupBox):
    def __init__(self):
        super().__init__("Color Controllers")

        self.contrast = QSlider(Qt.Horizontal)
        self.exposure = QSlider(Qt.Horizontal)
        self.saturation = QSlider(Qt.Horizontal)

        self.reset()

        form_layout = QFormLayout()

        form_layout.addRow("Contrast", self.contrast)
        form_layout.addRow("Exposure", self.exposure)
        form_layout.addRow("Saturation", self.saturation)

        self.setLayout(form_layout)


    
    def get_saturation_value(self):
        return (self.saturation.value() / 100) * 10
    
    def get_exposure_value(self):
        return (self.exposure.value() / 100) * 2

    def get_contrast_value(self):
        return (self.contrast.value() / 100) * 10
    
    def reset(self):
        self.saturation.setSliderPosition(10)
        self.exposure.setSliderPosition(50)
        self.contrast.setSliderPosition(10)

        

class ImageFileMenu(QGroupBox):

    
    def __init__(self):
        super().__init__("File Menu")

        self.enhanced_image_visualization = QPushButton()
        self.reset_enhances = QPushButton()
        self.upload_image = QPushButton()
        self.save_image = QPushButton()

        save_icon = QPixmap("static/images/4136712.png")
        reset_icon = QPixmap("static/images/2618245.png")
        upload_icon = QPixmap("static/images/2055824.png")
        enhance_icon = QPixmap("static/images/17499.png")

        self.save_image.setIcon(save_icon)
        self.upload_image.setIcon(upload_icon)
        self.reset_enhances.setIcon(reset_icon)
        self.enhanced_image_visualization.setIcon(enhance_icon)

        self.icon_size = QSize(36, 36)

        self.enhanced_image_visualization.setIconSize(self.icon_size)
        self.reset_enhances.setIconSize(self.icon_size)
        self.upload_image.setIconSize(self.icon_size)
        self.save_image.setIconSize(self.icon_size)

        layout = QVBoxLayout()
        layout.addWidget(self.enhanced_image_visualization)
        layout.addWidget(self.reset_enhances)
        layout.addWidget(self.upload_image)
        layout.addWidget(self.save_image)

        self.setLayout(layout)

        self.enhanced_image_visualization.setCheckable(True)

        self.enhanced_image_visualization.clicked.connect(self.change_enhanced_image_visualization_color)

        self.enhanced_image_visualization.setChecked(True)

    def change_enhanced_image_visualization_color(self):
        
        if self.enhanced_image_visualization.isChecked(): 
            self.enhanced_image_visualization.setIcon(QPixmap("static/images/17499.png"))
        else:
            self.enhanced_image_visualization.setIcon(QPixmap("static/images/17495.png"))
        

    


class ToolBar(QWidget):
    def __init__(self):
        super().__init__()

        self.color_controller = ImageColorController()
        self.image_file_menu = ImageFileMenu()

        layout = QHBoxLayout()
        layout.addWidget(self.image_file_menu)
        layout.addWidget(self.color_controller)

        self.setMaximumHeight(256)
        

        self.setLayout(layout)

class ImageColorGrader(QWidget):

    def __init__(self):
        super().__init__()

        self.original_image = None
        self.enhanced_image = None

        self.sample_image = QLabel("Upload An Image !!!")
        self.tool_bar = ToolBar()



        self.sample_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.sample_image)
        layout.addWidget(self.tool_bar)
        self.setLayout(layout)

        
        self.tool_bar.color_controller.saturation.valueChanged.connect(self.enhance_image)
        self.tool_bar.color_controller.exposure.valueChanged.connect(self.enhance_image)
        self.tool_bar.color_controller.contrast.valueChanged.connect(self.enhance_image)

        self.tool_bar.image_file_menu.upload_image.clicked.connect(self.upload_image)
        self.tool_bar.image_file_menu.reset_enhances.clicked.connect(self.tool_bar.color_controller.reset)
        self.tool_bar.image_file_menu.enhanced_image_visualization.clicked.connect(self.toggle_visualization)
        self.tool_bar.image_file_menu.save_image.clicked.connect(self.save_image)

    def upload_image(self):
        file_name = QFileDialog.getOpenFileName(filter="Images (*.png *.jpg)")
        self.original_image = Image.open(file_name[0])
        self.show_original_image()
        self.tool_bar.color_controller.reset()

    def enhance_image(self):
        if self.original_image != None:
            saturation_value = self.tool_bar.color_controller.get_saturation_value()
            exposure_value = self.tool_bar.color_controller.get_exposure_value()
            contrast_value = self.tool_bar.color_controller.get_contrast_value()

            enhancer = ImageEnhance.Color(self.original_image)
            enhance_image = enhancer.enhance(saturation_value)

            enhancer = ImageEnhance.Contrast(enhance_image)
            enhance_image = enhancer.enhance(contrast_value)

            enhancer = ImageEnhance.Brightness(enhance_image)
            enhance_image = enhancer.enhance(exposure_value)

            self.enhanced_image = enhance_image
            self.show_enhanced_image()

    def show_enhanced_image(self):
        pixmap = QPixmap.fromImage(ImageQt(self.enhanced_image))
        pixmap = pixmap.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.sample_image.setPixmap(pixmap)
    
    def show_original_image(self):
        pixmap = QPixmap.fromImage(ImageQt(self.original_image))
        pixmap = pixmap.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.sample_image.setPixmap(pixmap)
    
    def toggle_visualization(self):
        if self.original_image != None:
            if self.tool_bar.image_file_menu.enhanced_image_visualization.isChecked():
                self.show_enhanced_image()
            else:
                self.show_original_image()
    
    def save_image(self):
        file_name = QFileDialog.getSaveFileName(filter="Images (*.png *.jpg)")
        print(file_name)
        self.enhanced_image.save(file_name[0])
        


class MainWindown(QMainWindow):

    def __init__(self):
        super().__init__()

        self.image_color_grader = ImageColorGrader()

        self.setCentralWidget(self.image_color_grader)
        self.show()
        

if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setApplicationName("Color Adjuster")
    app.setStyleSheet(load_stylesheet())

    main_windown = MainWindown()

    app.exec()



