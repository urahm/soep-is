import pandas as pd
from ddi.onrails.repos import convert_r2ddi, copy, dor1, merge_instruments
from questions_variables import questions_from_generations

STUDY = "soep-is"
VERSION = "v2015.1"


def datasets():
    logical_datasets = pd.read_csv("metadata/logical_datasets.csv")
    datasets_distributions = pd.read_csv("metadata/datasets_distributions.csv")

    # merge on "study" and "dataset"
    datasets = logical_datasets.merge(datasets_distributions, on=["study", "dataset"])

    WANTED_COLUMNS = [
        "study",
        "dataset",
        "label",
        "description",
        "conceptual_dataset",
        "analysis_unit",
        "period",
    ]
    datasets = datasets[WANTED_COLUMNS]

    RENAME_COLUMNS = {
        "study": "study_name",
        "dataset": "dataset_name",
        "period": "period_name",
        "analysis_unit": "analysis_unit_name",
        "conceptual_dataset": "conceptual_dataset_name",
    }
    datasets.rename(columns=RENAME_COLUMNS, inplace=True)

    SORT_COLUMNS = ["study_name", "dataset_name"]
    datasets.sort_values(by=SORT_COLUMNS, inplace=True)
    dor1.lower_all_names(datasets)
    datasets.to_csv("ddionrails/datasets.csv", index=False)


def main():
    copy.study()
    datasets()
    dor1.variables()
    dor1.concepts_questions()
    questions_from_generations(VERSION)
    merge_instruments.main()
    convert_r2ddi.Parser(STUDY, version=VERSION).write_json()
    copy.bibtex()


if __name__ == "__main__":
    main()
