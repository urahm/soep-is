import os, sys
import pandas as pd

sys.path.append(os.path.expanduser("~/github/ddi.py/"))

from ddi.onrails.repos import merge_instruments, dor1, copy, convert_r2ddi

def main():
    copy.study()
    dor1.datasets()
    dor1.variables()
    dor1.questions_variables()
    merge_instruments.main()
    convert_r2ddi.Parser(version="v2013").write_json()
    copy.bibtex()

if __name__ == "__main__":
    main()
