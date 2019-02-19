import json

import click
import pytest

import great_expectations as ge

ANSWERS_FILENAME = "../metadata/answers.csv"
QUESTIONS_FILENAME = "../metadata/questions.csv"
QUESTIONNAIRES_FILENAME = "../metadata/questionnaires.csv"
DATASETS_FILENAME = "../metadata/logical_datasets.csv"

ANSWERS_EXPECTATIONS_FILENAME = "expectations/answers.json"
QUESTIONS_EXPECTATIONS_FILENAME = "expectations/questions.json"
QUESTIONNAIRES_EXPECTATIONS_FILENAME = "expectations/questionnaires.json"
DATASETS_EXPECTATIONS_FILENAME = "expectations/datasets.json"


def load_expectations(filename):
    with open(filename) as f:
        return json.load(f)


@pytest.fixture
def questions():
    return ge.read_csv(
        QUESTIONS_FILENAME,
        expectations_config=load_expectations(QUESTIONS_EXPECTATIONS_FILENAME),
    )


@pytest.fixture
def answers():
    return ge.read_csv(
        ANSWERS_FILENAME,
        expectations_config=load_expectations(ANSWERS_EXPECTATIONS_FILENAME),
    )


@pytest.fixture
def questionnaires():
    return ge.read_csv(
        QUESTIONNAIRES_FILENAME,
        expectations_config=load_expectations(QUESTIONNAIRES_EXPECTATIONS_FILENAME),
    )


@pytest.fixture
def datasets():
    return ge.read_csv(
        DATASETS_FILENAME,
        expectations_config=load_expectations(DATASETS_EXPECTATIONS_FILENAME),
    )


def validate(df):
    results = df.validate(result_format="COMPLETE")
    for result in results["results"]:
        if result["success"] is False:
            click.secho(json.dumps(result, indent=2), fg="red")
            indices = result["result"]["unexpected_index_list"]
            print(df.iloc[indices])

    assert results["success"] is True


def validate_answers(answers):
    validate(answers)


def validate_logical_variables():
    pass


def validate_logical_datasets(datasets):
    # remove datasets with conceptual_dataset "raw"
    datasets = datasets[datasets["conceptual_dataset"] != "raw"]
    validate(datasets)


def validate_generations():
    pass


def validate_questions(questions):
    validate(questions)


def foreign_key_relationship(df1, df2, key):
    unique_values = df2[key].unique()
    results = df1.expect_column_values_to_be_in_set(
        key, unique_values, result_format="COMPLETE"
    )
    if results["success"] is False:
        click.secho(json.dumps(results, indent=2), fg="red")
    assert results["success"] is True


def validate_question_questionnaire_relationship(questions, questionnaires):
    """ Every entry in the column "questionnaire" in "questions.csv"
        has to be defined in "questionnaires.csv"
    """
    foreign_key_relationship(questions, questionnaires, "questionnaire")


def validate_answers_questionnaire_relationship(answers, questionnaires):
    """ Every entry in the column "questionnaire" in "answers.csv"
        has to be defined in "questionnaires.csv"
    """
    foreign_key_relationship(answers, questionnaires, "questionnaire")


def validate_questionnaires(questionnaires):
    validate(questionnaires)
