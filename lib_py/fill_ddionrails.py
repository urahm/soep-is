import os, sys
import pandas as pd

sys.path.append(os.path.expanduser("~/github/ddi.py/"))

from ddi.onrails.repos import merge_instruments, dor1, copy

def main():
    copy.study()
    dor1.datasets()
    dor1.variables()
    dor1.questions_variables()
    merge_instruments.main()
    copy.r2ddi("r2ddi/v2013/en", "ddionrails/r2ddi/v2013")

if __name__ == "__main__":
    main()
