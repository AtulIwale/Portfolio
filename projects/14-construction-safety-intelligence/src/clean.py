"""
Rebuild the cleaned construction dataset from OSHA's raw file.

    1. Download https://www.osha.gov/sites/default/files/January2015toNovember2025.zip
       (the "Download the full SIR data set" button on https://www.osha.gov/severe-injury-reports)
    2. Unzip January2015toNovember2025.csv into data/raw/
    3. From the project folder, run:  python src/clean.py

Outputs
    data/osha_construction_clean.csv   one row per construction injury report, no employer names or addresses
    data/cause_group_map.csv           every OSHA event code and title, with the cause group it was mapped to
    reports/data_quality.json          the counts quoted in the README
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from cleaning import (load_raw, filter_construction, tidy, redact_all, add_labels,
                      cause_map_table, final_table, quality_report)


def main():
    raw = load_raw()
    con = filter_construction(raw)
    df = add_labels(redact_all(tidy(con)))
    final = final_table(df)

    os.makedirs("reports", exist_ok=True)
    final.to_csv("data/osha_construction_clean.csv", index=False)
    cause_map_table(df).to_csv("data/cause_group_map.csv", index=False)
    rep = quality_report(raw, con, final)
    with open("reports/data_quality.json", "w") as f:
        json.dump(rep, f, indent=2, default=str)
    print(json.dumps(rep, indent=2, default=str))


if __name__ == "__main__":
    main()
