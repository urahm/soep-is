import json
import pathlib

import click
import pytest

import great_expectations as ge
from great_expectations.dataset.pandas_dataset import PandasDataset

VERSION = "v2015.1"
LANGUAGES = ("en", "de")

METADATA_DIR = pathlib.Path("../metadata")
EXPECTATIONS_DIR = pathlib.Path("expectations")
XML_DIR = pathlib.Path("../r2ddi/")


def metadata_filepath(filename: str) -> pathlib.PosixPath:
    return (METADATA_DIR / filename).with_suffix(".csv")


def expectations_filepath(filename: str) -> pathlib.PosixPath:
    return (EXPECTATIONS_DIR / filename).with_suffix(".json")


def load_expectations(filename: pathlib.PosixPath):
    with open(filename) as f:
        return json.load(f)


def have_foreign_key_relationship_based_on_key(
    df1: PandasDataset, df2: PandasDataset, key: str
) -> None:
    """
    This function gets two datasets and a string as arguments.
    The values in column "key" of df1 need to be defined
    in column "key" of df2.
    """
    unique_values = df2[key].unique()
    results = df1.expect_column_values_to_be_in_set(
        key, unique_values, result_format="COMPLETE"
    )
    if results["success"] is False:
        click.secho(json.dumps(results, indent=2), fg="red")
    assert results["success"] is True


def validate(df: PandasDataset) -> None:
    """
    This function gets a dataset as input.
    The function calls the validate method on the dataset.
    The function asserts that the overall validation result is a success.
    If the results contain False, the containing result is printed.
    Also the corresponding rows of the dataset are printed.
    """

    results = df.validate(result_format="COMPLETE")
    for result in results["results"]:
        if result["success"] is False:
            click.secho(json.dumps(result, indent=2), fg="red")
            indices = result["result"]["unexpected_index_list"]
            print(df.iloc[indices])

    assert results["success"] is True


@pytest.fixture
def questions():
    expectations_config = load_expectations(expectations_filepath("questions"))
    return ge.read_csv(
        metadata_filepath("questions"), expectations_config=expectations_config
    )


@pytest.fixture
def answers():
    expectations_config = load_expectations(expectations_filepath("answers"))
    return ge.read_csv(
        metadata_filepath("answers"), expectations_config=expectations_config
    )


@pytest.fixture
def questionnaires():
    expectations_config = load_expectations(expectations_filepath("questionnaires"))
    return ge.read_csv(
        metadata_filepath("questionnaires"), expectations_config=expectations_config
    )


@pytest.fixture
def datasets():
    expectations_config = load_expectations(expectations_filepath("datasets"))
    return ge.read_csv(
        metadata_filepath("datasets"), expectations_config=expectations_config
    )


@pytest.fixture
def generations():
    expectations_config = load_expectations(expectations_filepath("generations"))
    return ge.read_csv(
        metadata_filepath("generations"), expectations_config=expectations_config
    )


def validate_answers(answers: PandasDataset):
    validate(answers)


def validate_logical_variables():
    pass


def validate_datasets(datasets: PandasDataset):
    validate(datasets)


def validate_generations(generations: PandasDataset):
    validate(generations)


def validate_questions(questions: PandasDataset):
    validate(questions)


def validate_question_questionnaire_relationship(
    questions: PandasDataset, questionnaires: PandasDataset
):
    """ Every entry in the column "questionnaire" in "questions.csv"
        has to be defined in "questionnaires.csv"
    """
    have_foreign_key_relationship_based_on_key(
        questions, questionnaires, "questionnaire"
    )


def validate_answers_questionnaire_relationship(
    answers: PandasDataset, questionnaires: PandasDataset
):
    """ Every entry in the column "questionnaire" in "answers.csv"
        has to be defined in "questionnaires.csv"
    """
    have_foreign_key_relationship_based_on_key(answers, questionnaires, "questionnaire")


def validate_questionnaires(questionnaires):
    validate(questionnaires)


def validate_publications(publications):
    pass


def validate_xml_files(datasets: PandasDataset):
    unique_datasets = datasets["dataset_name"].unique()
    for language in LANGUAGES:
        datasets_dir = XML_DIR / VERSION / language
        assert datasets_dir.exists()
        dataset_xml_files = sorted([file.stem for file in datasets_dir.glob("*.xml")])
        assert len(dataset_xml_files) == len(unique_datasets)

        results = datasets.expect_column_values_to_be_in_set(
            "dataset_name", dataset_xml_files, result_format="SUMMARY"
        )
        assert results["success"] is True
