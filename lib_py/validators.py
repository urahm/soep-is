from colorama import Fore, init

import pandas as pd

init()


def test_questions_questionnaries():
    """
    Every question in "questions.csv" should reference a
    questionnaire that is defined in questionnaires.csv
    """
    questions = pd.read_csv("metadata/questions.csv")
    assert "questionnaire" in questions.columns
    assert "study" in questions.columns

    questionnaires = pd.read_csv("metadata/questionnaires.csv")
    assert "questionnaire" in questionnaires.columns
    assert "study" in questionnaires.columns

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
        print('\nAffected rows in "questions.csv":')
        print(questions[questions["questionnaire"].isin(unique_questionnaires)])
        print(Style.RESET_ALL, end="")

    assert len(questionnaires_not_used) == 0
    assert (
        len(questionnaires_not_defined) == 0
    ), 'Some questionnaires are not defined in "questionnaires.csv"'
