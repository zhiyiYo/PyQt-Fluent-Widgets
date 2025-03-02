# coding:utf-8
from enum import Enum
from typing import Union

from PyQt6.QtCore import Qt, QPoint, QObject, QPointF, QTimer, QPropertyAnimation, QEvent
from PyQt6.QtGui import QPainter, QColor, QPainterPath, QIcon, QCursor, QPolygonF, QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QApplication, QGraphicsDropShadowEffect

from ...common.icon import FluentIconBase
from ...common.screen import getCurrentScreenGeometry
from ...common.style_sheet import isDarkTheme
from .flyout import FlyoutView, FlyoutViewBase


class TeachingTipTailPosition(Enum):
    """ Teaching tip tail position """
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    TOP_LEFT = 4
    TOP_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_RIGHT = 7
    LEFT_TOP = 8
    LEFT_BOTTOM = 9
    RIGHT_TOP = 10
    RIGHT_BOTTOM = 11
    NONE = 12


class ImagePosition(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


class TeachingTipView(FlyoutView):
    """ Teaching tip view """

    def __init__(self, title: str, content: str, icon: Union[FluentIconBase, QIcon, str] = None,
                 image: Union[str, QPixmap, QImage] = None, isClosable=True, tailPosition=TeachingTipTailPosition.BOTTOM,
                 parent=None):
        self.manager = TeachingTipManager.make(tailPosition)
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        super().__init__(title, content, icon, image, isClosable, parent)

    def _adjustImage(self):
        if self.manager.imagePosition() in [ImagePosition.TOP, ImagePosition.BOTTOM]:
            return super()._adjustImage()

        h = self.vBoxLayout.sizeHint().height() - 2
        self.imageLabel.scaledToHeight(h)

    def _addImageToLayout(self):
        self.imageLabel.setHidden(self.imageLabel.isNull())
        pos = self.manager.imagePosition()

        if pos == ImagePosition.TOP:
            self.imageLabel.setBorderRadius(8, 8, 0, 0)
            self.vBoxLayout.insertWidget(0, self.imageLabel)
        elif pos == ImagePosition.BOTTOM:
            self.imageLabel.setBorderRadius(0, 0, 8, 8)
            self.vBoxLayout.addWidget(self.imageLabel)
        elif pos == ImagePosition.LEFT:
            self.vBoxLayout.removeItem(self.vBoxLayout.itemAt(0))
            self.hBoxLayout.addLayout(self.viewLayout)
            self.vBoxLayout.addLayout(self.hBoxLayout)

            self.imageLabel.setBorderRadius(8, 0, 8, 0)
            self.hBoxLayout.insertWidget(0, self.imageLabel)
        elif pos == ImagePosition.RIGHT:
            self.vBoxLayout.removeItem(self.vBoxLayout.itemAt(0))
            self.hBoxLayout.addLayout(self.viewLayout)
            self.vBoxLayout.addLayout(self.hBoxLayout)

            self.imageLabel.setBorderRadius(0, 8, 0, 8)
            self.hBoxLayout.addWidget(self.imageLabel)

    def paintEvent(self, e):
        pass


class TeachTipBubble(QWidget):
    """ Teaching tip bubble """

    def __init__(self, view: FlyoutViewBase, tailPosition=TeachingTipTailPosition.BOTTOM, parent=None):
        super().__init__(parent=parent)
        self.manager = TeachingTipManager.make(tailPosition)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = view

        self.manager.doLayout(self)
        self.hBoxLayout.addWidget(self.view)

    def setView(self, view: QWidget):
        self.hBoxLayout.removeWidget(self.view)
        self.view.deleteLater()
        self.view = view
        self.hBoxLayout.addWidget(view)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        painter.setBrush(
            QColor(40, 40, 40) if isDarkTheme() else QColor(248, 248, 248))
        painter.setPen(
            QColor(23, 23, 23) if isDarkTheme() else QColor(0, 0, 0, 17))

        self.manager.draw(self, painter)


class TeachingTip(QWidget):
    """ Teaching tip """

    def __init__(self, view: FlyoutViewBase, target: QWidget, duration=1000,
                 tailPosition=TeachingTipTailPosition.BOTTOM, parent=None, isDeleteOnClose=True):
        """
        Parameters
        ----------
        target: QWidget
            the target widget to show tip

        view: FlyoutViewBase
            teaching tip view

        duration: int
            the time for teaching tip to display in milliseconds. If duration is less than zero,
            teaching tip will never disappear.

        tailPosition: TeachingTipTailPosition
            the position of bubble tail

        parent: QWidget
            parent widget

        isDeleteOnClose: bool
            whether delete flyout automatically when flyout is closed
        """
        super().__init__(parent=parent)
        self.target = target
        self.duration = duration
        self.isDeleteOnClose = isDeleteOnClose
        self.manager = TeachingTipManager.make(tailPosition)

        self.hBoxLayout = QHBoxLayout(self)
        self.opacityAni = QPropertyAnimation(self, b'windowOpacity', self)

        self.bubble = TeachTipBubble(view, tailPosition, self)

        self.hBoxLayout.setContentsMargins(15, 8, 15, 20)
        self.hBoxLayout.addWidget(self.bubble)
        self.setShadowEffect()

        # set style
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)

        if parent and parent.window():
            parent.window().installEventFilter(self)

    def setShadowEffect(self, blurRadius=35, offset=(0, 8)):
        """ add shadow to dialog """
        color = QColor(0, 0, 0, 80 if isDarkTheme() else 30)
        self.shadowEffect = QGraphicsDropShadowEffect(self.bubble)
        self.shadowEffect.setBlurRadius(blurRadius)
        self.shadowEffect.setOffset(*offset)
        self.shadowEffect.setColor(color)
        self.bubble.setGraphicsEffect(None)
        self.bubble.setGraphicsEffect(self.shadowEffect)

    def _fadeOut(self):
        """ fade out """
        self.opacityAni.setDuration(167)
        self.opacityAni.setStartValue(1)
        self.opacityAni.setEndValue(0)
        self.opacityAni.finished.connect(self.close)
        self.opacityAni.start()

    def showEvent(self, e):
        if self.duration >= 0:
            QTimer.singleShot(self.duration, self._fadeOut)

        self.move(self.manager.position(self))
        self.adjustSize()
        self.opacityAni.setDuration(167)
        self.opacityAni.setStartValue(0)
        self.opacityAni.setEndValue(1)
        self.opacityAni.start()
        super().showEvent(e)

    def closeEvent(self, e):
        if self.isDeleteOnClose:
            self.deleteLater()

        super().closeEvent(e)

    def eventFilter(self, obj, e: QEvent):
        if self.parent() and obj is self.parent().window():
            if e.type() in [QEvent.Type.Resize, QEvent.Type.WindowStateChange, QEvent.Type.Move]:
                self.move(self.manager.position(self))

        return super().eventFilter(obj, e)

    def addWidget(self, widget: QWidget, stretch=0, align=Qt.AlignmentFlag.AlignLeft):
        """ add widget to teaching tip """
        self.view.addSpacing(8)
        self.view.addWidget(widget, stretch, align)

    @property
    def view(self):
        return self.bubble.view

    def setView(self, view):
        self.bubble.setView(view)

    @classmethod
    def make(cls, view: FlyoutViewBase, target: QWidget, duration=1000, tailPosition=TeachingTipTailPosition.BOTTOM,
             parent=None, isDeleteOnClose=True):
        """
        Parameters
        ----------
        view: FlyoutViewBase
            teaching tip view

        target: QWidget
            the target widget to show tip

        duration: int
            the time for teaching tip to display in milliseconds. If duration is less than zero,
            teaching tip will never disappear.

        tailPosition: TeachingTipTailPosition
            the position of bubble tail

        parent: QWidget
            parent widget

        isDeleteOnClose: bool
            whether delete flyout automatically when flyout is closed
        """
        w = cls(view, target, duration, tailPosition, parent, isDeleteOnClose)
        w.show()
        return w

    @classmethod
    def create(cls, target: QWidget, title: str, content: str, icon: Union[FluentIconBase, QIcon, str] = None,
               image: Union[str, QPixmap, QImage] = None, isClosable=True, duration=1000,
               tailPosition=TeachingTipTailPosition.BOTTOM, parent=None, isDeleteOnClose=True):
        """
        Parameters
        ----------
        target: QWidget
            the target widget to show tip

        title: str
            the title of teaching tip

        content: str
            the content of teaching tip

        icon: InfoBarIcon | FluentIconBase | QIcon | str
            the icon of teaching tip

        image: str | QPixmap | QImage
            the image of teaching tip

        isClosable: bool
            whether to show the close button

        duraction: int
            the time for teaching tip to display in milliseconds. If duration is less than zero,
            teaching tip will never disappear.

        parent: QWidget
            parent widget

        isDeleteOnClose: bool
            whether delete flyout automatically when flyout is closed
        """
        view = TeachingTipView(title, content, icon, image, isClosable, tailPosition)
        w = cls.make(view, target, duration, tailPosition, parent, isDeleteOnClose)
        view.closed.connect(w.close)
        return w


class PopupTeachingTip(TeachingTip):
    """ Pop up teaching tip """

    def __init__(self, view: FlyoutViewBase, target: QWidget, duration=1000,
                 tailPosition=TeachingTipTailPosition.BOTTOM, parent=None, isDeleteOnClose=True):
        super().__init__(view, target, duration, tailPosition, parent, isDeleteOnClose)
        self.setWindowFlags(Qt.WindowType.Popup |
                            Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.NoDropShadowWindowHint)


class TeachingTipManager(QObject):
    """ Teaching tip manager """

    def __init__(self):
        super().__init__()

    def doLayout(self, tip: TeachTipBubble):
        """ manage the layout of tip """
        tip.hBoxLayout.setContentsMargins(0, 0, 0, 0)

    def imagePosition(self):
        return ImagePosition.TOP

    def position(self, tip: TeachingTip) -> QPoint:
        pos = self._pos(tip)
        x, y = pos.x(), pos.y()

        rect = getCurrentScreenGeometry()
        x = max(rect.left(), min(pos.x(), rect.right() - tip.width() - 4))
        y = max(rect.top(), min(pos.y(), rect.bottom() - tip.height() - 4))

        return QPoint(x, y)

    def draw(self, tip: TeachTipBubble, painter: QPainter):
        """ draw the shape of bubble """
        rect = tip.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 8, 8)

    def _pos(self, tip: TeachingTip):
        """ return the poisition of tip """
        return tip.pos()

    @staticmethod
    def make(position: TeachingTipTailPosition):
        """ mask teaching tip manager according to the display position """
        managers = {
            TeachingTipTailPosition.TOP: TopTailTeachingTipManager,
            TeachingTipTailPosition.BOTTOM: BottomTailTeachingTipManager,
            TeachingTipTailPosition.LEFT: LeftTailTeachingTipManager,
            TeachingTipTailPosition.RIGHT: RightTailTeachingTipManager,
            TeachingTipTailPosition.TOP_RIGHT: TopRightTailTeachingTipManager,
            TeachingTipTailPosition.BOTTOM_RIGHT: BottomRightTailTeachingTipManager,
            TeachingTipTailPosition.TOP_LEFT: TopLeftTailTeachingTipManager,
            TeachingTipTailPosition.BOTTOM_LEFT: BottomLeftTailTeachingTipManager,
            TeachingTipTailPosition.LEFT_TOP: LeftTopTailTeachingTipManager,
            TeachingTipTailPosition.LEFT_BOTTOM: LeftBottomTailTeachingTipManager,
            TeachingTipTailPosition.RIGHT_TOP: RightTopTailTeachingTipManager,
            TeachingTipTailPosition.RIGHT_BOTTOM: RightBottomTailTeachingTipManager,
            TeachingTipTailPosition.NONE: TeachingTipManager,
        }

        if position not in managers:
            raise ValueError(
                f'`{position}` is an invalid teaching tip position.')

        return managers[position]()


class TopTailTeachingTipManager(TeachingTipManager):
    """ Top tail teaching tip manager """

    def doLayout(self, tip):
        tip.hBoxLayout.setContentsMargins(0, 8, 0, 0)

    def imagePosition(self):
        return ImagePosition.BOTTOM

    def draw(self, tip, painter):
        w, h = tip.width(), tip.height()
        pt = tip.hBoxLayout.contentsMargins().top()

        path = QPainterPath()
        path.addRoundedRect(1, pt, w - 2, h - pt - 1, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(w/2 - 7, pt), QPointF(w/2, 1), QPointF(w/2 + 7, pt)]))

        painter.drawPath(path.simplified())

    def _pos(self, tip: TeachingTip):
        target = tip.target
        pos = target.mapToGlobal(QPoint(0, target.height()))
        x = pos.x() + target.width()//2 - tip.sizeHint().width()//2
        y = pos.y() - tip.layout().contentsMargins().top()
        return QPoint(x, y)


class BottomTailTeachingTipManager(TeachingTipManager):
    """ Bottom tail teaching tip manager """

    def doLayout(self, tip):
        tip.hBoxLayout.setContentsMargins(0, 0, 0, 8)

    def draw(self, tip, painter):
        w, h = tip.width(), tip.height()
        pb = tip.hBoxLayout.contentsMargins().bottom()

        path = QPainterPath()
        path.addRoundedRect(1, 1, w - 2, h - pb - 1, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(w/2 - 7, h - pb), QPointF(w/2, h - 1), QPointF(w/2 + 7, h - pb)]))

        painter.drawPath(path.simplified())

    def _pos(self, tip: TeachingTip):
        target = tip.target
        pos = target.mapToGlobal(QPoint())
        x = pos.x() + target.width()//2 - tip.sizeHint().width()//2
        y = pos.y() - tip.sizeHint().height() + tip.layout().contentsMargins().bottom()
        return QPoint(x, y)


class LeftTailTeachingTipManager(TeachingTipManager):
    """ Left tail teaching tip manager """

    def doLayout(self, tip):
        tip.hBoxLayout.setContentsMargins(8, 0, 0, 0)

    def imagePosition(self):
        return ImagePosition.RIGHT

    def draw(self, tip, painter):
        w, h = tip.width(), tip.height()
        pl = 8

        path = QPainterPath()
        path.addRoundedRect(pl, 1, w - pl - 2, h - 2, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(pl, h/2 - 7), QPointF(1, h/2), QPointF(pl, h/2 + 7)]))

        painter.drawPath(path.simplified())

    def _pos(self, tip: TeachingTip):
        target = tip.target
        m = tip.layout().contentsMargins()
        pos = target.mapToGlobal(QPoint(target.width(), 0))
        x = pos.x() - m.left()
        y = pos.y() - tip.view.sizeHint().height()//2 + target.height()//2 - m.top()
        return QPoint(x, y)


class RightTailTeachingTipManager(TeachingTipManager):
    """ Left tail teaching tip manager """

    def doLayout(self, tip):
        tip.hBoxLayout.setContentsMargins(0, 0, 8, 0)

    def imagePosition(self):
        return ImagePosition.LEFT

    def draw(self, tip, painter):
        w, h = tip.width(), tip.height()
        pr = 8

        path = QPainterPath()
        path.addRoundedRect(1, 1, w - pr - 1, h - 2, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(w - pr, h/2 - 7), QPointF(w - 1, h/2), QPointF(w - pr, h/2 + 7)]))

        painter.drawPath(path.simplified())

    def _pos(self, tip: TeachingTip):
        target = tip.target
        m = tip.layout().contentsMargins()
        pos = target.mapToGlobal(QPoint(0, 0))
        x = pos.x() - tip.sizeHint().width() + m.right()
        y = pos.y() - tip.view.sizeHint().height()//2 + target.height()//2 - m.top()
        return QPoint(x, y)


class TopLeftTailTeachingTipManager(TopTailTeachingTipManager):
    """ Top left tail teaching tip manager """

    def draw(self, tip, painter):
        w, h = tip.width(), tip.height()
        pt = tip.hBoxLayout.contentsMargins().top()

        path = QPainterPath()
        path.addRoundedRect(1, pt, w - 2, h - pt - 1, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(20, pt), QPointF(27, 1), QPointF(34, pt)]))

        painter.drawPath(path.simplified())

    def _pos(self, tip: TeachingTip):
        target = tip.target
        pos = target.mapToGlobal(QPoint(0, target.height()))
        x = pos.x() - tip.layout().contentsMargins().left()
        y = pos.y() - tip.layout().contentsMargins().top()
        return QPoint(x, y)


class TopRightTailTeachingTipManager(TopTailTeachingTipManager):
    """ Top right tail teaching tip manager """

    def draw(self, tip, painter):
        w, h = tip.width(), tip.height()
        pt = tip.hBoxLayout.contentsMargins().top()

        path = QPainterPath()
        path.addRoundedRect(1, pt, w - 2, h - pt - 1, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(w - 20, pt), QPointF(w - 27, 1), QPointF(w - 34, pt)]))

        painter.drawPath(path.simplified())

    def _pos(self, tip: TeachingTip):
        target = tip.target
        pos = target.mapToGlobal(QPoint(target.width(), target.height()))
        x = pos.x() - tip.sizeHint().width() + tip.layout().contentsMargins().left()
        y = pos.y() - tip.layout().contentsMargins().top()
        return QPoint(x, y)


class BottomLeftTailTeachingTipManager(BottomTailTeachingTipManager):
    """ Bottom left tail teaching tip manager """

    def draw(self, tip, painter):
        w, h = tip.width(), tip.height()
        pb = tip.hBoxLayout.contentsMargins().bottom()

        path = QPainterPath()
        path.addRoundedRect(1, 1, w - 2, h - pb - 1, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(20, h - pb), QPointF(27, h - 1), QPointF(34, h - pb)]))

        painter.drawPath(path.simplified())

    def _pos(self, tip: TeachingTip):
        target = tip.target
        pos = target.mapToGlobal(QPoint())
        x = pos.x() - tip.layout().contentsMargins().left()
        y = pos.y() - tip.sizeHint().height() + tip.layout().contentsMargins().bottom()
        return QPoint(x, y)


class BottomRightTailTeachingTipManager(BottomTailTeachingTipManager):
    """ Bottom right tail teaching tip manager """

    def draw(self, tip, painter):
        w, h = tip.width(), tip.height()
        pb = tip.hBoxLayout.contentsMargins().bottom()

        path = QPainterPath()
        path.addRoundedRect(1, 1, w - 2, h - pb - 1, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(w - 20, h - pb), QPointF(w - 27, h - 1), QPointF(w - 34, h - pb)]))

        painter.drawPath(path.simplified())

    def _pos(self, tip: TeachingTip):
        target = tip.target
        pos = target.mapToGlobal(QPoint(target.width(), 0))
        x = pos.x() - tip.sizeHint().width() + tip.layout().contentsMargins().left()
        y = pos.y() - tip.sizeHint().height() + tip.layout().contentsMargins().bottom()
        return QPoint(x, y)


class LeftTopTailTeachingTipManager(LeftTailTeachingTipManager):
    """ Left top tail teaching tip manager """

    def imagePosition(self):
        return ImagePosition.BOTTOM

    def draw(self, tip, painter):
        w, h = tip.width(), tip.height()
        pl = 8

        path = QPainterPath()
        path.addRoundedRect(pl, 1, w - pl - 2, h - 2, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(pl, 10), QPointF(1, 17), QPointF(pl, 24)]))

        painter.drawPath(path.simplified())

    def _pos(self, tip: TeachingTip):
        target = tip.target
        m = tip.layout().contentsMargins()
        pos = target.mapToGlobal(QPoint(target.width(), 0))
        x = pos.x() - m.left()
        y = pos.y() - m.top()
        return QPoint(x, y)


class LeftBottomTailTeachingTipManager(LeftTailTeachingTipManager):
    """ Left bottom tail teaching tip manager """

    def imagePosition(self):
        return ImagePosition.TOP

    def draw(self, tip, painter):
        w, h = tip.width(), tip.height()
        pl = 9

        path = QPainterPath()
        path.addRoundedRect(pl, 1, w - pl - 1, h - 2, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(pl, h - 10), QPointF(1, h - 17), QPointF(pl, h - 24)]))

        painter.drawPath(path.simplified())

    def _pos(self, tip: TeachingTip):
        target = tip.target
        m = tip.layout().contentsMargins()
        pos = target.mapToGlobal(QPoint(target.width(), target.height()))
        x = pos.x() - m.left()
        y = pos.y() - tip.sizeHint().height() + m.bottom()
        return QPoint(x, y)


class RightTopTailTeachingTipManager(RightTailTeachingTipManager):
    """ Right top tail teaching tip manager """

    def imagePosition(self):
        return ImagePosition.BOTTOM

    def draw(self, tip, painter):
        w, h = tip.width(), tip.height()
        pr = 8

        path = QPainterPath()
        path.addRoundedRect(1, 1, w - pr - 1, h - 2, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(w - pr, 10), QPointF(w - 1, 17), QPointF(w - pr, 24)]))

        painter.drawPath(path.simplified())

    def _pos(self, tip: TeachingTip):
        target = tip.target
        m = tip.layout().contentsMargins()
        pos = target.mapToGlobal(QPoint(0, 0))
        x = pos.x() - tip.sizeHint().width() + m.right()
        y = pos.y() - m.top()
        return QPoint(x, y)


class RightBottomTailTeachingTipManager(RightTailTeachingTipManager):
    """ Right bottom tail teaching tip manager """

    def imagePosition(self):
        return ImagePosition.TOP

    def draw(self, tip, painter):
        w, h = tip.width(), tip.height()
        pr = 8

        path = QPainterPath()
        path.addRoundedRect(1, 1, w - pr - 1, h - 2, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(w - pr, h-10), QPointF(w - 1, h-17), QPointF(w - pr, h-24)]))

        painter.drawPath(path.simplified())

    def _pos(self, tip: TeachingTip):
        target = tip.target
        m = tip.layout().contentsMargins()
        pos = target.mapToGlobal(QPoint(0, target.height()))
        x = pos.x() - tip.sizeHint().width() + m.right()
        y = pos.y() - tip.sizeHint().height() + m.bottom()
        return QPoint(x, y)
