"""Punto de entrada de Chrotrixum."""

from __future__ import annotations

import sys
from urllib.parse import quote_plus, urlsplit

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QToolBar,
)
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView


HOME_URL = "https://www.google.com/"


class ChrotrixumBrowser(QMainWindow):
    """Ventana principal del navegador."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Chrotrixum")
        self.resize(1200, 800)

        self.browser = QWebEngineView()
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Escribe una URL o busca en la web…")
        self.url_bar.setClearButtonEnabled(True)
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        toolbar = QToolBar("Navegación", self)
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        self.btn_back = QPushButton("←")
        self.btn_back.setToolTip("Volver")
        self.btn_back.clicked.connect(self.browser.back)

        self.btn_forward = QPushButton("→")
        self.btn_forward.setToolTip("Avanzar")
        self.btn_forward.clicked.connect(self.browser.forward)

        self.btn_reload = QPushButton("⟳")
        self.btn_reload.setToolTip("Recargar")
        self.btn_reload.clicked.connect(self.browser.reload)

        self.btn_home = QPushButton("⌂")
        self.btn_home.setToolTip("Página de inicio")
        self.btn_home.clicked.connect(self.navigate_home)

        for button in (self.btn_back, self.btn_forward, self.btn_reload, self.btn_home):
            toolbar.addWidget(button)

        toolbar.addWidget(self.url_bar)
        self.url_bar.setMinimumWidth(250)
        self.setCentralWidget(self.browser)

        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.titleChanged.connect(self.update_window_title)
        self.browser.loadProgress.connect(self.update_load_progress)
        self.browser.loadFinished.connect(self.finish_load)
        self.browser.loadFinished.connect(self.update_navigation_buttons)
        self.browser.loadStarted.connect(self.update_navigation_buttons)

        settings = self.browser.settings()
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, False
        )
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False
        )
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, False
        )
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False
        )

        self.apply_styles()
        self.navigate_home()

    def apply_styles(self) -> None:
        """Aplica un tema oscuro inicial que se ampliará después."""
        self.setStyleSheet(
            """
            QMainWindow { background: #11131a; }
            QToolBar {
                background: #191c27;
                border: none;
                spacing: 8px;
                padding: 8px;
            }
            QToolBar QPushButton {
                color: #f1f3f9;
                background: #252a39;
                border: 1px solid #343a4d;
                border-radius: 8px;
                min-width: 34px;
                min-height: 32px;
                padding: 2px 8px;
            }
            QToolBar QPushButton:hover {
                background: #343b50;
                border-color: #8b5cf6;
            }
            QLineEdit {
                color: #f1f3f9;
                background: #10121a;
                border: 1px solid #343a4d;
                border-radius: 9px;
                padding: 8px 12px;
                selection-background-color: #7c3aed;
            }
            QLineEdit:focus { border-color: #8b5cf6; }
            """
        )

    def navigate_home(self) -> None:
        self.browser.setUrl(QUrl(HOME_URL))

    def navigate_to_url(self) -> None:
        text = self.url_bar.text().strip()
        if not text:
            return

        has_whitespace = any(character.isspace() for character in text)
        parsed = urlsplit(text if "://" in text else f"https://{text}")
        looks_like_host = "." in parsed.netloc and " " not in parsed.netloc

        if not has_whitespace and looks_like_host:
            url = QUrl.fromUserInput(text)
            if url.isValid() and url.scheme() in {"http", "https"}:
                self.browser.setUrl(url)
                return

        query = quote_plus(text)
        self.browser.setUrl(QUrl(f"https://www.google.com/search?q={query}"))

    def update_url_bar(self, url: QUrl) -> None:
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0)

    def update_window_title(self, title: str) -> None:
        self.setWindowTitle(f"{title or 'Nueva pestaña'} — Chrotrixum")

    def update_load_progress(self, progress: int) -> None:
        self.statusBar().showMessage(f"Cargando… {progress}%")

    def finish_load(self, succeeded: bool) -> None:
        if not succeeded:
            self.statusBar().showMessage(
                "No se pudo cargar la página. Revisa la conexión y el certificado.",
                6000,
            )

    def update_navigation_buttons(self) -> None:
        history = self.browser.history()
        self.btn_back.setEnabled(history.canGoBack())
        self.btn_forward.setEnabled(history.canGoForward())


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Chrotrixum")
    window = ChrotrixumBrowser()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
