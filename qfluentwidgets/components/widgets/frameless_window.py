import sys

if sys.platform != "win32" or sys.getwindowsversion().build < 22000:
    from qframelesswindow import FramelessWindow
else:
    from ctypes.wintypes import MSG

    import win32con
    from PySide6.QtCore import QPoint, QEvent, Qt
    from PySide6.QtGui import QCursor, QMouseEvent
    from PySide6.QtWidgets import QApplication

    from qframelesswindow import AcrylicWindow as Window
    from qframelesswindow.titlebar.title_bar_buttons import TitleBarButtonState


    class FramelessWindow(Window):
        """ Frameless window """

        def __init__(self, parent=None):
            super().__init__(parent)
            self.windowEffect.setMicaEffect(self.winId())

        def nativeEvent(self, eventType, message):
            """ Handle the Windows message """
            msg = MSG.from_address(message.__int__())
            if not msg.hWnd:
                return super().nativeEvent(eventType, message)

            if msg.message == win32con.WM_NCHITTEST and self._isResizeEnabled:
                if self._isHoverMaxBtn():
                    self.titleBar.maxBtn.setState(TitleBarButtonState.HOVER)
                    return True, win32con.HTMAXBUTTON

            elif msg.message in [0x2A2, win32con.WM_MOUSELEAVE]:
                self.titleBar.maxBtn.setState(TitleBarButtonState.NORMAL)
            elif msg.message in [win32con.WM_NCLBUTTONDOWN, win32con.WM_NCLBUTTONDBLCLK] and self._isHoverMaxBtn():
                e = QMouseEvent(QEvent.MouseButtonPress, QPoint(), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
                QApplication.sendEvent(self.titleBar.maxBtn, e)
                return True, 0
            elif msg.message in [win32con.WM_NCLBUTTONUP, win32con.WM_NCRBUTTONUP] and self._isHoverMaxBtn():
                e = QMouseEvent(QEvent.MouseButtonRelease, QPoint(), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
                QApplication.sendEvent(self.titleBar.maxBtn, e)

            return super().nativeEvent(eventType, message)

        def _isHoverMaxBtn(self):
            pos = QCursor.pos() - self.geometry().topLeft() - self.titleBar.pos()
            return self.titleBar.childAt(pos) is self.titleBar.maxBtn