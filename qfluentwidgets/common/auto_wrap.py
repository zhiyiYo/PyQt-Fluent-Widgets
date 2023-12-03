from enum import Enum, auto
from functools import lru_cache
from re import sub
from typing import List, Optional, Tuple
from unicodedata import east_asian_width


class CharType(Enum):
    SPACE = auto()
    ASIAN = auto()
    LATIN = auto()


class TextWrap:
    """Text wrap"""

    EAST_ASAIN_WIDTH_TABLE = {
        "F": 2,
        "H": 1,
        "W": 2,
        "A": 1,
        "N": 1,
        "Na": 1,
    }

    @classmethod
    @lru_cache(maxsize=128)
    def get_width(cls, char: str) -> int:
        """Returns the width of the char"""
        return cls.EAST_ASAIN_WIDTH_TABLE.get(east_asian_width(char), 1)

    @classmethod
    @lru_cache(maxsize=32)
    def get_text_width(cls, text: str) -> int:
        """Returns the width of the text"""
        return sum(cls.get_width(char) for char in text)

    @classmethod
    @lru_cache(maxsize=128)
    def get_char_type(cls, char: str) -> CharType:
        """Returns the type of the char"""

        if char.isspace():
            return CharType.SPACE

        if cls.get_width(char) == 1:
            return CharType.LATIN

        return CharType.ASIAN

    @classmethod
    def process_text_whitespace(cls, text: str) -> str:
        """Process whitespace and leading and trailing spaces in strings"""
        return sub(pattern=r"\s+", repl=" ", string=text).strip()

    @classmethod
    @lru_cache(maxsize=32)
    def split_long_token(cls, token: str, width: int) -> List[str]:
        """Split long token into smaller chunks."""
        return [token[i : i + width] for i in range(0, len(token), width)]

    @classmethod
    def tokenizer(cls, text: str):
        """tokenize line"""

        buffer = ""
        last_char_type: Optional[CharType] = None

        for char in text:
            char_type = cls.get_char_type(char)

            if buffer and (char_type != last_char_type or char_type != CharType.LATIN):
                yield buffer
                buffer = ""

            buffer += char
            last_char_type = char_type

        yield buffer

    @classmethod
    def wrap(cls, text: str, width: int, once: bool = True) -> Tuple[str, bool]:
        """Wrap according to string length

        Parameters
        ----------
        text: str
            the text to be wrapped

        width: int
            the maximum length of a single line, the length of Chinese characters is 2

        once: bool
            whether to wrap only once

        Returns
        -------
        wrap_text: str
            text after auto word wrap process

        is_wrapped: bool
            whether a line break occurs in the text
        """

        width = int(width)
        lines = text.splitlines()
        is_wrapped = False
        wrapped_lines = []

        for line in lines:
            line = cls.process_text_whitespace(line)

            if cls.get_text_width(line) > width:
                wrapped_line, is_wrapped = cls._wrap_line(line, width, once)
                wrapped_lines.append(wrapped_line)

                if once:
                    wrapped_lines.append(text[len(wrapped_line) :].rstrip())
                    return "".join(wrapped_lines), is_wrapped

            else:
                wrapped_lines.append(line)

        return "\n".join(wrapped_lines), is_wrapped

    @classmethod
    def _wrap_line(cls, text: str, width: int, once: bool = True) -> Tuple[str, bool]:
        line_buffer = ""
        wrapped_lines = []
        current_width = 0

        for token in cls.tokenizer(text):
            token_width = cls.get_text_width(token)

            if token == " " and current_width == 0:
                continue

            if current_width + token_width <= width:
                line_buffer += token
                current_width += token_width

                if current_width == width:
                    wrapped_lines.append(line_buffer.rstrip())
                    line_buffer = ""
                    current_width = 0
            else:
                if current_width != 0:
                    wrapped_lines.append(line_buffer.rstrip())

                chunks = cls.split_long_token(token, width)

                for chunk in chunks[:-1]:
                    wrapped_lines.append(chunk.rstrip())

                line_buffer = chunks[-1]
                current_width = cls.get_text_width(chunks[-1])

        if current_width != 0:
            wrapped_lines.append(line_buffer.rstrip())

        if once:
            return "\n".join([wrapped_lines[0], " ".join(wrapped_lines[1:])]), True

        return "\n".join(wrapped_lines), True
