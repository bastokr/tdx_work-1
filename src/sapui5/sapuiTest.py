from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, QVariant
import os

class CallHandler(QObject):
    @pyqtSlot(result=QVariant)
    def test(self):
        print('call received')
        return {"abc": "def", "ab": 22}
    
    @pyqtSlot(QVariant, result=QVariant)
    def test1(self, args):
        print('i got')
        print(args)
        return "ok"

class CustomNetworkAccessManager(QWebEngineView):
    def __init__(self):
        super().__init__()

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        # Intercept navigation requests and modify headers as needed
        request = self.page().networkRequest(url)
        request.setRawHeader(b'Access-Control-Allow-Origin', b'*')  # Set CORS header
        self.page().setNetworkRequest(url, request)
        return True

class WebView(QWebEngineView):
    def __init__(self):
        super(WebView, self).__init__()
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--blink-settings=darkMode=4,darkModeImagePolicy=2"

        self.channel = QWebChannel()
        self.handler = CallHandler()
        self.channel.registerObject('handler', self.handler)
        self.page().setWebChannel(self.channel)

        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)

        #custom_network_manager = CustomNetworkAccessManager()
        #self.setPage(custom_network_manager)

        self.load(QUrl('http://tipsvalleydemo.iptime.org:3031/'))

if __name__ == "__main__":
    app = QApplication([])
    view = WebView()
    view.show()
    app.exec_()
