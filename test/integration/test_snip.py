import tempfile
from io import StringIO

from snipfile._parser import snip


def test_snip_not_snippet():
    f = StringIO("Test\nFile")
    o = StringIO()

    snip(f, o)

    assert f.getvalue() == o.getvalue()


def test_snip_snippet():
    with tempfile.NamedTemporaryFile(suffix=".txt") as tf:
        tf.write(b"Hello\n")
        tf.flush()

        f = StringIO("TestFile\n--8<-- {f}".format(f=tf.name))
        o = StringIO()

        expected = "TestFile\nHello\n"

        snip(f, o)

    assert expected == o.getvalue()


def test_snip_2snippet():
    with tempfile.NamedTemporaryFile(suffix=".txt") as tf:
        tf.write(b"Hello\n")
        tf.flush()

        f = StringIO("TestFile\n--8<-- {f}\n--8<-- {f}".format(f=tf.name))
        o = StringIO()

        expected = "TestFile\nHello\nHello\n"

        snip(f, o)

    assert expected == o.getvalue()
