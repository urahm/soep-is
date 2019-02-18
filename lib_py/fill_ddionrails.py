from ddi.onrails.repos import convert_r2ddi, copy, dor1, merge_instruments
from questions_variables import questions_from_generations

STUDY = "soep-is"
VERSION = "v2015.1"


def main():
    copy.study()
    dor1.datasets()
    dor1.variables()
    dor1.concepts_questions()
    questions_from_generations(VERSION)
    merge_instruments.main()
    convert_r2ddi.Parser(STUDY, version=VERSION).write_json()
    copy.bibtex()


if __name__ == "__main__":
    main()
