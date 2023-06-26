# coding:utf-8
from typing import Union
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QParallelAnimationGroup, QEasingCurve, QMargins, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QCursor, QIcon, QImage, QPainterPath, QBrush
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QLabel, QHBoxLayout, QVBoxLayout, QApplication

from ...common.auto_wrap import TextWrap
from ...common.style_sheet import isDarkTheme, FluentStyleSheet
from ...common.icon import FluentIconBase
from .teaching_tip import IconWidget


class FlyoutViewBase(QWidget):
    """ Flyout view base class """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        painter.setBrush(
            QColor(40, 40, 40) if isDarkTheme() else QColor(248, 248, 248))
        painter.setPen(
            QColor(23, 23, 23) if isDarkTheme() else QColor(195, 195, 195))

        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 8, 8)


class FlyoutView(FlyoutViewBase):
    """ Flyout view """

    def __init__(self, title: str, content: str, icon: Union[FluentIconBase, QIcon, str] = None,
                 image: Union[str, QPixmap, QImage] = None, parent=None):
        super().__init__(parent=parent)
        """
        Parameters
        ----------
        title: str
            the title of teaching tip

        content: str
            the content of teaching tip

        icon: InfoBarIcon | FluentIconBase | QIcon | str
            the icon of teaching tip

        image: str | QPixmap | QImage
            the image of teaching tip

        parent: QWidget
            parent widget
        """
        self.icon = icon
        self.title = title
        self.content = content

        self.image = image
        if isinstance(image, str):
            self.image = QImage(image)
        elif isinstance(image, QPixmap):
            self.image = image.toImage()
        elif not self.image:
            self.image = QImage()

        self.originImage = QImage(self.image)

        self.viewLayout = QHBoxLayout(self)
        self.widgetLayout = QVBoxLayout()
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content, self)
        self.iconWidget = IconWidget(icon, self)

        self.__initWidgets()

    def __initWidgets(self):
        self.titleLabel.setVisible(bool(self.title))
        self.contentLabel.setVisible(bool(self.content))
        self.iconWidget.setHidden(self.icon is None)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        FluentStyleSheet.TEACHING_TIP.apply(self)

        self.__initLayout()

    def __initLayout(self):
        self.widgetLayout.setContentsMargins(0, 8, 0, 8)
        self.viewLayout.setSpacing(4)
        self.widgetLayout.setSpacing(0)

        # add icon widget
        if not self.title or not self.content:
            self.iconWidget.setFixedHeight(36)

        self.viewLayout.addWidget(self.iconWidget, 0, Qt.AlignTop)

        # add text
        self._adjustText()
        self.widgetLayout.addWidget(self.titleLabel)
        self.widgetLayout.addWidget(self.contentLabel)
        self.viewLayout.addLayout(self.widgetLayout)

        # adjust content margins
        margins = QMargins(6, 5, 20, 5)
        margins.setLeft(20 if not self.icon else 5)
        self.viewLayout.setContentsMargins(margins)

        self._adjustImage()

    def addWidget(self, widget: QWidget, stretch=0, align=Qt.AlignLeft):
        """ add widget to view """
        self.widgetLayout.addSpacing(8)
        self.widgetLayout.addWidget(widget, stretch, align)

    def _adjustText(self):
        w = min(900, QApplication.screenAt(
            QCursor.pos()).geometry().width() - 200)

        # adjust title
        chars = max(min(w / 10, 120), 30)
        self.titleLabel.setText(TextWrap.wrap(self.title, chars, False)[0])

        # adjust content
        chars = max(min(w / 9, 120), 30)
        self.contentLabel.setText(TextWrap.wrap(self.content, chars, False)[0])

    def _adjustImage(self):
        if self.image.isNull():
            return

        w = self.viewLayout.sizeHint().width() - 2
        self.image = self.originImage.scaledToWidth(w, Qt.SmoothTransformation)

        margins = self.viewLayout.contentsMargins()
        margins.setTop(self.image.height())
        self.viewLayout.setContentsMargins(margins)

    def showEvent(self, e):
        super().showEvent(e)
        self._adjustImage()
        self.adjustSize()

    def paintEvent(self, e):
        super().paintEvent(e)

        if self.image.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        w, h = self.image.width(), self.image.height()
        rect = QRectF(1, 1, w, h)
        path.addRoundedRect(rect, 8, 8)
        path.addRect(QRectF(1, h - 9, w, 10))

        painter.setPen(Qt.NoPen)
        painter.fillPath(path.simplified(), QBrush(self.image))


class Flyout(QWidget):
    """ Flyout """

    def __init__(self, view: FlyoutViewBase, parent=None):
        super().__init__(parent=parent)
        self.view = view
        self.hBoxLayout = QHBoxLayout(self)

        self.opacityAni = QPropertyAnimation(self, b'windowOpacity', self)
        self.slideAni = QPropertyAnimation(self, b'pos', self)
        self.aniGroup = QParallelAnimationGroup(self)

        self.aniGroup.addAnimation(self.opacityAni)
        self.aniGroup.addAnimation(self.slideAni)

        self.hBoxLayout.setContentsMargins(15, 8, 15, 20)
        self.hBoxLayout.addWidget(self.view)
        self.setShadowEffect()

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

    def setShadowEffect(self, blurRadius=35, offset=(0, 8)):
        """ add shadow to dialog """
        color = QColor(0, 0, 0, 80 if isDarkTheme() else 30)
        self.shadowEffect = QGraphicsDropShadowEffect(self.view)
        self.shadowEffect.setBlurRadius(blurRadius)
        self.shadowEffect.setOffset(*offset)
        self.shadowEffect.setColor(color)
        self.view.setGraphicsEffect(None)
        self.view.setGraphicsEffect(self.shadowEffect)

    def exec(self, pos: QPoint, ani=True):
        """ show calendar view """
        rect = QApplication.screenAt(QCursor.pos()).availableGeometry()
        w, h = self.sizeHint().width() + 5, self.sizeHint().height()
        pos.setX(max(rect.left(), min(pos.x(), rect.right() - w)))
        pos.setY(max(rect.top(), min(pos.y() - 4, rect.bottom() - h + 5)))
        self.move(pos)

        if not ani:
            return self.show()

        self.opacityAni.setStartValue(0)
        self.opacityAni.setEndValue(1)
        self.opacityAni.setDuration(187)
        self.opacityAni.setEasingCurve(QEasingCurve.OutQuad)

        self.slideAni.setStartValue(pos+QPoint(0, 8))
        self.slideAni.setEndValue(pos)
        self.slideAni.setDuration(187)
        self.slideAni.setEasingCurve(QEasingCurve.OutQuad)
        self.aniGroup.start()

        self.show()

    @classmethod
    def make(cls, view: FlyoutViewBase, target: Union[QWidget, QPoint] = None, parent=None):
        """ create and show a flyout

        Parameters
        ----------
        view: FlyoutViewBase
            flyout view

        target: QWidget | QPoint
            the target widget or position to show flyout

        parent: QWidget
            parent window
        """
        w = Flyout(view, parent)

        if target is None:
            return w

        # show flyout first so that we can get the correct size
        w.show()

        # move flyout to the top of target
        if isinstance(target, QWidget):
            pos = target.mapToGlobal(QPoint())
            x = pos.x() + target.width()//2 - w.sizeHint().width()//2
            y = pos.y() - w.sizeHint().height() + w.layout().contentsMargins().bottom()
            target = QPoint(x, y)

        w.exec(target)
        return w

    @classmethod
    def create(cls, title: str, content: str, icon: Union[FluentIconBase, QIcon, str] = None,
               image: Union[str, QPixmap, QImage] = None, target: Union[QWidget, QPoint] = None, parent=None):
        """ create and show a flyout using the default view

        Parameters
        ----------
        title: str
            the title of teaching tip

        content: str
            the content of teaching tip

        icon: InfoBarIcon | FluentIconBase | QIcon | str
            the icon of teaching tip

        image: str | QPixmap | QImage
            the image of teaching tip

        view: FlyoutViewBase
            flyout view

        target: QWidget | QPoint
            the target widget or position to show flyout

        parent: QWidget
            parent window
        """
        view = FlyoutView(title, content, icon, image)
        return cls.make(view, target, parent)