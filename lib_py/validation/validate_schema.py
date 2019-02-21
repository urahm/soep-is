import json

import click
import pytest

from great_expectations.dataset.pandas_dataset import PandasDataset

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
    validate(publications)


def validate_questionnaires(questionnaires: PandasDataset):
    validate(questionnaires)


def validate_questions(questions: PandasDataset):
    validate(questions)


def validate_variables():
    pytest.fail("Write the test")
