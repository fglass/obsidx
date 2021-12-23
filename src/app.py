import logging
import sys
from PyQt5.QtWidgets import QApplication
from src.config import TOGGLE_HOTKEY
from src.hotkey_listener import HotkeyListener
from src.launcher_dialog import LauncherDialog
from src.tray_icon import TrayIcon


# TODO:
#   - Click highlight bug
#   - Settings menu
#   - Installer


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    launcher = LauncherDialog()

    hotkey_listener = _create_hotkey_listener(launcher)
    hotkey_listener.start()

    tray_icon = _create_tray_icon(app, launcher, hotkey_listener)
    tray_icon.show()

    app.exec()


def _create_hotkey_listener(launcher: LauncherDialog) -> HotkeyListener:
    hotkeys = {1: TOGGLE_HOTKEY}
    actions = {1: launcher.toggle_signal.emit}
    hotkey_listener = HotkeyListener(hotkeys, actions)
    return hotkey_listener


def _create_tray_icon(app: QApplication, launcher: LauncherDialog, hotkey_listener: HotkeyListener) -> TrayIcon:
    tray_icon = TrayIcon()
    tray_icon.open_action.triggered.connect(launcher.toggle_signal.emit)

    def quit_app():
        hotkey_listener.stop()
        app.quit()

    tray_icon.quit_action.triggered.connect(quit_app)

    return tray_icon


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO)
    main()
