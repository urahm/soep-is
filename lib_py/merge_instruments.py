import json
import yaml
import pandas as pd

def import_tables():
    tables = dict(
        questionnaires=pd.read_csv("metadata/questionnaires.csv"),
        questions=pd.read_csv("metadata/questions.csv"),
        answers=pd.read_csv("metadata/answers.csv"),
    )
    return tables

def gen_instruments(tables):
    instrument_list = [dict(row) for i, row in tables["questionnaires"].iterrows()]
    instruments = dict([(x["questionnaire"], x) for x in instrument_list])
    for instrument in instruments.values():
        instrument["instrument"] = instrument["questionnaire"]
        instrument["questions"] = list()
    for i, question in tables["questions"].iterrows():
        question = dict(question)
        i_name = question["questionnaire"]
        if not i_name in instruments:
            instruments[i_name] = dict(
                instrument=i_name,
                questions=list()
            )
        instruments[i_name]["questions"].append(question)
    return instruments

def main(export_json=True, export_yaml=False):
    tables = import_tables()
    instruments = gen_instruments(tables)
    if export_json:
        with open("ddionrails/instruments.json", "w") as f:
            json.dump(instruments, f)
    if export_yaml:
        with open("ddionrails/instruments.yaml", "w") as f:
            yaml.dump(instruments, f, default_flow_style=False)

if __name__ == "__main__":
    main()
