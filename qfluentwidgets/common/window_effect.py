# coding:utf-8
import sys
from enum import Enum
from ctypes import POINTER, c_bool, c_int, pointer, sizeof
from ctypes.wintypes import DWORD, HWND, LONG

from PyQt5.QtCore import QObject


class WindowEffectType(Enum):
    """ Window effect type enum """
    
    MICA = "mica"
    MICA_ALT = "micaAlt"
    ACRYLIC = "acrylic"
    DWM_BLUR = "dwmBlur"


class WINDOWCOMPOSITIONATTRIB(Enum):
    """ Window composition attribute """
    
    WCA_UNDEFINED = 0
    WCA_NCRENDERING_ENABLED = 1
    WCA_NCRENDERING_POLICY = 2
    WCA_TRANSITIONS_FORCEDISABLED = 3
    WCA_ALLOW_NCPAINT = 4
    WCA_CAPTION_BUTTON_BOUNDS = 5
    WCA_NONCLIENT_RTL_LAYOUT = 6
    WCA_FORCE_ICONIC_REPRESENTATION = 7
    WCA_EXTENDED_FRAME_BOUNDS = 8
    WCA_HAS_ICONIC_BITMAP = 9
    WCA_THEME_ATTRIBUTES = 10
    WCA_NCRENDERING_EXILED = 11
    WCA_NCADORNMENTINFO = 12
    WCA_EXCLUDED_FROM_LIVEPREVIEW = 13
    WCA_VIDEO_OVERLAY_ACTIVE = 14
    WCA_FORCE_ACTIVEWINDOW_APPEARANCE = 15
    WCA_DISALLOW_PEEK = 16
    WCA_CLOAK = 17
    WCA_CLOAKED = 18
    WCA_ACCENT_POLICY = 19
    WCA_FREEZE_REPRESENTATION = 20
    WCA_EVER_UNCLOAKED = 21
    WCA_VISUAL_OWNER = 22
    WCA_HOLOGRAPHIC = 23
    WCA_EXCLUDED_FROM_DDA = 24
    WCA_PASSIVEUPDATEMODE = 25
    WCA_USEDARKMODECOLORS = 26
    WCA_LAST = 27


class DWMWINDOWATTRIBUTE(Enum):
    """ DWM window attribute """
    
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    DWMWA_SYSTEMBACKDROP_TYPE = 38
    DWMWA_MICA_EFFECT = 1029


class DWM_SYSTEMBACKDROP_TYPE(Enum):
    """ DWM system backdrop type """
    
    DWMSBT_AUTO = 0
    DWMSBT_NONE = 1
    DWMSBT_MAINWINDOW = 2  # Mica
    DWMSBT_TRANSIENTWINDOW = 3  # Acrylic
    DWMSBT_TABBEDWINDOW = 4  # Mica Alt


class ACCENT_STATE(Enum):
    """ Accent state for Windows 7/10 blur """
    
    ACCENT_DISABLED = 0
    ACCENT_ENABLE_GRADIENT = 1
    ACCENT_ENABLE_TRANSPARENTGRADIENT = 2
    ACCENT_ENABLE_BLURBEHIND = 3  # DWM blur for Windows 7+
    ACCENT_ENABLE_ACRYLICBLURBEHIND = 4
    ACCENT_ENABLE_HOSTBACKDROP = 5
    ACCENT_INVALID_STATE = 6


def getWindowsBuildNumber():
    """ get Windows build number """
    if sys.platform != 'win32':
        return 0
    
    try:
        return sys.getwindowsversion().build
    except:
        return 0


def isWin11():
    """ check if system is Windows 11 """
    return getWindowsBuildNumber() >= 22000


def isWin11_22H2():
    """ check if system is Windows 11 22H2 or later """
    return getWindowsBuildNumber() >= 22621


def isWin7OrLater():
    """ check if system is Windows 7 or later """
    return getWindowsBuildNumber() >= 7600


class WindowEffectManager:
    """ Window effect manager for various Windows versions """
    
    def __init__(self):
        if sys.platform != 'win32':
            return
        
        try:
            from ctypes import windll
            self.user32 = windll.user32
            self.dwmapi = windll.dwmapi
        except:
            self.user32 = None
            self.dwmapi = None
    
    def setMicaEffect(self, hWnd: int, isDarkMode: bool = False):
        """ set Mica effect (Windows 11+)
        
        Parameters
        ----------
        hWnd: int
            window handle
            
        isDarkMode: bool
            whether to use dark mode
        """
        if not isWin11() or not self.dwmapi:
            return False
        
        # convert to int if needed
        if hasattr(hWnd, '__int__'):
            hWnd = int(hWnd)
        
        # set dark mode
        isDark = c_int(1 if isDarkMode else 0)
        self.dwmapi.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_USE_IMMERSIVE_DARK_MODE.value,
            pointer(isDark),
            sizeof(isDark)
        )
        
        # set Mica effect
        backdrop = c_int(DWM_SYSTEMBACKDROP_TYPE.DWMSBT_MAINWINDOW.value)
        self.dwmapi.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_SYSTEMBACKDROP_TYPE.value,
            pointer(backdrop),
            sizeof(backdrop)
        )
        
        return True
    
    def setMicaAltEffect(self, hWnd: int, isDarkMode: bool = False):
        """ set Mica Alt effect (Windows 11 22H2+)
        
        Parameters
        ----------
        hWnd: int
            window handle
            
        isDarkMode: bool
            whether to use dark mode
        """
        if not isWin11_22H2() or not self.dwmapi:
            return False
        
        # convert to int if needed
        if hasattr(hWnd, '__int__'):
            hWnd = int(hWnd)
        
        # set dark mode
        isDark = c_int(1 if isDarkMode else 0)
        self.dwmapi.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_USE_IMMERSIVE_DARK_MODE.value,
            pointer(isDark),
            sizeof(isDark)
        )
        
        # set Mica Alt effect
        backdrop = c_int(DWM_SYSTEMBACKDROP_TYPE.DWMSBT_TABBEDWINDOW.value)
        self.dwmapi.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_SYSTEMBACKDROP_TYPE.value,
            pointer(backdrop),
            sizeof(backdrop)
        )
        
        return True
    
    def setAcrylicEffect(self, hWnd: int, isDarkMode: bool = False):
        """ set Acrylic effect (Windows 11+)
        
        Parameters
        ----------
        hWnd: int
            window handle
            
        isDarkMode: bool
            whether to use dark mode
        """
        if not isWin11() or not self.dwmapi:
            return False
        
        # convert to int if needed
        if hasattr(hWnd, '__int__'):
            hWnd = int(hWnd)
        
        # set dark mode
        isDark = c_int(1 if isDarkMode else 0)
        self.dwmapi.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_USE_IMMERSIVE_DARK_MODE.value,
            pointer(isDark),
            sizeof(isDark)
        )
        
        # set Acrylic effect
        backdrop = c_int(DWM_SYSTEMBACKDROP_TYPE.DWMSBT_TRANSIENTWINDOW.value)
        self.dwmapi.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_SYSTEMBACKDROP_TYPE.value,
            pointer(backdrop),
            sizeof(backdrop)
        )
        
        return True
    
    def setDwmBlurEffect(self, hWnd: int, isEnabled: bool = True):
        """ set DWM blur effect (Windows 7+)
        
        Parameters
        ----------
        hWnd: int
            window handle
            
        isEnabled: bool
            whether to enable blur effect
        """
        if not isWin7OrLater() or not self.user32:
            return False
        
        try:
            from ctypes import Structure, c_uint
            
            # convert to int if needed
            if hasattr(hWnd, '__int__'):
                hWnd = int(hWnd)
            
            class ACCENT_POLICY(Structure):
                _fields_ = [
                    ('AccentState', c_uint),
                    ('AccentFlags', c_uint),
                    ('GradientColor', c_uint),
                    ('AnimationId', c_uint),
                ]
            
            class WINDOWCOMPOSITIONATTRIBDATA(Structure):
                _fields_ = [
                    ('Attribute', c_int),
                    ('Data', POINTER(ACCENT_POLICY)),
                    ('SizeOfData', c_int),
                ]
            
            accent = ACCENT_POLICY()
            accent.AccentState = ACCENT_STATE.ACCENT_ENABLE_BLURBEHIND.value if isEnabled else ACCENT_STATE.ACCENT_DISABLED.value
            accent.AccentFlags = 0
            accent.GradientColor = 0
            accent.AnimationId = 0
            
            data = WINDOWCOMPOSITIONATTRIBDATA()
            data.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
            data.SizeOfData = sizeof(accent)
            data.Data = pointer(accent)
            
            # use SetWindowCompositionAttribute
            self.user32.SetWindowCompositionAttribute(hWnd, pointer(data))
            
            return True
        except Exception as e:
            return False
    
    def removeEffect(self, hWnd: int):
        """ remove window effect
        
        Parameters
        ----------
        hWnd: int
            window handle
        """
        if sys.platform != 'win32':
            return False
        
        # convert to int if needed
        if hasattr(hWnd, '__int__'):
            hWnd = int(hWnd)
        
        if self.dwmapi and isWin11():
            # remove backdrop effect for Win11
            backdrop = c_int(DWM_SYSTEMBACKDROP_TYPE.DWMSBT_NONE.value)
            self.dwmapi.DwmSetWindowAttribute(
                hWnd,
                DWMWINDOWATTRIBUTE.DWMWA_SYSTEMBACKDROP_TYPE.value,
                pointer(backdrop),
                sizeof(backdrop)
            )
        
        # remove DWM blur effect
        if self.user32 and isWin7OrLater():
            self.setDwmBlurEffect(hWnd, False)
        
        return True

