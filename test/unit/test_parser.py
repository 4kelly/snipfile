from typing import List, NamedTuple, Union

from snipfile._parser import Snippet, Token, is_a_snippet, parser, tokenize


def test_is_a_snippet():
    class Case(NamedTuple):
        test: str
        want: bool

    cases = [
        Case("--8<-- filename.txt", True),
        Case("--8<--", True),
        # Case("\t--8<--", True),
        # Case("    --8<--", True),
        Case("Not a line --8<--", False),
        Case("Not a line", False),
    ]

    for case in cases:
        got = is_a_snippet(case.test)
        assert got == case.want


def test_tokenize():
    class Case(NamedTuple):
        name: str
        test: str
        want_items: List[str]
        want_tokens: List[Token]

    cases = [
        Case(
            "Happy Path",
            "--8<-- filename.txt",
            ["--8<--", "filename.txt"],
            [Token.SNIPPET, Token.FILEPATH],
        ),
        Case(
            "Happy Path Line Range",
            "--8<-- filename.txt 1 3",
            ["--8<--", "filename.txt", "1", "3"],
            [Token.SNIPPET, Token.FILEPATH, Token.LINENUM, Token.LINENUM],
        ),
        Case(
            "Weird Spacing",
            " --8<--  filename.txt    1  3",
            ["--8<--", "filename.txt", "1", "3"],
            [Token.SNIPPET, Token.FILEPATH, Token.LINENUM, Token.LINENUM],
        ),
        Case(
            "Happy Path Negative Line",
            "--8<-- filename.txt -1",
            ["--8<--", "filename.txt", "-1"],
            [Token.SNIPPET, Token.FILEPATH, Token.LINENUM],
        ),
        Case(
            "Filename with parent directory",
            "--8<-- ../filename.txt",
            ["--8<--", "../filename.txt"],
            [Token.SNIPPET, Token.FILEPATH],
        ),
        Case(
            "Filename with sub directory",
            "--8<-- dir/filename.txt",
            ["--8<--", "dir/filename.txt"],
            [Token.SNIPPET, Token.FILEPATH],
        ),
        Case("Snippet Only", "--8<--", ["--8<--"], [Token.SNIPPET]),
    ]
    for case in cases:
        got_items = []
        got_tokens = []
        token_generator = tokenize(case.test)
        for item, token in token_generator:
            got_items.append(item)
            got_tokens.append(token)
        assert got_items == case.want_items
        assert got_tokens == case.want_tokens


def test_parse_snippet():
    class Case(NamedTuple):
        name: str
        test_items: List[Union[str, int]]
        test_tokens: List[Token]
        want: Snippet

    cases = [
        Case(
            "Happy Path",
            ["--8<--", "filename.txt"],
            [Token.SNIPPET, Token.FILEPATH],
            Snippet(filepath="filename.txt"),
        ),
        Case(
            "Happy Path Line Range",
            ["--8<--", "filename.txt", 1, 3],
            [Token.SNIPPET, Token.FILEPATH, Token.LINENUM, Token.LINENUM],
            Snippet(filepath="filename.txt", startline=1, endline=3),
        ),
    ]
    for case in cases:
        got = parser(case.test_items, case.test_tokens)
        assert got == case.want
