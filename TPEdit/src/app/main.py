from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from flask import Flask, render_template
from threading import Thread
import sys
from werkzeug.serving import make_server

class ServerThread(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

def spawn_main_window():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return render_template('editor/index.html')

    server = ServerThread(app)
    server.start()

    class MainWindow(QMainWindow):
        def closeEvent(self, event):
            server.shutdown()

    # Create the PyQt application
    app = QApplication(sys.argv)

    # Create and configure the QWebEngineView
    view = QWebEngineView()
    view.setZoomFactor(1.0)
    main_window = MainWindow()
    main_window.setCentralWidget(view)
    view.load(QUrl("http://localhost:5000"))
    main_window.showMaximized()  # Maximizes the window

    # Run the PyQt event loop
    sys.exit(app.exec_())