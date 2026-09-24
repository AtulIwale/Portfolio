"""
Cleaning and feature functions for Project 15: NYC permit approval forecasting.

Source: NYC Open Data, "DOB NOW: Build - Job Application Filings" (dataset w9ak-ipjd),
        https://data.cityofnewyork.us/Housing-Development/DOB-NOW-Build-Job-Application-Filings/w9ak-ipjd
        Extract used here: the four major job types (New Building, Alteration CO, ALT-CO New Building
        with Existing Elements to Remain, Full Demolition), 55 columns, no applicant or owner names.
        Downloaded 24 Sep 2026: 131,515 filing records. See src/download.py for the exact query.

Run `python src/clean.py` to rebuild data/dob_initial_filings_clean.csv from data/raw/dob_major_jobs.csv.
"""
import re
import numpy as np
import pandas as pd

RAW_FILE = "data/raw/dob_major_jobs.csv"
DATA_DATE = pd.Timestamp("2026-09-23")     # latest current_status_date in the extract

WORK_FLAGS = ["sprinkler_work_type", "plumbing_work_type", "standpipe", "antenna", "sign", "curb_cut", "fence", "scaffold", "shed",
              "boiler_equipment_work_type_", "earth_work_work_type_", "foundation_work_type_", "general_construction_work_type_",
              "mechanical_systems_work_type_", "place_of_assembly_work_type_", "protection_mechanical_methods_work_type_",
              "sidewalk_shed_work_type_", "structural_work_type_", "support_of_excavation_work_type_",
              "temporary_place_of_assembly_work_type_", "green_roof_work_type_", "solar_work_type_",
              "full_demolition_work_type_", "suspended_scaffold_work_type_"]
DATES = ["filing_date", "approved_date", "first_permit_date", "signoff_date", "current_status_date"]
JOB_SHORT = {"New Building": "New Building", "Alteration CO": "Alteration CO",
             "ALT-CO - New Building with Existing Elements to Remain": "ALT-CO (NB with existing elements)",
             "Full Demolition": "Full Demolition"}
# Location identifiers that are not needed for the model and are not republished.
NOT_PUBLISHED = ["block", "lot", "bin", "latitude", "longitude", "census_tract", "postcode", "work_on_floor"]


def load_raw(path=RAW_FILE):
    return pd.read_csv(path, dtype=str)


def split_filing_number(df):
    """B00123456-I1 = the job's initial filing; -S1, -P1, -A1 ... are later subsequent / post-approval amendments."""
    out = df.copy()
    parts = out.job_filing_number.str.split("-", n=1, expand=True)
    out["job_number"], out["filing_suffix"] = parts[0], parts[1]
    out["is_initial"] = out.filing_suffix.eq("I1")
    return out


def dedupe(df):
    """128 filing numbers appear twice. Keep the row with the latest status date (the most recent state of the filing)."""
    tmp = df.assign(_s=pd.to_datetime(df.current_status_date, errors="coerce"))
    return tmp.sort_values("_s").drop_duplicates("job_filing_number", keep="last").drop(columns="_s")


def tidy(df):
    out = df.copy()
    for c in DATES:
        out[c] = pd.to_datetime(out[c], errors="coerce")
    out["filing_date"] = out.filing_date.dt.normalize()
    for c in ["initial_cost", "total_construction_floor_area", "existing_dwelling_units", "proposed_dwelling_units"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    for c in WORK_FLAGS + ["little_e"]:
        out[c] = out[c].fillna("").str.strip().str.upper().isin(["YES", "Y"]).astype(int)
    out["job_type"] = out.job_type.map(JOB_SHORT).fillna(out.job_type)
    out["job_description"] = out.job_description.fillna("").str.replace(r"\s+", " ", regex=True).str.strip()
    for c in ["borough", "building_type", "owner_type", "applicant_professional_title", "filing_review_type", "review_building_code", "nta"]:
        out[c] = out[c].fillna("Unknown").str.strip()
    return out


def add_outcome(df, data_date=DATA_DATE):
    """Survival outcome for each initial filing.
    event = 1 if DOB approved it; duration = days from filing to approval.
    event = 0 (censored) if it is still open: duration = days from filing to the data date. A withdrawn filing is censored
    at its last status date: we only know it had not been approved by then."""
    out = df.copy()
    appr = out.approved_date.dt.normalize()
    withdrawn = out.filing_status.eq("Filing Withdrawn") & appr.isna()
    end = np.where(appr.notna(), appr, np.where(withdrawn, out.current_status_date.dt.normalize(), data_date))
    out["event"] = appr.notna().astype(int)
    out["duration"] = (pd.to_datetime(end) - out.filing_date).dt.days
    out["withdrawn"] = withdrawn.astype(int)
    out["bad_dates"] = (out.duration < 0).astype(int)
    return out


def add_features(df, all_initial):
    """Only information available on the filing day."""
    out = df.copy()
    cost, area = out.initial_cost, out.total_construction_floor_area
    out["log_cost"] = np.log1p(cost.clip(lower=0))
    out["cost_zero"] = (cost.fillna(0) <= 0).astype(int)
    out["log_area"] = np.log1p(area.clip(lower=0))
    out["cost_per_sqft"] = np.where((cost > 0) & (area > 0), cost / area.where(area > 0), np.nan)
    out["units_added"] = (out.proposed_dwelling_units.fillna(0) - out.existing_dwelling_units.fillna(0))
    out["n_work_types"] = out[WORK_FLAGS].sum(axis=1)
    out["desc_words"] = out.job_description.str.split().str.len().fillna(0)
    out["filing_month"] = out.filing_date.dt.month
    out["pe_applicant"] = out.applicant_professional_title.str.upper().eq("PE").astype(int)
    out = out.join(workload(out, all_initial))
    return out


def workload(df, all_initial, window=30, active=180):
    """DOB's workload when the job was filed, per borough, using only information known that day:
    - filed_30d: plan-exam filings in the same borough in the previous 30 days
    - open_queue: plan-exam filings in the borough filed in the previous 180 days and not yet approved or withdrawn
      by that day. The 180-day window keeps long-abandoned filings (stuck in objections for years) out of the queue,
      otherwise the queue would only ever grow and act as a stand-in for the calendar date."""
    pe = all_initial[all_initial.filing_review_type.eq("Standard Plan Examination") & all_initial.filing_date.notna()]
    res = pd.DataFrame(index=df.index, columns=["filed_30d", "open_queue"], dtype=float)
    for b, g in df.groupby("borough"):
        p = pe[pe.borough == b]
        f = np.sort(p.filing_date.values.astype("datetime64[D]"))
        closed = p.approved_date.dt.normalize().fillna(p.current_status_date.where(p.filing_status.eq("Filing Withdrawn")).dt.normalize())
        fd = p.filing_date.values.astype("datetime64[D]")
        cd = closed.values.astype("datetime64[D]")
        t = g.filing_date.values.astype("datetime64[D]")
        filed_before = np.searchsorted(f, t, side="left")
        res.loc[g.index, "filed_30d"] = filed_before - np.searchsorted(f, t - np.timedelta64(window, "D"), side="left")
        q = []
        for ti in t:   # filed in [t-180, t) and not closed before t
            m = (fd < ti) & (fd >= ti - np.timedelta64(active, "D"))
            q.append(int((m & ~(cd < ti)).sum()))
        res.loc[g.index, "open_queue"] = q
    return res


def add_split(df):
    d = df.filing_date
    out = df.copy()
    # The first six months of DOB NOW filings are left out of modelling: the 180-day workload window needs history.
    out["split"] = np.select([d < "2021-09-01", d < "2024-01-01", d < "2024-07-01", d < "2025-07-01"],
                             ["warm-up (not modelled)", "train", "validation", "test"], "recent (not used for testing)")
    return out


def quality_report(raw, dedup, initial, final):
    pe = final[final.filing_review_type.eq("Standard Plan Examination")]
    return {
        "raw_rows": len(raw),
        "duplicate_filing_numbers": int(raw.job_filing_number.duplicated().sum()),
        "distinct_jobs": int(dedup.job_filing_number.str.split("-").str[0].nunique()),
        "initial_filings": len(initial),
        "initial_missing_filing_date": int(initial.filing_date.isna().sum()),
        "approved_before_filed": int(final.bad_dates.sum()),
        "plan_exam_initial_filings": len(pe),
        "plan_exam_approved_share": round(float(pe.event.mean()), 3),
        "plan_exam_withdrawn": int(pe.withdrawn.sum()),
        "declared_cost_zero_share": round(float(pe.cost_zero.mean()), 3),
        "filing_date_range": [str(final.filing_date.min().date()), str(final.filing_date.max().date())],
        "split_sizes_plan_exam": pe.split.value_counts().to_dict(),
    }
