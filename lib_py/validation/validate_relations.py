import json

import click
import pytest

from great_expectations.dataset.pandas_dataset import PandasDataset

pytestmark = [pytest.mark.relation]


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


def validate_answers_questionnaire_relationship(
    answers: PandasDataset, questionnaires: PandasDataset
):
    """ Every entry in the column "questionnaire" in "answers.csv"
        has to be defined in "questionnaires.csv"
    """
    have_foreign_key_relationship_based_on_key(answers, questionnaires, "questionnaire")


def validate_question_questionnaire_relationship(
    questions: PandasDataset, questionnaires: PandasDataset
):
    """ Every entry in the column "questionnaire" in "questions.csv"
        has to be defined in "questionnaires.csv"
    """
    have_foreign_key_relationship_based_on_key(
        questions, questionnaires, "questionnaire"
    )


def validate_datasets_analysis_units_relationship(
    datasets: PandasDataset, analysis_units: PandasDataset
):
    """ Every entry in the column "analysis_unit_name" in "datasets.csv"
        has to be defined in "analysis_units.csv"
    """
    have_foreign_key_relationship_based_on_key(
        datasets, analysis_units, "analysis_unit_name"
    )
