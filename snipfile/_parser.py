"""
Contains a lexer and parser for the following syntax.

# --8<-- filename.ext 2 3 # template lines 2-3 (0 index
# --8<-- filename.ext 1  # skip first line (0 index)
# --8<-- filename.ext -1 # skip last line (negative slice)
# Handle extra spaces in the syntax
# TODO: Handle preserving indents for snippets in lists, etc.
"""

import enum
import logging
import re
from dataclasses import dataclass
from typing import IO, List, Optional, Tuple

logger = logging.getLogger(__name__)

SNIPPET_REGEX = re.compile(r"^--8<--")
FILEPATH_REGEX = re.compile(r"^[\S]?[\w.\\/\-]+\.[a-z]+")
LINENUM_REGEX = re.compile(r"[\-]?[0-9]+")

format_error = (
    "--8<-- <filepath> <line-num> <line-num>\nwhere:"
    "\n\t- <filepath> is a relative path."
    "\n - <line num> is an optional range of 2 ints, or a single integer."
)


def snip(f: IO, o: IO) -> None:
    for line in f:

        if is_a_snippet(line):
            snippet = parse(line)

            with open(snippet.filepath) as snippet_data:
                for snippet_line in snippet_data:
                    o.write(snippet_line)
        else:
            o.write(line)


@dataclass(frozen=True)
class Snippet:
    filepath: str
    basedir: str = None
    startline: Optional[int] = None
    endline: Optional[int] = None


class Token(enum.Enum):
    SNIPPET = SNIPPET_REGEX
    FILEPATH = FILEPATH_REGEX
    LINENUM = LINENUM_REGEX


def parse(line: str) -> Snippet:
    items = []
    tokens = []
    for item, token in tokenize(line):
        items.append(item)
        tokens.append(token)

    snippet = parser(items, tokens)
    logger.debug(f"Snippet: {snippet}")
    return snippet


def tokenize(line: str) -> Tuple[str, Token]:
    logger.debug(f"Tokenizing line: {line}")

    for token in Token:
        line = line.strip()

        match = token.value.findall(line)
        if match:
            for m in match:
                line = line[len(m) :]
                logger.debug(f"{m} is a {token}")
                yield m, token


def parser(items: List[str], tokens: List[Token]) -> Snippet:
    """
    Items and tokens are equal length lists, where each token describes the corresponding index in items
    The complexity of the above sentence is probably a bad sign.
    """

    # Valid grammars
    if tokens == [Token.SNIPPET, Token.FILEPATH]:
        _, filepath = items
        return Snippet(filepath=filepath)
    elif tokens == [Token.SNIPPET, Token.FILEPATH, Token.LINENUM]:
        _, filepath, startline = items
        return Snippet(filepath=filepath, startline=int(startline))
    elif tokens == [Token.SNIPPET, Token.FILEPATH, Token.LINENUM, Token.LINENUM]:
        _, filepath, startline, endline = items
        return Snippet(filepath=filepath, startline=int(startline), endline=(endline))
    else:
        raise SyntaxError()


def is_a_snippet(line: str) -> bool:
    if SNIPPET_REGEX.search(line):
        return True
    return False
