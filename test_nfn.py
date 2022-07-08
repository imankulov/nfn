from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from nfn import Arguments, nfn


def test_nfn_works_for_empty_directory(tmpdir: Path):
    ret = nfn(Arguments(dir=str(tmpdir), name="fooNNN.txt", touch=False))
    assert ret == "foo001.txt"


def test_nfn_works_for_non_empty_directory(tmpdir: Path):
    (Path(tmpdir) / "foo001.txt").touch()
    ret = nfn(Arguments(dir=str(tmpdir), name="fooNNN.txt", touch=False))
    assert ret == "foo002.txt"


@pytest.mark.parametrize("filename", ["foo.txt", "foo/barNNN.txt"])
def test_nfn_forbidden_names(tmpdir: Path, filename: str):
    with pytest.raises(ValueError):
        nfn(Arguments(dir=str(tmpdir), name=filename, touch=False))


def test_nfn_non_existent_directories(tmpdir: Path):
    with pytest.raises(ValueError):
        nfn(Arguments(dir=str(tmpdir) + "non-existent", name="foo.txt", touch=False))


def test_nfn_touch_creates_file(tmpdir: Path):
    ret = nfn(Arguments(dir=str(tmpdir), name="fooNNN.txt", touch=True))
    assert ret == "foo001.txt"
    assert (Path(tmpdir) / "foo001.txt").is_file()


def test_nfn_race_conditions(tmpdir: Path):
    with ThreadPoolExecutor(max_workers=10) as executor:
        args = [Arguments(dir=str(tmpdir), name="fooNNN.txt", touch=True)] * 100
        result = set(executor.map(nfn, args))
    assert len(result) == 100
