# coding:utf-8
import sys

if sys.platform == "win32":
    from win32con import DESKTOPHORZRES, HORZRES
    from win32gui import GetDC, ReleaseDC
    from win32print import GetDeviceCaps
elif sys.platform == "darwin":
    from Cocoa import NSScreen, NSDeviceSize, NSDeviceResolution
    from Quartz import CGDisplayScreenSize
else:
    import xcffib
    import xcffib.xproto
    import xcffib.randr
    from PyQt5.QtX11Extras import QX11Info
    from PyQt5 import sip


class DPIManager:
    """ DPI Manager """

    def __new__(cls, *args, **kwargs):
        if sys.platform == "win32":
            cls = WindowsDPIManager
        elif sys.platform == "darwin":
            cls = MacDPIManager
        else:
            cls = LinuxDPIManager
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        self.scale = self._get_scale()
        self.dpi = round(self.scale*96)

    def _get_scale(self) -> float:
        return 1


class WindowsDPIManager(DPIManager):
    """ Windows DPI Manager """

    def _get_scale(self) -> float:
        hdc = GetDC(None)
        t = GetDeviceCaps(hdc, DESKTOPHORZRES)
        d = GetDeviceCaps(hdc, HORZRES)
        ReleaseDC(None, hdc)
        return t / d


class LinuxDPIManager(DPIManager):
    """ Linux DPI Manager """

    def _get_scale(self) -> float:
        x = xcffib.connect()
        x.randr = x(xcffib.randr.key)
        res = x.randr.GetScreenResources(x.setup.roots[0].root).reply()
        dpi = 96
        px = dict(w=0, h=0)
        mm = dict(w=0, h=0)

        for crtc in res.crtcs:
            info = x.randr.GetCrtcInfo(crtc, xcffib.CurrentTime).reply()
            px['w'] += info.width
            px['h'] += info.height

        for out in res.outputs:
            info = x.randr.GetOutputInfo(out, xcffib.CurrentTime).reply()
            mm['w'] += info.mm_width
            mm['h'] += info.mm_height

        if mm['w'] > 0:
            w_dpi = px['w'] * 25.4 / mm['w']
            h_dpi = px['h'] * 25.4 / mm['h']
            dpi = (w_dpi + h_dpi) / 2

        return dpi/96


class MacDPIManager(DPIManager):

    def _get_scale(self) -> float:
        # for screen in NSScreen.screens():
        #     return screen.backingScaleFactor() 

        return 1


dpi_manager = DPIManager()
