import win32con
from ctypes import byref, windll, wintypes

# Ref: http://timgolden.me.uk/python/win32_how_do_i/catch_system_wide_hotkeys.html


def listen(hotkeys: dict, hotkey_actions: dict):
    _register_hotkeys(hotkeys)
    try:
        _listen_for_messages(hotkey_actions)
    finally:
        _unregister_hotkeys(hotkeys)


def _register_hotkeys(hotkeys: dict):
    for identifier, (vk, modifiers) in hotkeys.items():
        if not windll.user32.RegisterHotKey(None, identifier, modifiers, vk):
            raise OSError(f"Unable to register hotkey {identifier}")


def _listen_for_messages(hotkey_actions: dict):
    msg = wintypes.MSG()
    while windll.user32.GetMessageA(byref(msg), None, 0, 0) != 0:
        if msg.message == win32con.WM_HOTKEY:
            action = hotkey_actions.get(msg.wParam)
            if action:
                action()

        windll.user32.TranslateMessage(byref(msg))
        windll.user32.DispatchMessageA(byref(msg))


def _unregister_hotkeys(hotkeys: dict):
    for identifier in hotkeys.keys():
        windll.user32.UnregisterHotKey(None, identifier)
