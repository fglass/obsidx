import logging
import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from src.config import Config, FONT_SIZE
from src.hotkey_listener import HotkeyListener
from src.ui.launcher_dialog import LauncherDialog
from src.ui.settings_menu import SettingsMenu
from src.ui.tray_icon import TrayIcon


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    _set_fixed_font_size(app)

    config = Config()
    launcher = LauncherDialog(config)
    settings_menu = SettingsMenu(config)

    if config.vault_directory == "":
        settings_menu.show()

    hotkey_listener = _create_hotkey_listener(config, launcher)
    hotkey_listener.start()

    tray_icon = _create_tray_icon(app, launcher, settings_menu, hotkey_listener)
    tray_icon.show()

    app.exec()


def _set_fixed_font_size(app: QApplication):
    font = QFont()
    font.setPixelSize(FONT_SIZE)
    app.setFont(font)


def _create_hotkey_listener(config: Config, launcher: LauncherDialog) -> HotkeyListener:
    hotkeys = {1: config.toggle_hotkey}
    actions = {1: launcher.toggle_signal.emit}
    hotkey_listener = HotkeyListener(hotkeys, actions)
    return hotkey_listener


def _create_tray_icon(app: QApplication, launcher: LauncherDialog, settings_menu: SettingsMenu, hotkey_listener: HotkeyListener) -> TrayIcon:
    tray_icon = TrayIcon()
    tray_icon.open_action.triggered.connect(launcher.toggle_signal.emit)
    tray_icon.settings_action.triggered.connect(settings_menu.show)

    def quit_app():
        hotkey_listener.stop()
        app.quit()

    tray_icon.quit_action.triggered.connect(quit_app)

    return tray_icon


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO)
    main()
