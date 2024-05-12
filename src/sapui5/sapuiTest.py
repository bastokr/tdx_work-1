from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings, QWebEnginePage, QWebEngineScript
from PyQt5.QtWebChannel import QWebChannel

from PyQt5.QtCore import QObject, pyqtSlot, QUrl, QVariant

import os 


class CallHandler(QObject):


    @pyqtSlot(result=QVariant)
    def test(self):
        print('call received')
        return QVariant({"abc": "def", "ab": 22})
    
    # take an argument from javascript - JS:  handler.test1('hello!')
    @pyqtSlot(QVariant, result=QVariant)
    def test1(self, args):
      print('i got')
      print(args)
      return "ok"
  
class CustomNetworkAccessManager(QWebEnginePage):
    def __init__(self):
        super().__init__()

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        # Intercept navigation requests and modify headers as needed
        request = self.networkRequest(url)
        request.setRawHeader(b'Access-Control-Allow-Origin', b'*')  # Set CORS header
        self.setNetworkRequest(url, request)
        return True
    
class WebView(QWebEngineView):

    def __init__(self):
        super(WebView, self).__init__()
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--blink-settings=darkMode=4,darkModeImagePolicy=2"
       
        self.channel = QWebChannel()
        self.handler = CallHandler()
        self.channel.registerObject('handler', self.handler)
        self.page().setWebChannel(self.channel)
 
        #self.page().profile().setHttpUserAgent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36")
        
        #self.profile = QWebEngineProfile.defaultProfile()
        self.page().profile().setHttpUserAgent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36")
        
        
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        #settings.setAttribute(QWebEngineSettings.ContentAccessEnabled, True)  # Allow access to content from other origins
       
        custom_network_manager = CustomNetworkAccessManager()

        # Set the custom network access manager
        self.setPage(custom_network_manager)


        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))
        local_url = QUrl.fromLocalFile(file_path)
 
        self.load(local_url)
        #self.setUrl(QUrl('https://seesawclub.com/sapui.html'))


if __name__ == "__main__":
  app = QApplication([])
  view = WebView()
  view.show()
  app.exec_()