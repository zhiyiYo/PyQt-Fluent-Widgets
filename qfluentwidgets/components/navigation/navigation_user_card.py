# coding:utf-8
from typing import Union

from enum import Enum
from PyQt5.QtCore import Qt, QRectF, QPropertyAnimation, pyqtProperty, QEasingCurve, QParallelAnimationGroup
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPixmap, QImage, QPainterPath, QFont
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect

from ...common.config import isDarkTheme
from ...common.icon import FluentIcon as FIF, drawIcon, toQIcon
from ...common.font import getFont
from .navigation_widget import NavigationWidget


class NavigationUserCardClickBehavior(Enum):
    """ Navigation user card click behavior """
    EXPAND = "expand"  # expand navigation panel in compact mode
    CALLBACK = "callback"  # trigger onClick callback
    EXPAND_AND_CALLBACK = "expand_and_callback"  # both expand and callback


class NavigationUserCard(NavigationWidget):
    """ Navigation user card widget """
    
    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        
        # avatar properties
        self._avatar = None
        self._avatarPath = None
        self._avatarIcon = FIF.PEOPLE
        self._avatarRadius = 12  # current avatar radius (24px diameter in compact mode)
        self._targetRadius = 12  # target radius for animation
        
        # text properties
        self._title = ""
        self._subtitle = ""
        self._titleSize = 14
        self._subtitleSize = 12
        
        # avatar background colors
        self.lightAvatarBgColor = QColor(0, 0, 0, 50)
        self.darkAvatarBgColor = QColor(255, 255, 255, 50)
        
        # click behavior
        self._compactClickBehavior = NavigationUserCardClickBehavior.EXPAND
        
        # animation properties
        self._isAnimating = False
        self._textOpacity = 0.0
        self._animationDuration = 250
        self._animationGroup = QParallelAnimationGroup(self)
        
        # avatar size animation
        self._radiusAni = QPropertyAnimation(self, b"avatarRadius", self)
        self._radiusAni.setDuration(self._animationDuration)
        self._radiusAni.setEasingCurve(QEasingCurve.OutCubic)
        
        # text opacity animation
        self._opacityAni = QPropertyAnimation(self, b"textOpacity", self)
        self._opacityAni.setDuration(int(self._animationDuration * 0.8))
        self._opacityAni.setEasingCurve(QEasingCurve.InOutQuad)
        
        self._animationGroup.addAnimation(self._radiusAni)
        self._animationGroup.addAnimation(self._opacityAni)
        
        # initial size
        self.setFixedSize(40, 36)
        
    def setAvatar(self, avatar: Union[str, QPixmap, QImage]):
        """ set avatar image
        
        Parameters
        ----------
        avatar: str | QPixmap | QImage
            avatar image source
        """
        if isinstance(avatar, str):
            self._avatarPath = avatar
            self._avatar = QPixmap(avatar)
        elif isinstance(avatar, QImage):
            self._avatar = QPixmap.fromImage(avatar)
        elif isinstance(avatar, QPixmap):
            self._avatar = avatar
        else:
            self._avatar = None
            
        self.update()
        
    def setAvatarIcon(self, icon: FIF):
        """ set avatar icon when no image is set """
        self._avatarIcon = icon
        self.update()
        
    def setAvatarBackgroundColor(self, light: QColor, dark: QColor):
        """ set avatar background color in light/dark theme mode """
        self.lightAvatarBgColor = QColor(light)
        self.darkAvatarBgColor = QColor(dark)
        self.update()
        
    def title(self):
        """ get user card title """
        return self._title
        
    def setTitle(self, title: str):
        """ set user card title """
        self._title = title
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
            self._radiusAni.setStartValue(self._avatarRadius)
            self._radiusAni.setEndValue(12)  # 24px diameter
            self._opacityAni.setStartValue(self._textOpacity)
            self._opacityAni.setEndValue(0.0)
        else:
            # expanded mode: large avatar with text
            self.setFixedSize(self.EXPAND_WIDTH, 80)
            self._radiusAni.setStartValue(self._avatarRadius)
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
        if self.isCompacted:
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
            return
        
        # in expanded mode, emit clicked signal normally
        super().mouseReleaseEvent(e)
        
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing | QPainter.TextAntialiasing
        )
        
        # draw hover background
        if self.isEnter:
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 10))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.rect(), 5, 5)
            
        # calculate avatar position
        if self.isCompacted:
            # match NavigationAvatarWidget position: (8, 6) with radius 12
            avatarX = 8
            avatarY = 6
        else:
            avatarX = 16
            avatarY = (self.height() - self._avatarRadius * 2) // 2
            
        # draw avatar
        self._drawAvatar(painter, avatarX, avatarY)
        
        # draw text in expanded mode
        if not self.isCompacted and self._textOpacity > 0:
            self._drawText(painter)
            
    def _drawAvatar(self, painter: QPainter, x: int, y: int):
        """ draw avatar image or icon """
        radius = int(self._avatarRadius)
        diameter = radius * 2
        
        # create avatar rect
        avatarRect = QRectF(x, y, diameter, diameter)
        
        # create circular clip path
        path = QPainterPath()
        path.addEllipse(avatarRect)
        
        painter.save()
        painter.setPen(Qt.NoPen)
        
        if self._avatar and not self._avatar.isNull():
            # draw avatar image - scale and center crop like AvatarWidget
            painter.setClipPath(path)
            
            # scale image
            image = self._avatar.toImage().scaled(
                diameter, diameter,
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            
            # center crop
            iw, ih = image.width(), image.height()
            if iw > diameter or ih > diameter:
                cropX = int((iw - diameter) / 2)
                cropY = int((ih - diameter) / 2)
                image = image.copy(cropX, cropY, diameter, diameter)
            
            painter.drawImage(avatarRect, image)
            
        painter.restore()
        
        # draw icon if no avatar image (without background, like other navigation items)
        if not self._avatar or self._avatar.isNull():
            drawIcon(self._avatarIcon, painter, avatarRect)
        
    def _drawText(self, painter: QPainter):
        """ draw title and subtitle """
        textX = 16 + int(self._avatarRadius * 2) + 12
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
            
            c = self.textColor()
            c.setAlpha(int(150 * self._textOpacity))
            painter.setPen(c)
            
            subtitleY = self.height() // 2 + 2
            painter.drawText(QRectF(textX, subtitleY, textWidth, self.height() - subtitleY),
                           Qt.AlignLeft | Qt.AlignTop,
                           self._subtitle)
    
    # properties
    @pyqtProperty(float)
    def avatarRadius(self):
        return self._avatarRadius
        
    @avatarRadius.setter
    def avatarRadius(self, value: float):
        self._avatarRadius = value
        self.update()
        
    @pyqtProperty(float)
    def textOpacity(self):
        return self._textOpacity
        
    @textOpacity.setter
    def textOpacity(self, value: float):
        self._textOpacity = value
        self.update()
