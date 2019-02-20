import json
import pathlib

import click
import pytest

from great_expectations.dataset.pandas_dataset import PandasDataset

VERSION = "v2015.1"
LANGUAGES = ("en", "de")
XML_DIR = pathlib.Path("../r2ddi/")

pytestmark = [pytest.mark.schema]


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


def validate_analysis_units(analysis_units: PandasDataset):
    validate(analysis_units)


def validate_answers(answers: PandasDataset):
    validate(answers)


def validate_datasets(datasets: PandasDataset):
    validate(datasets)


def validate_generations(generations: PandasDataset):
    validate(generations)


def validate_periods(periods: PandasDataset):
    validate(periods)


def validate_publications(publications: PandasDataset):
    pytest.fail("Write the test")


def validate_questionnaires(questionnaires: PandasDataset):
    validate(questionnaires)


def validate_questions(questions: PandasDataset):
    validate(questions)


def validate_logical_variables():
    pytest.fail("Write the test")


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
