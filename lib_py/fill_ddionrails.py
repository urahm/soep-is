from ddi.onrails.repos import convert_r2ddi, copy, dor1, merge_instruments
from questions_variables import questions_from_generations


def main():
    copy.study()
    dor1.datasets()
    dor1.variables()
    dor1.concepts_questions()
    questions_from_generations()
    merge_instruments.main()
    convert_r2ddi.Parser("soep-is", version="v2015.1").write_json()
    copy.bibtex()


if __name__ == "__main__":
    main()
