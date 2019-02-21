import json
import pathlib

import click
import pytest
from lxml import etree

import pandas as pd
from great_expectations.dataset.pandas_dataset import PandasDataset

pytestmark = [pytest.mark.relation]

VERSION = "v2015.1"
LANGUAGES = ("en", "de")
XML_DIR = pathlib.Path("../r2ddi/")


def have_foreign_key_relationship_based_on_key(
    df1: PandasDataset, df2: PandasDataset, key_df1: str, key_df2: str
) -> None:
    """
    This function gets two datasets and a string as arguments.
    The values in column "key_df1" of df1 need to be defined
    in column "key_df2" of df2.
    """
    unique_values_df1 = df1[key_df1].sort_values().unique().tolist()
    unique_values_df2 = df2[key_df2].sort_values().unique().tolist()

    results = df1.expect_column_values_to_be_in_set(
        key_df1, unique_values_df2, result_format="COMPLETE"
    )
    if results["success"] is False:
        click.secho(json.dumps(results, indent=2), fg="red")
    assert results["success"] is True
    assert unique_values_df1 == unique_values_df2


def validate_answers_questionnaire_relationship(
    answers: PandasDataset, questionnaires: PandasDataset
):
    """ Every entry in the column "questionnaire" in "answers.csv"
        has to be defined in "questionnaires.csv"
    """
    have_foreign_key_relationship_based_on_key(
        answers, questionnaires, "questionnaire", "questionnaire"
    )


def validate_question_questionnaire_relationship(
    questions: PandasDataset, questionnaires: PandasDataset
):
    """ Every entry in the column "questionnaire" in "questions.csv"
        has to be defined in "questionnaires.csv"
    """
    have_foreign_key_relationship_based_on_key(
        questions, questionnaires, "questionnaire", "questionnaire"
    )


def validate_datasets_relations(
    datasets: PandasDataset,
    analysis_units: PandasDataset,
    conceptual_datasets: PandasDataset,
    periods: PandasDataset,
):
    """
    Every entry in "datasets.csv" in the column
    1.) "analysis_unit_name" has to be defined in "analysis_units.csv"
    2.) "conceptual_dataset_name" has to be defined in "conceptual_datasets.csv"
    3.) "period_name" has to be defined in "periods.csv"

    """
    have_foreign_key_relationship_based_on_key(
        datasets, analysis_units, "analysis_unit_name", "name"
    )
    have_foreign_key_relationship_based_on_key(
        datasets, conceptual_datasets, "conceptual_dataset_name", "name"
    )
    have_foreign_key_relationship_based_on_key(datasets, periods, "period_name", "name")


def validate_xml_file_count_and_names(datasets: PandasDataset):

    """
    The number of xml files has to match the number of rows in "datasets.csv"
    The names of the xml files have to match the contents of the "name" column in "datasets.csv"
    """

    unique_datasets = datasets["name"].unique()
    for language in LANGUAGES:
        datasets_dir = XML_DIR / VERSION / language
        assert datasets_dir.exists()
        dataset_xml_files = sorted([file.stem for file in datasets_dir.glob("*.xml")])
        assert len(dataset_xml_files) == len(unique_datasets)

        results = datasets.expect_column_values_to_be_in_set(
            "name", dataset_xml_files, result_format="SUMMARY"
        )
        assert results["success"] is True


def get_variable(variable):
    return (variable.get("files"), variable.get("ID"), variable.findtext("labl"))


def read_xml(xml_file):
    return (
        get_variable(variable)
        for variable in etree.parse(str(xml_file)).findall("//var")
    )


def validate_xml_files_variables(datasets: PandasDataset):

    for language in LANGUAGES:
        variables_all_datasets = []
        datasets_dir = XML_DIR / VERSION / language
        assert datasets_dir.exists()

        dataset_xml_files = (file for file in datasets_dir.glob("*.xml"))
        for file in dataset_xml_files:
            variables_all_datasets.extend(read_xml(file))

        df = pd.DataFrame(variables_all_datasets, columns=["dataset", "name", "label"])
        df.sort_values(by=["dataset", "name"], inplace=True)

        print(df.head(10))
        print(len(df))

        break
