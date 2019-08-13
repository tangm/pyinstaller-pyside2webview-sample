import sys
import os
from pathlib import Path
from PySide2.QtWidgets import QApplication
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtCore import QUrl, Slot, QObject, QUrl

# Some hackery required for pyInstaller
if getattr(sys, 'frozen', False) and sys.platform == 'darwin':
    os.environ['QTWEBENGINEPROCESS_PATH'] = os.path.normpath(os.path.join(
        sys._MEIPASS, 'PySide2', 'Qt', 'lib',
        'QtWebEngineCore.framework', 'Helpers', 'QtWebEngineProcess.app',
        'Contents', 'MacOS', 'QtWebEngineProcess'
    ))

data_dir = Path(os.path.abspath(os.path.dirname(__file__))) / 'data'

class Handler(QObject):
    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)

    @Slot(str, result=str)
    def sayHello(self, name):        
        return f"Hello from the other side, {name}"

class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(WebEnginePage, self).__init__(*args, **kwargs)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print("WebEnginePage Console: ", level, message, lineNumber, sourceId)

if __name__ == "__main__":
    
	# Set up the main application
    app = QApplication([])
    app.setApplicationDisplayName("Greetings from the other side")

    # Use a webengine view
    view = QWebEngineView()
    view.resize(500,200)

    # Set up backend communication via web channel
    handler = Handler()
    channel = QWebChannel()
    # Make the handler object available, naming it "backend"
    channel.registerObject("backend", handler)

    # Use a custom page that prints console messages to make debugging easier
    page = WebEnginePage()
    page.setWebChannel(channel)
    view.setPage(page)

    # Finally, load our file in the view
    url = QUrl.fromLocalFile(f"{data_dir}/index.html")
    view.load(url)
    view.show()

    app.exec_()
