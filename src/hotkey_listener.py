import threading
import win32con
from ctypes import byref, windll, wintypes

# Ref: http://timgolden.me.uk/python/win32_how_do_i/catch_system_wide_hotkeys.html


class HotkeyListener(threading.Thread):
    def __init__(self, hotkeys: dict, hotkey_actions: dict):
        super().__init__()
        self._hotkeys = hotkeys
        self._hotkey_actions = hotkey_actions
        self._thread_id = None

    def stop(self):
        windll.user32.PostThreadMessageA(self._thread_id, win32con.WM_QUIT, wintypes.WPARAM(), wintypes.LPARAM())
        self.join()

    def run(self):
        self._thread_id = threading.get_ident()
        self._register_hotkeys()
        try:
            self._listen_for_messages()
        finally:
            self._unregister_hotkeys()

    def _register_hotkeys(self):
        for identifier, (vk, modifiers) in self._hotkeys.items():
            if not windll.user32.RegisterHotKey(None, identifier, modifiers, vk):
                raise OSError(f"Unable to register hotkey {identifier}")

    def _listen_for_messages(self):
        msg = wintypes.MSG()
        while windll.user32.GetMessageA(byref(msg), None, 0, 0) != 0:
            if msg.message == win32con.WM_HOTKEY:
                action = self._hotkey_actions.get(msg.wParam)
                if action:
                    action()

            windll.user32.TranslateMessage(byref(msg))
            windll.user32.DispatchMessageA(byref(msg))

    def _unregister_hotkeys(self):
        for identifier in self._hotkeys.keys():
            windll.user32.UnregisterHotKey(None, identifier)
