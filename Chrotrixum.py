import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLineEdit,
    QPushButton, QVBoxLayout, QWidget
)
from PyQt6.QtWebEngineWidgets import QWebEngineView


class ChrotrixumBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chrotrixum")
        self.resize(1200, 800)

        # --- Creación de los componentes principales ---
        # 1. El motor de renderizado web (el "corazón" del navegador)
        self.browser = QWebEngineView()

        # 2. La barra de direcciones (QLineEdit)
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Ingresa una URL o busca en Google...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # 3. La barra de herramientas con botones de navegación
        self.toolbar = QToolBar("Navegación")
        self.addToolBar(self.toolbar)

        # --- Creación de botones ---
        self.btn_back = QPushButton("←")
        self.btn_back.clicked.connect(self.browser.back)

        self.btn_forward = QPushButton("→")
        self.btn_forward.clicked.connect(self.browser.forward)

        self.btn_reload = QPushButton("⟳")
        self.btn_reload.clicked.connect(self.browser.reload)

        self.btn_home = QPushButton("⌂")
        self.btn_home.clicked.connect(self.navigate_home)

        # --- Ensamblaje de la interfaz ---
        # Agregamos los botones y la barra de direcciones a la barra de herramientas
        self.toolbar.addWidget(self.btn_back)
        self.toolbar.addWidget(self.btn_forward)
        self.toolbar.addWidget(self.btn_reload)
        self.toolbar.addWidget(self.btn_home)
        self.toolbar.addWidget(self.url_bar) # La barra de URL ocupa el espacio restante

        # Creamos un widget central con un layout vertical
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.browser) # El visor web ocupa casi toda la ventana
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # --- Conexiones de señales ---
        # Actualiza la barra de URL cuando la página cambia de dirección
        self.browser.urlChanged.connect(self.update_url_bar)

        # --- Carga inicial ---
        self.navigate_home()

    def navigate_home(self):
        """Carga la página de inicio (Google)."""
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        """Toma el texto de la barra de URL y carga la página."""
        url_text = self.url_bar.text().strip()
        if not url_text:
            return

        # Si el texto parece una URL (contiene un punto), se usa directamente.
        # Si no, se asume que es una búsqueda en Google.
        if "." in url_text and " " not in url_text:
            if not url_text.startswith(("http://", "https://")):
                url_text = "https://" + url_text
            self.browser.setUrl(QUrl(url_text))
        else:
            # Realiza una búsqueda en Google
            search_url = f"https://www.google.com/search?q={url_text}"
            self.browser.setUrl(QUrl(search_url))

    def update_url_bar(self, qurl):
        """Actualiza el texto de la barra de URL con la dirección actual."""
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0) # Muestra el inicio de la URL


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChrotrixumBrowser()
    window.show()
    sys.exit(app.exec())