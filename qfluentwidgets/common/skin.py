# coding: utf-8
""" reusable color schemes of the fluent widgets """
from abc import ABC
from typing import Dict, List, Optional, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from .config import Theme, qconfig
from .style_sheet import setSurfaceTint, setTheme, setThemeColor
from .tint import blendColor


class FluentSkin:
    """ A complete color scheme of the fluent widgets

    A skin bundles every knob that controls the colors of the application:

    =========================  =============================================
    attribute                  effect
    =========================  =============================================
    ``theme``                  light/dark base theme, see `setTheme`
    ``accentColor``            accent color, see `setThemeColor`
    ``surfaceTint``            tint color of surfaces, see `setSurfaceTint`
    ``surfaceTintStrength``    blend strength of the tint, `0` disables it
    ``lightWindowBackground``  window background color in light mode
    ``darkWindowBackground``   window background color in dark mode
    =========================  =============================================

    The accent color and the surface tint are two independent axes: the
    accent color paints the interactive contents (buttons, sliders, checks…)
    while the surface tint only shifts the near-neutral backgrounds and
    borders of the surfaces (cards, menus, flyouts, navigation…).

    The ready-made skins live in `FluentSkinSet`, they are registered to this
    class as soon as the module is imported.

    Examples
    --------
    Create a skin and apply it to the whole application:

    >>> skin = FluentSkin('Deep ocean', Theme.DARK, '#4CC2FF', '#12304E', 0.28)
    >>> skin.apply(window)

    Derive a new skin from an existing one:

    >>> warmer = skin.copy(name='Warmer ocean', surfaceTint='#4E2A12')

    Extend the class with your own color roles:

    >>> class BrandSkin(FluentSkin):
    ...     def __init__(self, name='Brand', theme=Theme.LIGHT, **kwargs):
    ...         kwargs.setdefault('accentColor', '#005FB8')
    ...         super().__init__(name, theme, **kwargs)
    ...         self.logoColor = QColor('#005FB8')
    ...
    ...     def apply(self, window=None, save=False, lazy=False):
    ...         super().apply(window, save, lazy)
    ...         # apply the extra roles here
    """

    #: attributes restored by `copy`, subclasses extending it must accept the
    #: new names as keyword arguments of `__init__`
    _FIELDS = ('name', 'theme', 'accentColor', 'surfaceTint', 'surfaceTintStrength',
               'lightWindowBackground', 'darkWindowBackground')

    #: base background color of the surfaces declared by the style sheet
    LIGHT_SURFACE = QColor(249, 249, 249)
    DARK_SURFACE = QColor(43, 43, 43)

    #: global preset registry shared by the whole application
    _presets: Dict[str, 'FluentSkin'] = {}

    def __init__(self, name: str = 'Custom',
                 theme: Theme = Theme.LIGHT,
                 accentColor: Union[str, QColor, Qt.GlobalColor] = '#009faa',
                 surfaceTint: Optional[Union[str, QColor, Qt.GlobalColor]] = None,
                 surfaceTintStrength: float = 0.28,
                 lightWindowBackground: Union[str, QColor, Qt.GlobalColor] = '#f0f4f9',
                 darkWindowBackground: Union[str, QColor, Qt.GlobalColor] = '#202020'):
        """
        Parameters
        ----------
        name: str
            the name of the skin, it's the key of the preset registry

        theme: Theme | str
            the base theme, `Theme.AUTO` follows the system theme

        accentColor: QColor | Qt.GlobalColor | str
            the accent color of the interactive contents

        surfaceTint: QColor | Qt.GlobalColor | str
            the tint color of surfaces, `None` disables the surface tint

        surfaceTintStrength: float
            the blend strength of the surface tint, ranging from 0 to 1

        lightWindowBackground, darkWindowBackground: QColor | Qt.GlobalColor | str
            the base background color of the fluent window, they are tinted
            by `surfaceTint` as well
        """
        if isinstance(theme, str):
            theme = Theme(theme)

        self.name = name
        self.theme = theme
        self.accentColor = QColor(accentColor)
        self.surfaceTint = QColor() if surfaceTint is None else QColor(surfaceTint)
        self.surfaceTintStrength = max(0, min(float(surfaceTintStrength), 1))
        self.lightWindowBackground = QColor(lightWindowBackground)
        self.darkWindowBackground = QColor(darkWindowBackground)

    @property
    def isTintEnabled(self) -> bool:
        """ whether the surface tint is enabled, it requires a valid tint
        color and a positive strength """
        return self.surfaceTint.isValid() and self.surfaceTintStrength > 0

    def _resolveTheme(self, theme: Optional[Theme]) -> Theme:
        """ resolve the given theme, `None` and `Theme.AUTO` are replaced by a
        concrete light/dark theme """
        theme = self.theme if theme is None else theme
        return qconfig.theme if theme == Theme.AUTO else theme

    def windowBackgroundColor(self, theme: Optional[Theme] = None) -> QColor:
        """ get the tinted background color of the fluent window

        The window paints its own background instead of reading it from the
        style sheet, so it must be tinted by hand.

        Parameters
        ----------
        theme: Theme
            the theme mode to get the background color, `None` means the
            theme of this skin, `Theme.AUTO` resolves to the current theme

        Returns
        -------
        color: QColor
            the tinted background color
        """
        theme = self._resolveTheme(theme)
        color = self.darkWindowBackground if theme == Theme.DARK else self.lightWindowBackground
        if not self.isTintEnabled:
            return QColor(color)

        return blendColor(color, self.surfaceTint, self.surfaceTintStrength)

    def surfaceColor(self, theme: Optional[Theme] = None) -> QColor:
        """ get the tinted background color of the surfaces, i.e. the color of
        the cards, menus, flyouts and navigation items

        It's handy to draw a preview of the skin, see the skin demo example.

        Parameters
        ----------
        theme: Theme
            the theme mode to get the surface color, `None` means the theme of
            this skin, `Theme.AUTO` resolves to the current theme

        Returns
        -------
        color: QColor
            the tinted surface color
        """
        theme = self._resolveTheme(theme)
        color = self.DARK_SURFACE if theme == Theme.DARK else self.LIGHT_SURFACE
        if not self.isTintEnabled:
            return QColor(color)

        return blendColor(color, self.surfaceTint, self.surfaceTintStrength)

    def apply(self, window=None, save=False, lazy=False):
        """ apply the skin to the whole application

        Parameters
        ----------
        window: FluentWidget
            the fluent window to repaint the background of, `None` means the
            background of the windows is left untouched

        save: bool
            whether to save the change to config file

        lazy: bool
            whether to update the style sheet lazily, set to `True` will
            accelerate the skin switching
        """
        setTheme(self.theme, save=False, lazy=lazy)
        setThemeColor(self.accentColor, save=False, lazy=lazy)
        setSurfaceTint(self.surfaceTint, self.surfaceTintStrength, lazy=lazy, save=False)

        if window is not None:
            window.setCustomBackgroundColor(
                self.windowBackgroundColor(Theme.LIGHT),
                self.windowBackgroundColor(Theme.DARK))

        if save:
            qconfig.save()

    def copy(self, **changes) -> 'FluentSkin':
        """ create a new skin with some attributes replaced

        Parameters
        ----------
        changes:
            the attributes to replace, the others are copied from this skin

        Returns
        -------
        skin: FluentSkin
            a new skin of the same class
        """
        values = {name: getattr(self, name) for name in self._FIELDS}
        values.update(changes)
        return type(self)(**values)

    def toDict(self) -> dict:
        """ convert the skin into a `dict` that can be stored in a json file """
        return {
            'name': self.name,
            'theme': self.theme.value,
            'accentColor': self.accentColor.name(),
            'surfaceTint': self.surfaceTint.name() if self.surfaceTint.isValid() else None,
            'surfaceTintStrength': self.surfaceTintStrength,
            'lightWindowBackground': self.lightWindowBackground.name(),
            'darkWindowBackground': self.darkWindowBackground.name(),
        }

    @classmethod
    def fromDict(cls, data: dict) -> 'FluentSkin':
        """ create a skin from the `dict` generated by `toDict` """
        return cls(**data)

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return NotImplemented

        return all(getattr(self, name) == getattr(other, name) for name in self._FIELDS)

    def __repr__(self) -> str:
        tint = self.surfaceTint.name() if self.surfaceTint.isValid() else None
        return (f'{self.__class__.__name__}(name={self.name!r}, theme={self.theme}, '
                f'accentColor={self.accentColor.name()!r}, surfaceTint={tint!r}, '
                f'surfaceTintStrength={self.surfaceTintStrength!r})')

    @classmethod
    def register(cls, *skins: 'FluentSkin'):
        """ add skins to the global preset registry

        Registering a skin with an existing name replaces the old one, which
        makes it possible to override a preset shipped by a library or a plugin.

        Parameters
        ----------
        skins: FluentSkin
            the skins to register
        """
        for skin in skins:
            if not isinstance(skin, FluentSkin):
                raise TypeError(f'expected a FluentSkin, but got {type(skin).__name__}')

            cls._presets[skin.name] = skin

    @classmethod
    def unregister(cls, *names: str):
        """ remove the skins with the given names from the preset registry """
        for name in names:
            cls._presets.pop(name, None)

    @classmethod
    def presets(cls) -> Dict[str, 'FluentSkin']:
        """ get a copy of the preset registry, the insertion order is kept """
        return dict(cls._presets)

    @classmethod
    def get(cls, name: str, default=None) -> Optional['FluentSkin']:
        """ get the registered skin by name, `default` is returned when the
        name is unknown """
        return cls._presets.get(name, default)


class FluentSkinSetBase(ABC):
    """ Abstract base class of a group of skins

    It declares no skin, it only knows how to collect the `FluentSkin` class
    attributes declared by a subclass, keeping the declaration order. Subclass
    it to group your own skins, `skins()` then returns exactly what you wrote:

    >>> class BrandSkins(FluentSkinSetBase):
    ...     DARK = FluentSkin('Brand dark', Theme.DARK, '#005FB8', '#0E2A47', 0.3)
    ...     LIGHT = FluentSkin('Brand light', Theme.LIGHT, '#005FB8', '#EAF3FB', 0.2)
    >>> [skin.name for skin in BrandSkins.skins()]
    ['Brand dark', 'Brand light']

    `FluentSkinSet` is a subclass of this class, so inheriting from *it* brings
    the 32 built-in presets along. Inherit from this class instead when you
    only want your own skins.

    Examples
    --------
    Register the skins of a set in one call, so that `FluentSkin.get()` can
    find them by name:

    >>> BrandSkins.register()
    >>> FluentSkin.get('Brand light').apply(window)
    """

    @classmethod
    def skins(cls) -> List['FluentSkin']:
        """ get all the skins of this set, the declaration order is kept

        The skins of the base classes come first, redeclaring a name in a
        subclass overrides the skin of the base class.
        """
        skins = {}
        for klass in reversed(cls.__mro__):
            for skin in vars(klass).values():
                if isinstance(skin, FluentSkin):
                    skins[skin.name] = skin

        return list(skins.values())

    @classmethod
    def register(cls):
        """ register all the skins of this set to the preset registry """
        FluentSkin.register(*cls.skins())


class FluentSkinSet(FluentSkinSetBase):
    """ The built-in skins

    They are registered to `FluentSkin` as soon as this module is imported,
    so they can be fetched by name as well.

    Examples
    --------
    Use a built-in skin:

    >>> FluentSkinSet.DEEP_OCEAN.apply(window)
    >>> FluentSkin.get('Celadon').apply(window)
    """

    DEFAULT_LIGHT = FluentSkin('Default light', Theme.LIGHT, '#009faa')
    DEFAULT_DARK = FluentSkin('Default dark', Theme.DARK, '#009faa')
    DARK_GOLD = FluentSkin('Dark gold', Theme.DARK, '#D4AF37', '#3A2D12', 0.28)
    DEEP_OCEAN = FluentSkin('Deep ocean', Theme.DARK, '#4CC2FF', '#12304E', 0.28)
    PAPER_INK = FluentSkin('Paper ink', Theme.LIGHT, '#7A5C2E', '#F2E8D5', 0.20)
    CELADON = FluentSkin('Celadon', Theme.LIGHT, '#2F7D6C', '#E7F2EC', 0.22)

    # The skins below come from the Material 3 dynamic color algorithm
    # (material-color-utilities, spec 2021), one light/dark pair per scheme.
    # A scheme is more than an accent color: its neutral palette carries a bit
    # of the primary hue, so `surfaceTint` is the M3 surface container tone
    # (the color of cards and menus) and the window background is the M3
    # surface tone. The light backgrounds sit halfway to the surface dim tone,
    # otherwise the cards would be lighter than the window and lose their edge.
    #   baseline    -> tonal spot,  seed #6750A4
    #   vibrant     -> vibrant,     seed #8B5000
    #   expressive  -> expressive,  seed #7D5260
    #   fidelity    -> fidelity,    seed #006A6A
    #   fruit salad -> fruit salad, seed #386A20
    #   monochrome  -> monochrome,  seed #6750A4
    #   content     -> content,     seed #B3261E
    #   neutral     -> neutral,     seed #386A20
    #   rainbow     -> rainbow,     seed #00639B
    # The nine scheme styles of Material 3 are all covered here, the seed
    # color only decides the hue, the style decides how the hue spreads over
    # the neutral surfaces.
    BASELINE_LIGHT = FluentSkin(
        'Baseline', Theme.LIGHT, '#65558f', '#f2ecf4', 0.45,
        lightWindowBackground='#eee8f0', darkWindowBackground='#141218')
    BASELINE_DARK = FluentSkin(
        'Baseline dark', Theme.DARK, '#cfbdfe', '#211f24', 0.45,
        lightWindowBackground='#eee8f0', darkWindowBackground='#141218')

    VIBRANT_LIGHT = FluentSkin(
        'Vibrant', Theme.LIGHT, '#8b5000', '#ffeada', 0.45,
        lightWindowBackground='#f6e7dd', darkWindowBackground='#1c1107')
    VIBRANT_DARK = FluentSkin(
        'Vibrant dark', Theme.DARK, '#ffb871', '#291d12', 0.45,
        lightWindowBackground='#f6e7dd', darkWindowBackground='#1c1107')

    EXPRESSIVE_LIGHT = FluentSkin(
        'Expressive', Theme.LIGHT, '#07658e', '#ffe9e9', 0.45,
        lightWindowBackground='#f5e7e6', darkWindowBackground='#1c1011')
    EXPRESSIVE_DARK = FluentSkin(
        'Expressive dark', Theme.DARK, '#89cefc', '#291c1d', 0.45,
        lightWindowBackground='#f5e7e6', darkWindowBackground='#1c1011')

    FIDELITY_LIGHT = FluentSkin(
        'Fidelity', Theme.LIGHT, '#005050', '#ebeeee', 0.45,
        lightWindowBackground='#e7ebea', darkWindowBackground='#101414')
    FIDELITY_DARK = FluentSkin(
        'Fidelity dark', Theme.DARK, '#84d4d3', '#1c2020', 0.45,
        lightWindowBackground='#e7ebea', darkWindowBackground='#101414')

    FRUIT_SALAD_LIGHT = FluentSkin(
        'Fruit salad', Theme.LIGHT, '#775a00', '#e9f0df', 0.45,
        lightWindowBackground='#e5eddb', darkWindowBackground='#0f150b')
    FRUIT_SALAD_DARK = FluentSkin(
        'Fruit salad dark', Theme.DARK, '#efc148', '#1b2117', 0.45,
        lightWindowBackground='#e5eddb', darkWindowBackground='#0f150b')

    MONOCHROME_LIGHT = FluentSkin(
        'Monochrome', Theme.LIGHT, '#000000', '#eeeeee', 0.45,
        lightWindowBackground='#eaeaea', darkWindowBackground='#131313')
    MONOCHROME_DARK = FluentSkin(
        'Monochrome dark', Theme.DARK, '#ffffff', '#1f1f1f', 0.45,
        lightWindowBackground='#eaeaea', darkWindowBackground='#131313')

    CONTENT_LIGHT = FluentSkin(
        'Content', Theme.LIGHT, '#900708', '#ffe9e6', 0.45,
        lightWindowBackground='#f7e6e3', darkWindowBackground='#1d100e')
    CONTENT_DARK = FluentSkin(
        'Content dark', Theme.DARK, '#ffb4aa', '#2b1c1a', 0.45,
        lightWindowBackground='#f7e6e3', darkWindowBackground='#1d100e')

    NEUTRAL_LIGHT = FluentSkin(
        'Neutral', Theme.LIGHT, '#586151', '#f0eeea', 0.45,
        lightWindowBackground='#ebe9e5', darkWindowBackground='#131412')
    NEUTRAL_DARK = FluentSkin(
        'Neutral dark', Theme.DARK, '#c0cab6', '#1f201e', 0.45,
        lightWindowBackground='#ebe9e5', darkWindowBackground='#131412')

    RAINBOW_LIGHT = FluentSkin(
        'Rainbow', Theme.LIGHT, '#00639b', '#eeeeee', 0.45,
        lightWindowBackground='#e9e9e9', darkWindowBackground='#131313')
    RAINBOW_DARK = FluentSkin(
        'Rainbow dark', Theme.DARK, '#96cbff', '#1f1f1f', 0.45,
        lightWindowBackground='#e9e9e9', darkWindowBackground='#131313')

    # The skins below borrow the palettes of the classic code editors, so the
    # colors are already familiar to most developers. Only the roles that map
    # to the fluent widgets are used:
    #   accentColor  -> the editor accent (blue, mauve, orange…)
    #   surfaceTint  -> the panel color of the palette (the container tone)
    #   window       -> the editor background, it's darker than the panel in
    #                   the dark skins and lighter than the card in the light
    #                   ones, otherwise the cards would sink into the window
    #   Nord       -> nord0 #2E3440 / nord4 #D8DEE9, frost #88C0D0 / #5E81AC
    #   Solarized  -> base03 #002B36 / base2 #EEE8D5, blue #268BD2, cyan #2AA198
    #   Catppuccin -> mocha #1E1E2E / latte #EFF1F5, mauve #CBA6F7 / #8839EF
    #   Dracula    -> background #282A36, purple #BD93F9
    #   Gruvbox    -> bg #282828, yellow #FABD2F
    NORD_LIGHT = FluentSkin(
        'Nord light', Theme.LIGHT, '#5e81ac', '#d8dee9', 0.45,
        lightWindowBackground='#e5e9f0', darkWindowBackground='#12161c')
    NORD_DARK = FluentSkin(
        'Nord dark', Theme.DARK, '#88c0d0', '#2e3440', 0.45,
        lightWindowBackground='#e5e9f0', darkWindowBackground='#12161c')

    SOLARIZED_LIGHT = FluentSkin(
        'Solarized light', Theme.LIGHT, '#268bd2', '#eee8d5', 0.50,
        lightWindowBackground='#e6dfc9', darkWindowBackground='#001820')
    SOLARIZED_DARK = FluentSkin(
        'Solarized dark', Theme.DARK, '#2aa198', '#073642', 0.45,
        lightWindowBackground='#e6dfc9', darkWindowBackground='#001820')

    CATPPUCCIN_LATTE = FluentSkin(
        'Catppuccin latte', Theme.LIGHT, '#8839ef', '#e6e9ef', 0.50,
        lightWindowBackground='#dce0e8', darkWindowBackground='#11111b')
    CATPPUCCIN_MOCHA = FluentSkin(
        'Catppuccin mocha', Theme.DARK, '#cba6f7', '#313244', 0.45,
        lightWindowBackground='#dce0e8', darkWindowBackground='#11111b')

    DRACULA_DARK = FluentSkin(
        'Dracula dark', Theme.DARK, '#bd93f9', '#44475a', 0.45,
        lightWindowBackground='#e9e9f2', darkWindowBackground='#191a21')
    GRUVBOX_DARK = FluentSkin(
        'Gruvbox dark', Theme.DARK, '#fabd2f', '#3c3836', 0.45,
        lightWindowBackground='#e8dcb5', darkWindowBackground='#141617')


FluentSkinSet.register()
