
import json
from pathlib import Path

import pytest

from tokenizer import Tokenizer


@pytest.fixture
def tokenizer():
    return Tokenizer()


@pytest.fixture
def imdb_sample():
    sample_path = Path(__file__).with_name("imdb_sample.json")
    return json.loads(sample_path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", []),
        ("<br><p></p>", []),
        ("Hello WORLD!", ["hello", "world"]),
        ("...!?!?!?", []),
        ("zażółć gęślą jaźń", ["zażółć", "gęślą", "jaźń"]),
        ("A bb CCC", ["a", "bb", "ccc"]),
    ],
)
def test_tokenize_cases(tokenizer, text, expected):
    assert tokenizer.tokenize(text) == expected


def test_vocab_dedup(tokenizer):
    assert tokenizer.vocab(
        ["aa bb", "bb cc"]
    ) == {"aa", "bb", "cc"}


def test_min_length_filter():
    tokenizer = Tokenizer(min_length=4)

    assert tokenizer.tokenize(
        "a bb ccc dddd eeeee"
    ) == ["dddd", "eeeee"]


def test_configuration_flags():
    assert Tokenizer(lower=False).tokenize(
        "Hello"
    ) == ["Hello"]

    assert Tokenizer(strip_html=False).tokenize(
        "<br>hello"
    ) == ["br", "hello"]


def test_imdb_sample_size(imdb_sample):
    assert len(imdb_sample) == 20
    assert all(isinstance(text, str) for text in imdb_sample)


def test_imdb_integration(tokenizer, imdb_sample):
    vocabulary = tokenizer.vocab(imdb_sample)

    assert len(vocabulary) > 500


@pytest.mark.xfail(
    strict=True,
    reason="Celowo błędne oczekiwanie dla lower=False",
)
def test_expected_failure():
    tokenizer = Tokenizer(lower=False)

    assert tokenizer.tokenize("Hello") == ["hello"]
