# Floorplan Design Application

# This is the main entry point for the Floorplan Design application. It initializes the application window and sets up the basic structure for the GUI.

import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton,
)
from PyQt5.QtGui import QPixmap, QKeySequence, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QRect, QPoint


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Floorplan Design Application")

        # Removed explicit geometry setting to let the window manager handle the size
        # Added support for resizing the window and its content
        self.setMinimumSize(800, 600)  # Set a reasonable minimum size

        # Set the application to open in fullscreen mode
        self.showMaximized()

        # Central widget setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout for the central widget
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)  # Remove spacing between widgets
        self.layout.setAlignment(Qt.AlignCenter)  # Center alignment for all widgets
        self.central_widget.setLayout(self.layout)

        # Adjust the layout to center the button
        self.layout.setAlignment(Qt.AlignCenter)

        # Add the upload button back for the empty canvas
        self.upload_button = QPushButton(
            "Click here to open a floorplan and get started!"
        )
        self.upload_button.setFixedSize(300, 50)
        self.upload_button.clicked.connect(self.open_image)
        # Add Alt+O shortcut to the upload button for the empty canvas
        self.upload_button.setShortcut(
            QKeySequence("Alt+O")
        )  # Alt+O for the upload button
        self.layout.addWidget(self.upload_button)

        # Menu bar setup
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("&File")  # Alt+F to open the File menu

        # Add 'Open' action to the File menu
        self.open_action = self.file_menu.addAction(
            "&Open Floorplan"
        )  # Alt+F followed by O
        self.open_action.triggered.connect(self.open_image)

        # Add an Edit menu with Crop and Reset Floorplan options
        self.edit_menu = self.menu_bar.addMenu("&Edit")  # Alt+E to open the Edit menu

        # Initially hide the Edit menu
        self.edit_menu.menuAction().setVisible(False)

        # Add 'Crop' action to the Edit menu
        self.crop_action = self.edit_menu.addAction(
            "&Crop Floorplan"
        )  # Alt+E followed by C
        self.crop_action.triggered.connect(self.crop_floorplan)

        # Add 'Reset' action to the Edit menu
        self.reset_action = self.edit_menu.addAction(
            "&Reset Floorplan"
        )  # Alt+E followed by R
        self.reset_action.triggered.connect(self.reset_floorplan)

        self.cropping = False  # Flag to track cropping state
        self.crop_rect = QRect()  # Rectangle for cropping

        # Add the overlay to the main window
        self.overlay = Overlay(self)
        self.overlay.setGeometry(self.central_widget.geometry())
        self.overlay.show()

        self.is_image_cropped = False  # Track if the image has been cropped
        self.original_pixmap = None  # Store the original high-quality image
        self.cropped_pixmap = None  # Store the high-quality cropped image

    def open_image(self):
        # Check if running in a test environment
        if os.getenv("TEST_ENV"):
            file_path = "tests/floorplan.jpg"
        else:
            # Open file dialog to select an image
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open Floorplan Image",
                "",
                "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)",
                options=options,
            )

        # Handle cases where no file is selected
        if not file_path:
            return

        # Load and display the new image
        pixmap = QPixmap(file_path)

        # Store the original high-quality pixmap
        self.original_pixmap = pixmap
        self.cropped_pixmap = None

        # Create and configure the image label
        self.image_label = QLabel()
        self.image_label.setMinimumSize(1, 1)  # Ensure the label can be sized

        # Update the overlay's image label reference
        self.overlay.image_label = self.image_label

        # Clear any existing widgets from the layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add the image label to the layout
        self.layout.addWidget(self.image_label)

        # Scale and display the image
        self.update_image_display()

        # Hide the upload button and show the Edit menu
        if hasattr(self, "upload_button") and self.upload_button:
            self.upload_button.hide()
        self.edit_menu.menuAction().setVisible(True)

    def crop_floorplan(self):
        self.overlay.setCropping(True)
        self.overlay.crop_rect = QRect()
        self.overlay.setCursor(Qt.CrossCursor)
        self.overlay.update()

    def perform_crop(self):
        if not self.overlay.crop_rect.isNull() and hasattr(self, "image_label"):
            source_pixmap = (
                self.original_pixmap
                if self.original_pixmap
                else self.image_label.pixmap()
            )
            if source_pixmap:
                # Ensure the crop rectangle is within the image bounds
                crop_rect = self.overlay.crop_rect.normalized()
                crop_rect = crop_rect.intersected(self.image_label.rect())

                # Scale the crop rectangle to match the actual pixmap size
                scale_x = source_pixmap.width() / self.image_label.width()
                scale_y = source_pixmap.height() / self.image_label.height()
                scaled_rect = QRect(
                    int(crop_rect.x() * scale_x),
                    int(crop_rect.y() * scale_y),
                    int(crop_rect.width() * scale_x),
                    int(crop_rect.height() * scale_y),
                )

                # Store the high-quality cropped image
                self.cropped_pixmap = source_pixmap.copy(scaled_rect)
                self.is_image_cropped = True

                # Update the display
                self.update_image_display()

        self.overlay.setCropping(False)
        self.overlay.unsetCursor()
        self.overlay.crop_rect = QRect()
        self.overlay.update()

    def update_image_display(self):
        if not hasattr(self, "image_label") or not self.image_label:
            return

        # Use the appropriate high-quality source image
        source_pixmap = (
            self.cropped_pixmap if self.is_image_cropped else self.original_pixmap
        )
        if not source_pixmap:
            return

        # Calculate the scaled dimensions based on the window height while maintaining aspect ratio
        original_width = source_pixmap.width()
        original_height = source_pixmap.height()
        scaled_height = self.central_widget.height()
        scaled_width = int((original_width / original_height) * scaled_height)

        # Update the display with a fresh scaling from the high-quality source
        self.image_label.setPixmap(
            source_pixmap.scaled(
                scaled_width,
                scaled_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

    def reset_floorplan(self):
        if hasattr(self, "original_pixmap") and self.original_pixmap:
            self.is_image_cropped = False
            self.cropped_pixmap = None
            self.update_image_display()

    def resizeEvent(self, event):
        # Update overlay size to match the new window size
        if hasattr(self, "overlay"):
            self.overlay.setGeometry(self.central_widget.geometry())

        # Update the image display from the high-quality source
        self.update_image_display()

        # Call the base class implementation
        super().resizeEvent(event)

    # Remove the mouse event methods from MainWindow since they're now in Overlay
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

    # Remove the paintEvent method from MainWindow since we're using the overlay
    def paintEvent(self, event):
        super().paintEvent(event)


# Update the overlay to align the crop rectangle with the QLabel displaying the image
class Overlay(QWidget):
    def __init__(self, parent=None, image_label=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(
            Qt.WA_TransparentForMouseEvents, True
        )  # Let events pass through by default
        self.crop_rect = QRect()
        self.cropping = False
        self.image_label = image_label
        self.setCursor(Qt.ArrowCursor)
        self.last_cursor_pos = None  # Track the last cursor position

    def setCropping(self, enabled):
        self.cropping = enabled
        # Only capture mouse events when in cropping mode
        self.setAttribute(Qt.WA_TransparentForMouseEvents, not enabled)

    def isOverImage(self, pos):
        if not self.image_label:
            return False
        image_rect = self.image_label.geometry()
        return image_rect.contains(pos)

    def mousePressEvent(self, event):
        if self.cropping and event.button() == Qt.LeftButton:
            if self.isOverImage(event.pos()):
                pos = event.pos() - self.image_label.pos()
                self.crop_rect = QRect(pos, pos)
                self.update()
                event.accept()
                return
        event.ignore()

    def mouseMoveEvent(self, event):
        if self.cropping:
            pos = event.pos()
            # Update cursor based on position, regardless of button state
            if self.isOverImage(pos):
                self.setCursor(Qt.CrossCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

            if event.buttons() & Qt.LeftButton:
                if self.isOverImage(pos):
                    pos = event.pos() - self.image_label.pos()
                    self.crop_rect.setBottomRight(pos)
                    self.update()
                    event.accept()
                    return
        event.ignore()

    def mouseReleaseEvent(self, event):
        if self.cropping and event.button() == Qt.LeftButton:
            if self.isOverImage(event.pos()) and not self.crop_rect.isNull():
                if hasattr(self.parent(), "perform_crop"):
                    self.parent().perform_crop()
                event.accept()
                return
        event.ignore()

    def paintEvent(self, event):
        if self.cropping and not self.crop_rect.isNull() and self.image_label:
            painter = QPainter(self)
            pen = QPen(Qt.DashLine)
            pen.setColor(Qt.red)
            pen.setWidth(2)
            painter.setPen(pen)

            # Translate coordinates to match the image label position
            label_pos = self.image_label.pos()
            rect = QRect(
                self.crop_rect.x() + label_pos.x(),
                self.crop_rect.y() + label_pos.y(),
                self.crop_rect.width(),
                self.crop_rect.height(),
            )
            painter.drawRect(rect)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
