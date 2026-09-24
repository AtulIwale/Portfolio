"""
Rebuild the cleaned dataset from the raw extract.

    1. Get data/raw/dob_major_jobs.csv with `python src/download.py` (or the browser URL it prints)
    2. From the project folder, run:  python src/clean.py

Outputs
    data/dob_initial_filings_clean.csv.gz   one row per job (its initial filing), outcome and filing-day features
    reports/data_quality.json            the counts quoted in the README
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import cleaning as C

KEEP = ["job_number", "job_filing_number", "filing_date", "split", "borough", "commmunity_board", "nta", "job_type", "filing_review_type",
        "building_type", "owner_type", "applicant_professional_title", "review_building_code", "little_e",
        "initial_cost", "total_construction_floor_area", "existing_dwelling_units", "proposed_dwelling_units",
        *C.WORK_FLAGS, "job_description", "filing_status", "approved_date", "first_permit_date", "event", "duration", "withdrawn", "bad_dates",
        "log_cost", "cost_zero", "log_area", "cost_per_sqft", "units_added", "n_work_types", "desc_words", "filing_month", "pe_applicant",
        "filed_30d", "open_queue"]


def build(raw):
    dedup = C.dedupe(C.split_filing_number(raw))
    initial = C.tidy(dedup[dedup.is_initial])
    df = initial[initial.filing_date.notna()]
    df = C.add_split(C.add_features(C.add_outcome(df), df))
    return dedup, initial, df


def main():
    raw = C.load_raw()
    dedup, initial, df = build(raw)
    final = df[KEEP].sort_values("filing_date").reset_index(drop=True)
    os.makedirs("reports", exist_ok=True)
    final.to_csv("data/dob_initial_filings_clean.csv.gz", index=False, date_format="%Y-%m-%d")
    rep = C.quality_report(raw, dedup, initial, df)
    json.dump(rep, open("reports/data_quality.json", "w"), indent=2, default=str)
    print(json.dumps(rep, indent=2, default=str))


if __name__ == "__main__":
    main()
