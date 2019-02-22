import shutil

import pandas as pd
from ddi.onrails.repos import convert_r2ddi, dor1, merge_instruments
from questions_variables import questions_from_generations

STUDY = "soep-is"
VERSION = "v2016.2"


def lowercase_column_contents(df, pattern):
    """ Modifies content of all dataframe columns where column name contains
        'pattern'.
        If
            cell contains a string => lower case
        else:
            cell contains any other type => do not modify
    """
    temp = df.filter(like=pattern).applymap(
        lambda s: s.lower() if type(s) == str else s
    )
    df.update(temp)


def copy_csv_file_with_lowercasing(inpath, outpath):
    """
    Read a csv file from inpath
    convert all entries in columns ending with "_name" to lowercase
    Write to csv file to outpath
    """
    df = pd.read_csv(inpath)
    lowercase_column_contents(df, pattern="_name")
    df.to_csv(outpath, index=False)


def main():
    shutil.copy("metadata/study.md", "ddionrails/study.md")
    shutil.copy("metadata/publications.csv", "ddionrails/publications.csv")
    shutil.copy("metadata/analysis_units.csv", "ddionrails/analysis_units.csv")
    shutil.copy(
        "metadata/conceptual_datasets.csv", "ddionrails/conceptual_datasets.csv"
    )
    shutil.copy("metadata/periods.csv", "ddionrails/periods.csv")

    copy_csv_file_with_lowercasing("metadata/datasets.csv", "ddionrails/datasets.csv")
    copy_csv_file_with_lowercasing("metadata/variables.csv", "ddionrails/variables.csv")

    dor1.concepts_questions()
    questions_from_generations(VERSION)
    merge_instruments.main()
    convert_r2ddi.Parser(STUDY, version=VERSION).write_json()


if __name__ == "__main__":
    main()
