import sys
import ctypes
from urllib.parse import unquote
from PyQt6.QtCore import QUrl, Qt, QByteArray, QSize
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QTabWidget,
    QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QStatusBar, QMenu
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineScript, QWebEngineProfile

# ---------- 1. RENDERIZADOR DE ICONOS SVG ----------
def create_icon(svg_string: str, color: str = "#e8eaed") -> QIcon:
    """Convierte un string SVG en un QIcon de alta calidad."""
    svg_string = svg_string.replace("CURRENT_COLOR", color)
    renderer = QSvgRenderer(QByteArray(svg_string.encode('utf-8')))
    pixmap = QPixmap(128, 128)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)

def get_logo_icon() -> QIcon:
    """Devuelve el logo de Chrotrixum desde la Data URL."""
    svg_data_url = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E%3Cdefs%3E%3ClinearGradient id='r' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop stop-color='%23ff3b3b'/%3E%3Cstop offset='1' stop-color='%238b0000'/%3E%3C/linearGradient%3E%3C/defs%3E%3Ccircle cx='256' cy='256' r='244' fill='%230b0b0e' stroke='%233a1015' stroke-width='8'/%3E%3Ccircle cx='256' cy='256' r='190' fill='none' stroke='%23271920' stroke-width='2'/%3E%3Cpath d='M326 150 A132 132 0 1 0 357 306' fill='none' stroke='url(%23r)' stroke-width='42' stroke-linecap='round'/%3E%3Cpath d='M302 118 L390 126 L354 201' fill='none' stroke='%23ff4545' stroke-width='25' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M177 256 L228 307 L329 203' fill='none' stroke='%23fff' stroke-width='17' stroke-linecap='round' stroke-linejoin='round' opacity='.95'/%3E%3C/svg%3E"
    svg_clean = unquote(svg_data_url.replace("data:image/svg+xml,", ""))
    return create_icon(svg_clean)

# Iconos SVG nativos (Estilo Material Design)
ICON_BACK = '<svg viewBox="0 0 24 24"><path fill="CURRENT_COLOR" d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>'
ICON_FORWARD = '<svg viewBox="0 0 24 24"><path fill="CURRENT_COLOR" d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"/></svg>'
ICON_RELOAD = '<svg viewBox="0 0 24 24"><path fill="CURRENT_COLOR" d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>'
ICON_HOME = '<svg viewBox="0 0 24 24"><path fill="CURRENT_COLOR" d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>'
ICON_PLUS = '<svg viewBox="0 0 24 24"><path fill="CURRENT_COLOR" d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>'
ICON_EXT = '<svg viewBox="0 0 24 24"><path fill="CURRENT_COLOR" d="M20.5 11H19V7c0-1.1-.9-2-2-2h-4V3.5C13 2.12 11.88 1 10.5 1S8 2.12 8 3.5V5H4c-1.1 0-1.99.9-1.99 2v3.8H3.5c1.49 0 2.7 1.21 2.7 2.7s-1.21 2.7-2.7 2.7H2V20c0 1.1.9 2 2 2h3.8v-1.5c0-1.49 1.21-2.7 2.7-2.7 1.49 0 2.7 1.21 2.7 2.7V22H17c1.1 0 2-.9 2-2v-4h1.5c1.38 0 2.5-1.12 2.5-2.5S21.88 11 20.5 11z"/></svg>'
ICON_SEARCH = '<svg viewBox="0 0 24 24"><path fill="CURRENT_COLOR" d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>'

# ---------- 2. SCRIPTS DE EXTENSIONES ----------
EXTENSION_DARK_MODE = """
(function() {
    var style = document.createElement('style');
    style.innerHTML = `html, body { background-color: #121212 !important; color: #e0e0e0 !important; } a { color: #64b5f6 !important; }`;
    document.head.appendChild(style);
})();
"""
EXTENSION_ADBLOCK = """
(function() {
    var style = document.createElement('style');
    style.innerHTML = `.ads, .ad, .advertisement, #ads, iframe[src*="doubleclick.net"], div[id^="google_ads_"] { display: none !important; }`;
    document.head.appendChild(style);
})();
"""

# ---------- 3. ESTILOS (QSS) ----------
MODERN_QSS = """
QMainWindow { background-color: #202124; }
QWidget { color: #e8eaed; font-family: 'Segoe UI', 'Cantarell', sans-serif; font-size: 13px; }
QLineEdit { 
    background-color: #292a2d; 
    color: #e8eaed; 
    border: 1px solid #3c4043; 
    border-radius: 16px; 
    padding: 6px 12px; 
}
QLineEdit:focus { 
    border: 1px solid #8ab4f8; 
    background-color: #202124; 
}
/* Control del icono de búsqueda dentro del QLineEdit */
QLineEdit QToolButton {
    background: transparent;
    border: none;
    padding: 0px;
    margin-left: 6px;
    margin-right: 4px;
    icon-size: 18px;
}
QToolButton { background-color: transparent; border: none; border-radius: 50%; padding: 6px; }
QToolButton:hover { background-color: #3c4043; }
QToolButton:pressed { background-color: #4e5256; }
QMenu { background-color: #292a2d; color: #e8eaed; border: 1px solid #3c4043; border-radius: 8px; padding: 4px; }
QMenu::item { padding: 6px 24px 6px 12px; border-radius: 4px; }
QMenu::item:selected { background-color: #3c4043; }
QTabWidget::pane { border: none; }
QTabBar { background-color: #202124; }
QTabBar::tab {
    background-color: transparent; color: #9aa0a6; padding: 8px 16px;
    margin-right: 2px; border-top-left-radius: 8px; border-top-right-radius: 8px;
    min-width: 120px; max-width: 200px;
}
QTabBar::tab:hover { background-color: #2a2b2e; color: #e8eaed; }
QTabBar::tab:selected { background-color: #35363a; color: #ffffff; }
QTabBar::close-button { image: none; } 
QStatusBar { background-color: #202124; color: #9aa0a6; }
"""

# ---------- 4. PESTAÑA WEB ----------
class WebTab(QWidget):
    def __init__(self, browser_window, url: QUrl):
        super().__init__()
        self.window = browser_window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.view = QWebEngineView()
        layout.addWidget(self.view)

        self.view.urlChanged.connect(self.on_url_changed)
        self.view.titleChanged.connect(self.on_title_changed)
        self.view.iconChanged.connect(self.on_icon_changed)
        self.view.loadFinished.connect(self.on_load_finished)

        self.view.setUrl(url)

    def on_url_changed(self, qurl: QUrl):
        if self.window.tabs.currentWidget() is self:
            self.window.url_bar.setText(qurl.toString())
            self.window.url_bar.setCursorPosition(0)

    def on_title_changed(self, title: str):
        idx = self.window.tabs.indexOf(self)
        if idx != -1:
            short = (title[:15] + "…") if len(title) > 18 else title
            self.window.tabs.setTabText(idx, short or "Nueva pestaña")

    def on_icon_changed(self, icon: QIcon):
        idx = self.window.tabs.indexOf(self)
        if idx != -1:
            self.window.tabs.setTabIcon(idx, icon if not icon.isNull() else self.window.logo_icon)

    def on_load_finished(self, ok: bool):
        if self.window.tabs.currentWidget() is self:
            self.window.status.showMessage("✓ Cargado" if ok else "✗ Error al cargar", 3000)


# ---------- 5. VENTANA PRINCIPAL ----------
class Chrotrixum(QMainWindow):
    HOME = QUrl("https://www.google.com")

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chrotrixum")
        self.resize(1280, 800)
        self.setStyleSheet(MODERN_QSS)
        
        self.logo_icon = get_logo_icon()
        self.setWindowIcon(self.logo_icon)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- BARRA SUPERIOR PERSONALIZADA ---
        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: #202124;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 6, 10, 6)
        top_layout.setSpacing(4)

        # 1. Logo SVG
        self.btn_logo = QToolButton()
        self.btn_logo.setIcon(self.logo_icon)
        self.btn_logo.setIconSize(QSize(24, 24))
        self.btn_logo.setToolTip("Inicio")
        self.btn_logo.clicked.connect(self.navigate_home)
        top_layout.addWidget(self.btn_logo)

        # 2. Botones de navegación
        self.btn_back = QToolButton()
        self.btn_back.setIcon(create_icon(ICON_BACK))
        self.btn_back.clicked.connect(self.go_back)
        top_layout.addWidget(self.btn_back)

        self.btn_forward = QToolButton()
        self.btn_forward.setIcon(create_icon(ICON_FORWARD))
        self.btn_forward.clicked.connect(self.go_forward)
        top_layout.addWidget(self.btn_forward)

        self.btn_reload = QToolButton()
        self.btn_reload.setIcon(create_icon(ICON_RELOAD))
        self.btn_reload.clicked.connect(self.reload_page)
        top_layout.addWidget(self.btn_reload)

        self.btn_home = QToolButton()
        self.btn_home.setIcon(create_icon(ICON_HOME))
        self.btn_home.clicked.connect(self.navigate_home)
        top_layout.addWidget(self.btn_home)

        # 3. Barra de URL
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Busca en Google o escribe una URL")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        # (Se eliminó self.url_bar.setIconSize que causaba el error)
        search_action = QAction(create_icon(ICON_SEARCH, "#9aa0a6"), "", self)
        self.url_bar.addAction(search_action, QLineEdit.ActionPosition.LeadingPosition)
        
        top_layout.addSpacing(10)
        top_layout.addWidget(self.url_bar, stretch=1)
        top_layout.addSpacing(10)

        # 4. Extensiones
        self.btn_extensions = QToolButton()
        self.btn_extensions.setIcon(create_icon(ICON_EXT))
        self.ext_menu = QMenu(self)
        
        self.act_dark_mode = self.ext_menu.addAction("🌙 Modo Oscuro Universal")
        self.act_dark_mode.setCheckable(True)
        self.act_dark_mode.triggered.connect(self.toggle_dark_mode)

        self.act_adblock = self.ext_menu.addAction("🛡️ AdBlock Básico")
        self.act_adblock.setCheckable(True)
        self.act_adblock.triggered.connect(self.toggle_adblock)

        self.btn_extensions.setMenu(self.ext_menu)
        self.btn_extensions.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        top_layout.addWidget(self.btn_extensions)

        main_layout.addWidget(top_bar)

        # --- PESTAÑAS ---
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        # Botón "+" (Nueva Pestaña)
        self.btn_new_tab = QToolButton()
        self.btn_new_tab.setIcon(create_icon(ICON_PLUS))
        self.btn_new_tab.setToolTip("Nueva Pestaña (Ctrl+T)")
        self.btn_new_tab.clicked.connect(lambda: self.add_tab(self.HOME))
        self.tabs.setCornerWidget(self.btn_new_tab, Qt.Corner.TopRightCorner)

        main_layout.addWidget(self.tabs)

        self.setCentralWidget(central_widget)

        # Barra de estado
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.ext_dark_mode_activa = False
        self.ext_adblock_activa = False

        self._install_shortcuts()
        self.add_tab(self.HOME)

    # ---------- LÓGICA DE EXTENSIONES ----------
    def toggle_dark_mode(self, checked):
        self.ext_dark_mode_activa = checked
        self.apply_extensions_to_all()

    def toggle_adblock(self, checked):
        self.ext_adblock_activa = checked
        self.apply_extensions_to_all()

    def apply_extensions_to_all(self):
        profile = QWebEngineProfile.defaultProfile()
        profile.scripts().clear()

        if self.ext_dark_mode_activa:
            script = QWebEngineScript()
            script.setName("ChrotrixumDarkMode")
            script.setSourceCode(EXTENSION_DARK_MODE)
            script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
            script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
            profile.scripts().insert(script)

        if self.ext_adblock_activa:
            script = QWebEngineScript()
            script.setName("ChrotrixumAdBlock")
            script.setSourceCode(EXTENSION_ADBLOCK)
            script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
            script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
            profile.scripts().insert(script)

        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if isinstance(tab, WebTab):
                tab.view.reload()

    # ---------- GESTIÓN DE PESTAÑAS ----------
    def current_web_tab(self) -> WebTab | None:
        w = self.tabs.currentWidget()
        return w if isinstance(w, WebTab) else None

    def add_tab(self, url: QUrl):
        tab = WebTab(self, url)
        idx = self.tabs.addTab(tab, "Cargando…")
        self.tabs.setTabIcon(idx, self.logo_icon)
        self.tabs.setCurrentIndex(idx)
        return tab

    def close_tab(self, index):
        widget = self.tabs.widget(index)
        self.tabs.removeTab(index)
        widget.deleteLater()
        if self.tabs.count() == 0:
            self.close()

    def on_tab_changed(self, _):
        tab = self.current_web_tab()
        if tab:
            self.url_bar.setText(tab.view.url().toString())
            self.status.showMessage("Listo")

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if not text: return
        tab = self.current_web_tab()
        if not tab: return
        if "." in text and " " not in text:
            if not text.startswith(("http://", "https://")):
                text = "https://" + text
            tab.view.setUrl(QUrl(text))
        else:
            tab.view.setUrl(QUrl(f"https://www.google.com/search?q={text}"))

    def go_back(self):
        tab = self.current_web_tab()
        if tab: tab.view.back()

    def go_forward(self):
        tab = self.current_web_tab()
        if tab: tab.view.forward()

    def reload_page(self):
        tab = self.current_web_tab()
        if tab: tab.view.reload()

    def navigate_home(self):
        tab = self.current_web_tab()
        if tab: tab.view.setUrl(self.HOME)

    def _install_shortcuts(self):
        shortcuts = [
            ("Ctrl+T", lambda: self.add_tab(self.HOME)),
            ("Ctrl+W", lambda: self.close_tab(self.tabs.currentIndex())),
            ("Ctrl+L", lambda: self.url_bar.setFocus()),
            ("Ctrl+R", self.reload_page),
            ("F5",       self.reload_page),
            ("Alt+Left", self.go_back),
            ("Alt+Right", self.go_forward),
            ("Alt+Home", self.navigate_home),
        ]
        for keys, slot in shortcuts:
            act = QAction(self)
            act.setShortcut(QKeySequence(keys))
            act.triggered.connect(slot)
            self.addAction(act)

if __name__ == "__main__":
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("chrotrixum.browser.3.0")

    app = QApplication(sys.argv)
    app.setApplicationName("Chrotrixum")
    app.setWindowIcon(get_logo_icon())
    
    window = Chrotrixum()
    window.show()
    sys.exit(app.exec())
