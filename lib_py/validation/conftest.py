import json
import pathlib

import pytest

import great_expectations as ge

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


def prepare_fixture(entity: str):
    expectations_config = load_expectations(expectations_filepath(entity))
    return ge.read_csv(
        metadata_filepath(entity), expectations_config=expectations_config
    )


@pytest.fixture
def analysis_units():
    """ A PandasDataset based on the input file "analysis_units.csv" and the expecations file "analysis_units.json"
    """
    return prepare_fixture("analysis_units")


@pytest.fixture
def answers():
    """ A PandasDataset based on the input file "answers.csv" and the expecations file "answers.json"
    """
    return prepare_fixture("answers")


@pytest.fixture
def conceptual_datasets():
    """ A PandasDataset based on the input file "conceptual_datasets.csv" and the expecations file "conceptual_datasets.json"
    """
    return prepare_fixture("conceptual_datasets")


@pytest.fixture
def datasets():
    """ A PandasDataset based on the input file "datasets.csv" and the expecations file "datasets.json"
    """
    return prepare_fixture("datasets")


@pytest.fixture
def generations():
    """ A PandasDataset based on the input file "generations.csv" and the expecations file "generations.json"
    """
    return prepare_fixture("generations")


@pytest.fixture
def periods():
    """ A PandasDataset based on the input file "periods.csv" and the expecations file "periods.json"
    """
    return prepare_fixture("periods")


@pytest.fixture
def publications():
    """ A PandasDataset based on the input file "publications.csv" and the expecations file "publications.json"
    """
    return prepare_fixture("publications")


@pytest.fixture
def questionnaires():
    """ A PandasDataset based on the input file "questionnaires.csv" and the expecations file "questionnaires.json"
    """
    return prepare_fixture("questionnaires")


@pytest.fixture
def questions():
    """ A PandasDataset based on the input file "questions.csv" and the expecations file "questions.json"
    """
    return prepare_fixture("questions")
