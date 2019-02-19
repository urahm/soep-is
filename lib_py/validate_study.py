import json

import click
import pytest

import great_expectations as ge

QUESTIONS_FILENAME = "../metadata/questions.csv"
QUESTIONNAIRES_FILENAME = "../metadata/questionnaires.csv"

QUESTIONS_EXPECTATIONS_FILENAME = "expectations/questions.json"
QUESTIONNAIRES_EXPECTATIONS_FILENAME = "expectations/questionnaires.json"


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
def questionnaires():
    return ge.read_csv(
        QUESTIONNAIRES_FILENAME,
        expectations_config=load_expectations(QUESTIONNAIRES_EXPECTATIONS_FILENAME),
    )


def validate(data_filename, expectations_filename):
    expectations_config = load_expectations(expectations_filename)
    df = ge.read_csv(data_filename, expectations_config=expectations_config)
    results = df.validate(result_format="COMPLETE")
    for result in results["results"]:
        if result["success"] is False:
            click.secho(json.dumps(result, indent=2), fg="red")
    assert results["success"] is True


def validate_answers():
    pass


def validate_logical_variables():
    pass


def validate_logical_datasets():
    pass


def validate_generations():
    pass


def validate_questions():
    validate(QUESTIONS_FILENAME, QUESTIONS_EXPECTATIONS_FILENAME)


def validate_question_questionnaire_relationship(questions, questionnaires):
    unique_questionnaires = questionnaires["questionnaire"].unique()
    results = questions.expect_column_values_to_be_in_set(
        "questionnaire", unique_questionnaires, result_format="COMPLETE"
    )
    if results["success"] is False:
        click.secho(json.dumps(results, indent=2), fg="red")
    assert results["success"] is True


def validate_questionnaires():
    validate("../metadata/questionnaires.csv", "expectations/questionnaires.json")
