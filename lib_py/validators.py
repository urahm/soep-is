import pytest
from colorama import Fore, Style, init

import pandas as pd

init()

STUDY = "soep-is"


@pytest.fixture(scope="module")
def questions():
    return pd.read_csv("metadata/questions.csv")


@pytest.fixture(scope="module")
def questionnaires():
    return pd.read_csv("metadata/questionnaires.csv", dtype={"period": str})


def assert_study_in_df(df):
    # only one study is defined in the study column
    assert 1 == len(df["study"].unique())
    # the one defined study is equal to STUDY
    assert STUDY == df["study"].unique()[0]


def test_questions(questions):
    WANTED_COLUMNS = {"study", "questionnaire"}
    assert WANTED_COLUMNS.issubset(questions.columns)
    assert_study_in_df(questions)


def test_questionnaries(questionnaires):
    WANTED_COLUMNS = {"study", "questionnaire", "label", "period"}
    assert WANTED_COLUMNS.issubset(questionnaires.columns)
    assert_study_in_df(questionnaires)

    has_no_period = questionnaires["period"].isna()
    if len(questionnaires[has_no_period]) != 0:
        print("Questionnaires without period:")
        print(questionnaires[has_no_period])

    assert len(questionnaires[has_no_period]) == 0


def test_questions_questionnaries():
    """
    Every question in "questions.csv" should reference a
    questionnaire that is defined in questionnaires.csv
    """
    WANTED_COLUMNS = {"study", "questionnaire"}
    questions = pd.read_csv("metadata/questions.csv")
    assert WANTED_COLUMNS.issubset(questions.columns)

    questionnaires = pd.read_csv("metadata/questionnaires.csv")
    assert WANTED_COLUMNS.issubset(questionnaires.columns)

    # merge two files based on "questionnaire"
    merged = questions.merge(questionnaires, on="questionnaire", how="outer")

    questionnaires_not_used = merged[merged["study_x"].isna()]
    if len(questionnaires_not_used) != 0:
        print(questionnaires_not_used)
        print(questionnaires_not_used["questionnaire"].unique())

    questionnaires_not_defined = merged[merged["study_y"].isna()]

    if len(questionnaires_not_defined) != 0:
        unique_questionnaires = questionnaires_not_defined["questionnaire"].unique()
        print()
        print(
            Fore.RED
            + f'Questionnaires not defined in "questionnaires.csv": {unique_questionnaires}'
        )

        row_indices = questions[
            questions["questionnaire"].isin(unique_questionnaires)
        ].index.tolist()
        print(Fore.RED + f'\nAffected rows in "questions.csv": {row_indices}')
        print(
            Fore.RED
            + f'{questions[questions["questionnaire"].isin(unique_questionnaires)]}'
        )
        print(Style.RESET_ALL, end="")

    assert len(questionnaires_not_used) == 0
    assert (
        len(questionnaires_not_defined) == 0
    ), 'Some questionnaires are not defined in "questionnaires.csv"'
