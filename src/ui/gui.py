from src.ui.selection_page import ModeSelectionPage
from src.ui.record_page import RecordPage
from src.ui.text_entry_page import TextEntryPage

from PyQt6.QtWidgets import (QMainWindow, QStackedWidget)
from PyQt6.QtCore import Qt, QThread, QMetaObject

from src.ui.welcome_page import WelcomePage
from src.services.response_service import ResponseService
from src.services.camera_service import CameraService
from src.ui.response_page import ResponsePage
from src.core.text_processor import TextProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EmergenSee AI Assistant")
        self.setGeometry(100, 100, 400, 700)
        self.setStyleSheet("background-color: #222222;")
        
        self.text_processor = TextProcessor()

        self.response_service = ResponseService(self.text_processor)
        self.camera_service = CameraService()
        self.camera_thread = QThread()
        self.camera_service.moveToThread(self.camera_thread)
        self.camera_thread.start()
        self.response_service.response_ready.connect(self.handle_response)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.welcome_page = WelcomePage(self)
        self.mode_selection_page = ModeSelectionPage(self)
        self.record_page = RecordPage(self, self.camera_service, self.response_service)
        self.text_entry_page = TextEntryPage(self, self.response_service, self.text_processor)
        self.response_page = ResponsePage(self)

        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.mode_selection_page)
        self.stacked_widget.addWidget(self.record_page)
        self.stacked_widget.addWidget(self.text_entry_page)
        self.stacked_widget.addWidget(self.response_page)

        self.navigateToPage(0)

    def navigateToPage(self, index):
        self.stacked_widget.setCurrentIndex(index)
        if index != 2:
            QMetaObject.invokeMethod(self.camera_service, "stop_camera", Qt.ConnectionType.QueuedConnection)

    def handle_response(self, response_text):
        self.response_page.set_response(response_text)
        self.navigateToPage(4)

    def closeEvent(self, event):
        self.camera_service.stop_camera()
        self.camera_thread.quit()
        self.camera_thread.wait()
        event.accept()