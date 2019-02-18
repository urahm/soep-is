import pandas as pd
from pandas.util.testing import assert_frame_equal
from questions_variables import (
    create_indirect_links_once,
    create_indirect_links_recursive,
    create_questions_from_generations,
)


def test_create_indirect_links_once():
    df = pd.read_csv("tests/data/generations_run_once.csv")
    result = create_indirect_links_once(df)
    expected = pd.read_csv("tests/data/generations_run_once_expected.csv")
    assert_frame_equal(expected, result)


def test_create_indirect_links_recursive():
    df = pd.read_csv("tests/data/generations_run_twice.csv")
    result = create_indirect_links_recursive(df)
    expected = pd.read_csv("tests/data/generations_run_twice_expected.csv")
    assert_frame_equal(expected, result)


def test_questions_from_generations():
    result = create_questions_from_generations(
        "y1", "tests/data/logical_variables.csv", "tests/data/generations_run_once.csv"
    )
    expected = pd.read_csv("tests/data/questions_variables.csv")
    assert_frame_equal(expected, result)


def test_questions_from_generations_with_multiple_versions():
    result = create_questions_from_generations(
        "y1",
        "tests/data/logical_variables.csv",
        "tests/data/generations_with_multiple_versions.csv",
    )
    expected = pd.read_csv("tests/data/questions_variables.csv")
    assert_frame_equal(expected, result)
