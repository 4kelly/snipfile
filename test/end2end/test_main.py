import shutil
from filecmp import cmp

from snipfile.commands import snipfiles


# Must be run from root due to relative paths.
def test_e2e():
    # Cleanup
    shutil.rmtree("test/tmp", ignore_errors=True)

    snipfiles(input_dir="test/data/golden_in", output_dir="test/tmp", pattern="*")

    actual_1 = "test/tmp/test/data/golden_in/test.md"
    golden_1 = "test/data/golden_out/test/data/golden_in/test.md"

    actual_2 = "test/tmp/test/data/golden_in/test.txt"
    golden_2 = "test/data/golden_out/test/data/golden_in/test.txt"

    # Nested Dir
    actual_3 = "test/tmp/test/data/golden_in/nested/test.md"
    golden_3 = "test/data/golden_out/test/data/golden_in/nested/test.md"

    actual_4 = "test/tmp/test/data/golden_in/nested/test.txt"
    golden_4 = "test/data/golden_out/test/data/golden_in/nested/test.txt"

    assert cmp(actual_1, golden_1) is True
    assert cmp(actual_2, golden_2) is True
    assert cmp(actual_3, golden_3) is True
    assert cmp(actual_4, golden_4) is True

    # Cleanup
    shutil.rmtree("test/tmp", ignore_errors=True)
