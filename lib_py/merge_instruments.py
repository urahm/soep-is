import json
import yaml
from collections import defaultdict
import pandas as pd

def import_tables():
    tables = dict(
        questionnaires=pd.read_csv("metadata/questionnaires.csv"),
        questions=pd.read_csv("metadata/questions.csv"),
        answers=pd.read_csv("metadata/answers.csv"),
    )
    return tables

def get_answers(tables):
    answers = defaultdict(list)
    for i, answer in tables["answers"].iterrows():
        answer = dict(answer)
        key = (answer["questionnaire"], answer["answer_list"])
        answers[key].append(answer)
    return answers

def get_instruments(tables):
    instrument_list = [dict(row) for i, row in tables["questionnaires"].iterrows()]
    instruments = dict([(x["questionnaire"], x) for x in instrument_list])
    for instrument in instruments.values():
        instrument["instrument"] = instrument["questionnaire"]
        instrument["questions"] = list()
    return instruments

def fill_questions(tables, instruments, answers):
    for i, question in tables["questions"].iterrows():
        question = dict(question)
        i_name = question["questionnaire"]
        if not i_name in instruments:
            instruments[i_name] = dict(
                instrument=i_name,
                questions=list()
            )
        try:
            key = (question["questionnaire"], question["answer_list"])
            question["answers"] = answers[key]
        except:
            question["answers"] = ""
        instruments[i_name]["questions"].append(question)
    return instruments

def export(instruments, export_json=True, export_yaml=False):
    if export_json:
        with open("ddionrails/instruments.json", "w") as f:
            json.dump(instruments, f)
    if export_yaml:
        with open("ddionrails/instruments.yaml", "w") as f:
            yaml.dump(instruments, f, default_flow_style=False)

def main(export_json=True, export_yaml=False):
    tables = import_tables()
    answers = get_answers(tables)
    instruments = get_instruments(tables)
    fill_questions(tables, instruments, answers)
    export(instruments, export_json, export_yaml)

if __name__ == "__main__":
    main(export_yaml=True)
