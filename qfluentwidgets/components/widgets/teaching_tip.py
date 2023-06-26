# coding:utf-8
from enum import Enum
from typing import Union

from PyQt5.QtCore import Qt, QPoint, QObject, QPointF, QRectF, QSize, QTimer, QPropertyAnimation, QEvent, QMargins
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QIcon, QCursor, QPolygonF, QPixmap, QImage, QBrush
from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QGraphicsDropShadowEffect

from ...common.auto_wrap import TextWrap
from ...common.icon import FluentIconBase, drawIcon, FluentIcon
from ...common.style_sheet import isDarkTheme, FluentStyleSheet
from .button import TransparentToolButton


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


class IconWidget(QWidget):

    def __init__(self, icon, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(36, 54)
        self.icon = icon

    def paintEvent(self, e):
        if not self.icon:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        rect = QRectF(8, (self.height()-20)/2, 20, 20)
        drawIcon(self.icon, painter, rect)


class TeachingTipView(QFrame):
    """ Teaching tip view """

    def __init__(self, title: str, content: str, icon: Union[FluentIconBase, QIcon, str] = None,
                 image: Union[str, QPixmap, QImage] = None, isClosable=True, tailPosition=TeachingTipTailPosition.BOTTOM,
                 parent=None):
        super().__init__(parent=parent)
        self.title = title
        self.content = content
        self.icon = icon
        self.isClosable = isClosable
        self.tailPosition = tailPosition

        self.image = image
        if isinstance(image, str):
            self.image = QImage(image)
        elif isinstance(image, QPixmap):
            self.image = image.toImage()
        elif not self.image:
            self.image = QImage()

        self.originImage = QImage(self.image)

        self.hBoxLayout = QHBoxLayout(self)
        self.viewLayout = QHBoxLayout()
        self.widgetLayout = QVBoxLayout()
        self.manager = TeachingTipManager.make(tailPosition)

        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content, self)
        self.iconWidget = IconWidget(icon, self)
        self.closeButton = TransparentToolButton(FluentIcon.CLOSE, self)

        self.__initWidgets()

    def __initWidgets(self):
        self.closeButton.setFixedSize(32, 32)
        self.closeButton.setIconSize(QSize(12, 12))
        self.closeButton.setVisible(self.isClosable)
        self.titleLabel.setVisible(bool(self.title))
        self.contentLabel.setVisible(bool(self.content))
        self.iconWidget.setHidden(self.icon is None)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        FluentStyleSheet.TEACHING_TIP.apply(self)

        self.__initLayout()

    def __initLayout(self):
        self.manager.doLayout(self)
        self.widgetLayout.setContentsMargins(0, 8, 0, 8)
        self.viewLayout.setSpacing(4)
        self.hBoxLayout.setSpacing(0)
        self.widgetLayout.setSpacing(0)

        self.hBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.viewLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.hBoxLayout.addLayout(self.viewLayout)

        # add icon widget
        if not self.title or not self.content:
            self.iconWidget.setFixedHeight(36)

        self.viewLayout.addWidget(self.iconWidget, 0, Qt.AlignTop)

        # add text
        self._adjustText()
        self.widgetLayout.addWidget(self.titleLabel)
        self.widgetLayout.addWidget(self.contentLabel)
        self.viewLayout.addLayout(self.widgetLayout)

        # add close button
        self.viewLayout.addWidget(
            self.closeButton, 0, Qt.AlignRight | Qt.AlignTop)

        # adjust content margins
        margins = QMargins(6, 5, 6, 5)
        margins.setLeft(20 if not self.icon else 5)
        margins.setRight(20 if not self.isClosable else 6)
        self.viewLayout.setContentsMargins(margins)

        self.adjustImage()

    def adjustImage(self):
        if self.image.isNull():
            return

        w = self.viewLayout.sizeHint().width() - 2
        self.image = self.originImage.scaledToWidth(w, Qt.SmoothTransformation)

        vm = self.manager.viewMargins(self)
        margins = self.viewLayout.contentsMargins()
        margins.setTop(vm.top())
        margins.setBottom(vm.bottom())
        self.viewLayout.setContentsMargins(margins)

    def _adjustText(self):
        w = min(900, QApplication.screenAt(
            QCursor.pos()).geometry().width() - 200)

        # adjust title
        chars = max(min(w / 10, 120), 30)
        self.titleLabel.setText(TextWrap.wrap(self.title, chars, False)[0])

        # adjust content
        chars = max(min(w / 9, 120), 30)
        self.contentLabel.setText(TextWrap.wrap(self.content, chars, False)[0])

        self.adjustSize()

    def showEvent(self, e):
        super().showEvent(e)
        self.adjustImage()
        self.adjustSize()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        painter.setBrush(
            QColor(40, 40, 40) if isDarkTheme() else QColor(249, 249, 249))
        painter.setPen(
            QColor(23, 23, 23) if isDarkTheme() else QColor(195, 195, 195))

        self.manager.draw(self, painter)


class TeachingTip(QWidget):
    """ Teaching tip """

    def __init__(self, target: QWidget, title: str, content: str, icon: Union[FluentIconBase, QIcon, str] = None,
                 image: Union[str, QPixmap, QImage] = None, isClosable=True, duration=1000,
                 tailPosition=TeachingTipTailPosition.BOTTOM, parent=None):
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
        """
        super().__init__(parent=parent)
        self.target = target
        self.duration = duration
        self.manager = TeachingTipManager.make(tailPosition)

        self.hBoxLayout = QHBoxLayout(self)
        self.view = TeachingTipView(
            title, content, icon, image, isClosable, tailPosition, self)
        self.opacityAni = QPropertyAnimation(self, b'windowOpacity', self)

        self.hBoxLayout.setContentsMargins(15, 8, 15, 20)
        self.hBoxLayout.addWidget(self.view)
        self.setShadowEffect()

        # set style
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

        self.view.closeButton.clicked.connect(self._fadeOut)

        if self.parent():
            self.parent().installEventFilter(self)

    def setShadowEffect(self, blurRadius=35, offset=(0, 8)):
        """ add shadow to dialog """
        color = QColor(0, 0, 0, 80 if isDarkTheme() else 30)
        self.shadowEffect = QGraphicsDropShadowEffect(self.view)
        self.shadowEffect.setBlurRadius(blurRadius)
        self.shadowEffect.setOffset(*offset)
        self.shadowEffect.setColor(color)
        self.view.setGraphicsEffect(None)
        self.view.setGraphicsEffect(self.shadowEffect)

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
        self.opacityAni.setDuration(167)
        self.opacityAni.setStartValue(0)
        self.opacityAni.setEndValue(1)
        self.opacityAni.start()
        super().showEvent(e)

    def eventFilter(self, obj, e: QEvent):
        if obj is self.parent():
            if e.type() in [QEvent.Resize, QEvent.WindowStateChange, QEvent.Move]:
                self.move(self.manager.position(self))

        return super().eventFilter(obj, e)

    def addWidget(self, widget: QWidget, stretch=0, align=Qt.AlignLeft):
        """ add widget to teaching tip """
        self.view.widgetLayout.addSpacing(8)
        self.view.widgetLayout.addWidget(widget, stretch, align)

    @staticmethod
    def create(target: QWidget, title: str, content: str, icon: Union[FluentIconBase, QIcon, str] = None,
               image: Union[str, QPixmap, QImage] = None, isClosable=True, duration=1000,
               tailPosition=TeachingTipTailPosition.BOTTOM, parent=None):
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
        """
        w = TeachingTip(target, title, content, icon, image,
                        isClosable, duration, tailPosition, parent)
        w.show()
        return w


class TeachingTipManager(QObject):
    """ Teaching tip manager """

    def __init__(self):
        super().__init__()

    def doLayout(self, tip: TeachingTipView):
        """ manage the layout of tip """
        tip.hBoxLayout.setContentsMargins(0, 0, 0, 0)

    def viewMargins(self, tip: TeachingTipView):
        return QMargins(0, 5 + tip.image.height(), 0, 5)

    def position(self, tip: TeachingTip) -> QPoint:
        pos = self._pos(tip)
        x, y = pos.x(), pos.y()

        rect = QApplication.screenAt(QCursor.pos()).availableGeometry()
        x = min(max(-2, x) if QCursor().pos().x() >=
                0 else x, rect.width() - tip.width() - 4)
        y = min(max(-2, y), rect.height() - tip.height() - 4)

        return QPoint(x, y)

    def draw(self, tip: TeachingTipView, painter: QPainter):
        self._drawShape(tip, painter)
        self._drawImage(tip, painter)

    def _drawShape(self, tip: TeachingTipView, painter: QPainter):
        """ draw the shape of tip """
        # draw border and background
        rect = tip.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 8, 8)

    def _drawImage(self, tip: TeachingTipView, painter: QPainter):
        """ draw the header image of tip """
        if tip.image.isNull():
            return

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        w, h = tip.image.width(), tip.image.height()
        rect = QRectF(1, 1, w, h)
        path.addRoundedRect(rect, 8, 8)
        path.addRect(QRectF(1, h - 9, w, 10))

        painter.setPen(Qt.NoPen)
        painter.fillPath(path.simplified(), QBrush(tip.image))

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

    def doLayout(self, tip: TeachingTip):
        tip.hBoxLayout.setContentsMargins(0, 8, 0, 0)

    def viewMargins(self, tip: TeachingTipView):
        return QMargins(0, 5, 0, 5 + tip.image.height())

    def _drawShape(self, tip, painter):
        # draw border and background
        w, h = tip.width(), tip.height()
        pt = tip.hBoxLayout.contentsMargins().top()

        path = QPainterPath()
        path.addRoundedRect(1, pt, w - 2, h - pt - 1, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(w/2 - 7, pt), QPointF(w/2, 1), QPointF(w/2 + 7, pt)]))

        painter.drawPath(path.simplified())

    def _drawImage(self, tip: TeachingTipView, painter: QPainter):
        """ draw the header image of tip """
        if tip.image.isNull():
            return

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        w, h = tip.image.width(), tip.image.height()
        rect = QRectF(1, 0, w, h)
        path.addRoundedRect(rect, 8, 8)
        path.addRect(QRectF(1, 0, w, 10))

        painter.setPen(Qt.NoPen)
        painter.translate(0, tip.sizeHint().height() - h)
        painter.fillPath(path.simplified(), QBrush(tip.image))

    def _pos(self, tip: TeachingTip):
        target = tip.target
        pos = target.mapToGlobal(QPoint(0, target.height()))
        x = pos.x() + target.width()//2 - tip.sizeHint().width()//2
        y = pos.y() - tip.layout().contentsMargins().top()
        return QPoint(x, y)


class BottomTailTeachingTipManager(TeachingTipManager):
    """ Bottom tail teaching tip manager """

    def doLayout(self, tip: TeachingTip):
        tip.hBoxLayout.setContentsMargins(0, 0, 0, 8)

    def _drawShape(self, tip, painter):
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

    def doLayout(self, tip: TeachingTip):
        tip.hBoxLayout.setContentsMargins(8, 0, 0, 0)

    def _drawShape(self, tip, painter):
        w, h = tip.width(), tip.height()
        pl = 8

        path = QPainterPath()
        path.addRoundedRect(pl, 1, w - pl - 2, h - 2, 8, 8)
        path.addPolygon(
            QPolygonF([QPointF(pl, h/2 - 7), QPointF(1, h/2), QPointF(pl, h/2 + 7)]))

        painter.drawPath(path.simplified())

    def _drawImage(self, tip: TeachingTipView, painter: QPainter):
        """ draw the header image of tip """
        painter.translate(7, 0)
        super()._drawImage(tip, painter)

    def _pos(self, tip: TeachingTip):
        target = tip.target
        m = tip.layout().contentsMargins()
        pos = target.mapToGlobal(QPoint(target.width(), 0))
        x = pos.x() - m.left()
        y = pos.y() - tip.view.sizeHint().height()//2 + target.height()//2 - m.top()
        return QPoint(x, y)


class RightTailTeachingTipManager(TeachingTipManager):
    """ Left tail teaching tip manager """

    def doLayout(self, tip: TeachingTip):
        tip.hBoxLayout.setContentsMargins(0, 0, 8, 0)

    def _drawShape(self, tip, painter):
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

    def _drawShape(self, tip, painter):
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

    def _drawShape(self, tip, painter):
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

    def _drawShape(self, tip, painter):
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

    def _drawShape(self, tip, painter):
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

    def _drawShape(self, tip, painter):
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

    def _drawShape(self, tip, painter):
        w, h = tip.width(), tip.height()
        pl = 8

        path = QPainterPath()
        path.addRoundedRect(pl, 1, w - pl - 2, h - 2, 8, 8)
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

    def _drawShape(self, tip, painter):
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

    def _drawShape(self, tip, painter):
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