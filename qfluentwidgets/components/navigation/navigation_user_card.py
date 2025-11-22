# coding:utf-8
from typing import Union

from enum import Enum
from PyQt5.QtCore import Qt, QRectF, QPropertyAnimation, pyqtProperty, QEasingCurve, QParallelAnimationGroup
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QImage

from ...common.config import isDarkTheme
from ...common.icon import FluentIcon as FIF, toQIcon
from ...common.font import getFont
from .navigation_widget import NavigationAvatarWidget


class NavigationUserCardClickBehavior(Enum):
    """ Navigation user card click behavior """
    EXPAND = "expand"  # expand navigation panel in compact mode
    CALLBACK = "callback"  # trigger onClick callback
    EXPAND_AND_CALLBACK = "expand_and_callback"  # both expand and callback


class NavigationUserCard(NavigationAvatarWidget):
    """ Navigation user card widget """

    def __init__(self, parent=None):
        super().__init__(name="", parent=parent)

        # text properties
        self._title = ""
        self._subtitle = ""
        self._titleSize = 14
        self._subtitleSize = 12
        self._subtitleColor = None  # type: QColor

        # click behavior
        self._compactClickBehavior = NavigationUserCardClickBehavior.EXPAND

        # animation properties
        self._isAnimating = False
        self._textOpacity = 0.0
        self._animationDuration = 250
        self._animationGroup = QParallelAnimationGroup(self)

        # avatar size animation
        self._radiusAni = QPropertyAnimation(self.avatar, b"radius", self)
        self._radiusAni.setDuration(self._animationDuration)
        self._radiusAni.setEasingCurve(QEasingCurve.OutCubic)
        self._radiusAni.valueChanged.connect(self._updateAvatarPosition)

        # text opacity animation
        self._opacityAni = QPropertyAnimation(self, b"textOpacity", self)
        self._opacityAni.setDuration(int(self._animationDuration * 0.8))
        self._opacityAni.setEasingCurve(QEasingCurve.InOutQuad)

        self._animationGroup.addAnimation(self._radiusAni)
        self._animationGroup.addAnimation(self._opacityAni)

        # initial size
        self.setFixedSize(40, 36)

    def setAvatarIcon(self, icon: FIF):
        """ set avatar icon when no image is set """
        self.avatar.setImage(toQIcon(icon).pixmap(64, 64))
        self.update()

    def setAvatarBackgroundColor(self, light: QColor, dark: QColor):
        """ set avatar background color in light/dark theme mode """
        self.avatar.setBackgroundColor(light, dark)
        self.update()

    def title(self):
        """ get user card title """
        return self._title

    def setTitle(self, title: str):
        """ set user card title """
        self._title = title
        self.setName(title)
        self.update()

    def subtitle(self):
        """ get user card subtitle """
        return self._subtitle

    def setSubtitle(self, subtitle: str):
        """ set user card subtitle """
        self._subtitle = subtitle
        self.update()

    def setTitleFontSize(self, size: int):
        """ set title font size """
        self._titleSize = size
        self.update()

    def setSubtitleFontSize(self, size: int):
        """ set subtitle font size """
        self._subtitleSize = size
        self.update()

    def setAnimationDuration(self, duration: int):
        """ set animation duration in milliseconds """
        self._animationDuration = duration
        self._radiusAni.setDuration(duration)
        self._opacityAni.setDuration(int(duration * 0.8))

    def setCompactClickBehavior(self, behavior: NavigationUserCardClickBehavior):
        """ set click behavior in compact mode

        Parameters
        ----------
        behavior: NavigationUserCardClickBehavior
            EXPAND: expand navigation panel
            CALLBACK: trigger onClick callback
            EXPAND_AND_CALLBACK: both expand and trigger callback
        """
        self._compactClickBehavior = behavior

    def setCompacted(self, isCompacted: bool):
        """ set whether the widget is compacted """
        if isCompacted == self.isCompacted:
            return

        # stop current animation to prevent state conflicts
        if self._animationGroup.state() == QParallelAnimationGroup.Running:
            self._animationGroup.stop()
            # disconnect old finished signal to avoid duplicate calls
            try:
                self._animationGroup.finished.disconnect(self._onAnimationFinished)
            except:
                pass

        self.isCompacted = isCompacted
        self._isAnimating = True

        if isCompacted:
            # compact mode: 24x24 avatar like NavigationAvatarWidget
            self.setFixedSize(40, 36)
            self._radiusAni.setStartValue(self.avatar.radius)
            self._radiusAni.setEndValue(12)  # 24px diameter
            self._opacityAni.setStartValue(self._textOpacity)
            self._opacityAni.setEndValue(0.0)
        else:
            # expanded mode: large avatar with text
            self.setFixedSize(self.EXPAND_WIDTH, 80)
            self._radiusAni.setStartValue(self.avatar.radius)
            self._radiusAni.setEndValue(32)  # 64px diameter
            self._opacityAni.setStartValue(self._textOpacity)
            self._opacityAni.setEndValue(1.0)

        self._animationGroup.finished.connect(self._onAnimationFinished)
        self._animationGroup.start()

    def _onAnimationFinished(self):
        """ handle animation finished """
        self._isAnimating = False
        # disconnect to avoid signal accumulation
        try:
            self._animationGroup.finished.disconnect(self._onAnimationFinished)
        except:
            pass

        self.update()

    def mouseReleaseEvent(self, e):
        """ handle mouse release event """
        # handle compact mode click behavior
        if not self.isCompacted:
            super().mouseReleaseEvent(e)
            return

        self.isPressed = False
        self.update()

        shouldExpand = self._compactClickBehavior in [
            NavigationUserCardClickBehavior.EXPAND,
            NavigationUserCardClickBehavior.EXPAND_AND_CALLBACK
        ]
        shouldCallback = self._compactClickBehavior in [
            NavigationUserCardClickBehavior.CALLBACK,
            NavigationUserCardClickBehavior.EXPAND_AND_CALLBACK
        ]

        # expand navigation panel if needed
        if shouldExpand:
            parent = self.parent()
            while parent:
                if hasattr(parent, 'expand'):
                    parent.expand()
                    break
                parent = parent.parent()

        # emit clicked signal if needed
        if shouldCallback:
            self.clicked.emit(True)

        e.accept()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing | QPainter.TextAntialiasing
        )

        if self.isPressed:
            painter.setOpacity(0.7)

        # draw hover background
        self._drawBackground(painter)

        # draw text in expanded mode
        if not self.isCompacted and self._textOpacity > 0:
            self._drawText(painter)

    def _drawText(self, painter: QPainter):
        """ draw title and subtitle """
        textX = 16 + int(self.avatar.radius * 2) + 12
        textWidth = self.width() - textX - 16

        # draw title
        painter.setFont(getFont(self._titleSize, QFont.Bold))
        c = self.textColor()
        c.setAlpha(int(255 * self._textOpacity))
        painter.setPen(c)

        titleY = self.height() // 2 - 2
        painter.drawText(QRectF(textX, 0, textWidth, titleY),
                        Qt.AlignLeft | Qt.AlignBottom,
                        self._title)

        # draw subtitle with semi-transparent color
        if self._subtitle:
            painter.setFont(getFont(self._subtitleSize))

            c = self.subtitleColor or self.textColor()
            c.setAlpha(int(150 * self._textOpacity))
            painter.setPen(c)

            subtitleY = self.height() // 2 + 2
            painter.drawText(QRectF(textX, subtitleY, textWidth, self.height() - subtitleY),
                           Qt.AlignLeft | Qt.AlignTop,
                           self._subtitle)

    def _updateAvatarPosition(self):
        """ update avatar position based on current size """
        if self.isCompacted:
            self.avatar.move(8, 6)
        else:
            self.avatar.move(16, (self.height() - self.avatar.height()) // 2)

    # properties
    @pyqtProperty(float)
    def textOpacity(self):
        return self._textOpacity

    @textOpacity.setter
    def textOpacity(self, value: float):
        self._textOpacity = value
        self.update()

    @pyqtProperty(QColor)
    def subtitleColor(self):
        return self._subtitleColor

    @subtitleColor.setter
    def subtitleColor(self, color: QColor):
        self._subtitleColor = color
        self.update()
