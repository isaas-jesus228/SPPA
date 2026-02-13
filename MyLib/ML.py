from screeninfo import get_monitors
import winreg

def is_dark_theme_enabled():
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        key = winreg.OpenKey(registry, key_path)

        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        
        return value == 0
    except Exception:
        return False

def MyRange(start, finish, step):
    arr = []
    while start < finish:
         arr.append(start)
         start += step

    return arr

def get_monitor():
    for m in get_monitors():
        if m.is_primary:
            return m
            
def get_mod(val):
    k = 0
    mod = 0

    if val == 0:
        return 1

    while True:
        mod += val
        k += 1
        fract = mod - int(mod)

        if fract == 0 or fract >= 0.99:
            return k
        
def shenter_text(text, val=37):
    
    k = 0
    f = False

    for i in range(0, len(text)):
        k += 1
        sym = text[i]

        if sym == "\n":
            k = 0
            continue

        if k == val:
            f = True

        if f and sym == " ":
            text = text[:i] + "\n" + text[i+1:]

            k = 0
            f = False
    
    return text