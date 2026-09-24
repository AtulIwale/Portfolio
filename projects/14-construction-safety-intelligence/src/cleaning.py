"""
Cleaning functions for Project 14: Construction Safety Intelligence.

Source: OSHA Severe Injury Reports, January 2015 to November 2025
        https://www.osha.gov/severe-injury-reports  ("Download the full SIR data set")
        File: January2015toNovember2025.csv (inside January2015toNovember2025.zip), 105,996 rows.

Each step is a small function so the notebook can show its effect one at a time.
Run `python src/clean.py` to rebuild data/osha_construction_clean.csv from the raw file.
"""
import re
import pandas as pd

RAW_FILE = "data/raw/January2015toNovember2025.csv"

# Columns dropped before anything is published. The data is public on osha.gov, but the
# portfolio does not need to name companies or pinpoint sites next to injuries.
PRIVATE_COLUMNS = ["Employer", "Address1", "Address2", "Zip", "Latitude", "Longitude", "UPA"]


# --------------------------------------------------------------------------------------
# 1. Load
# --------------------------------------------------------------------------------------
def load_raw(path=RAW_FILE):
    """OSHA publishes the file in Windows-1252 encoding. Everything is read as text first,
    so that codes such as NAICS '238160' keep their leading digits and nothing is guessed."""
    return pd.read_csv(path, encoding="cp1252", dtype=str)


# --------------------------------------------------------------------------------------
# 2. Keep construction only
# --------------------------------------------------------------------------------------
def filter_construction(df):
    """NAICS sector 23 = Construction. 18,994 rows carry a full 6-digit code; a few carry
    shorter codes (e.g. '2382'), which still start with 23 and are kept."""
    naics = df["Primary NAICS"].fillna("").str.strip()
    return df[naics.str.startswith("23")].copy()


# --------------------------------------------------------------------------------------
# 3. Types and tidy text
# --------------------------------------------------------------------------------------
TRADE_NAMES = {  # NAICS 4-digit industry groups within construction
    "2361": "Residential building", "2362": "Non-residential building",
    "2371": "Utility systems", "2372": "Land subdivision", "2373": "Highway, street and bridge",
    "2379": "Other heavy and civil", "2381": "Foundation, structure and exterior (incl. roofing, framing, concrete, steel)",
    "2382": "Building equipment (electrical, plumbing, HVAC)", "2383": "Building finishing (drywall, painting, flooring)",
    "2389": "Other specialty trades (site prep, demolition)",
}


def tidy(df):
    out = df.copy()
    out["event_date"] = pd.to_datetime(out["EventDate"], format="%m/%d/%Y", errors="coerce")
    for c in ["Hospitalized", "Amputation", "Loss of Eye"]:
        out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0).astype(int)
    out["naics"] = out["Primary NAICS"].str.strip()
    out["naics4"] = out["naics"].str[:4]
    out["trade"] = out["naics4"].map(TRADE_NAMES).fillna("Construction, not specified")
    out["state"] = out["State"].str.strip().str.title()
    out["inspected"] = out["Inspection"].notna().astype(int)
    for c in ["EventTitle", "NatureTitle", "Part of Body Title", "SourceTitle", "Secondary Source Title"]:
        out[c] = out[c].fillna("").str.strip().str.replace(r"\s+", " ", regex=True)
    out["narrative"] = out["Final Narrative"].fillna("").str.replace(r"\s+", " ", regex=True).str.strip()
    return out


# --------------------------------------------------------------------------------------
# 4. Remove employer names from the narratives
# --------------------------------------------------------------------------------------
SUFFIX = re.compile(r"[,.]?\s*\b(inc|llc|l\.l\.c|co|corp|corporation|company|ltd|lp|llp|pc|pllc)\b\.?", re.I)


def employer_variants(name):
    """'Tirone Electric, Inc.' -> ['Tirone Electric, Inc.', 'Tirone Electric']"""
    if not isinstance(name, str):
        return []
    name = name.strip()
    short = SUFFIX.sub("", name).strip(" ,.")
    return [v for v in dict.fromkeys([name, short]) if len(v) >= 5]


def redact_employer(narrative, employer):
    """Replace the reporting employer's own name with '[EMPLOYER]'. Returns (text, changed)."""
    new = narrative
    for v in employer_variants(employer):
        new = re.sub(re.escape(v), "[EMPLOYER]", new, flags=re.I)
    return new, new != narrative


def redact_all(df):
    out = df.copy()
    res = [redact_employer(n, e) for n, e in zip(out["narrative"], out["Employer"])]
    out["narrative"] = [r[0] for r in res]
    out["employer_redacted"] = [int(r[1]) for r in res]
    return out


# --------------------------------------------------------------------------------------
# 5. Cause groups from OSHA's event title
# --------------------------------------------------------------------------------------
# OSHA codes each injury with an OIICS "event or exposure" code. In construction alone there
# are 348 distinct codes, and the file mixes 2-, 3- and 4-digit codes from more than one
# version of the coding manual (the same 2-digit prefix can mean different things). The text
# title is consistent across versions, so the groups are assigned from the title, and the
# full code -> group table is saved to data/cause_group_map.csv for review.
GROUPS = [
    "Fall to lower level", "Slip, trip or same-level fall", "Struck by or against object", "Caught in or crushed",
    "Vehicle or mobile equipment", "Electrical", "Heat stress",
    "Fire, explosion or burn", "Other",
]
UNKNOWN = "Unknown (not usable)"

RULES = [  # order matters: the first matching rule wins
    (UNKNOWN, r"^nonclassifiable|^event or exposure unspecified|^contact with objects and equipment,? unspecified|^contact incidents unspecified|^contact with objects and equipment,? n\.e\.c|^contact with non-running objects or equipment unspecified"),
    ("Electrical", r"electric"),
    ("Heat stress", r"environmental heat"),
    ("Fire, explosion or burn", r"fire|explosion|ignition|flash|hot objects|controlled heat|blasting"),
    ("Vehicle or mobile equipment", r"pedestrian|jack-knifed|overturn|collision|roadway|transport incident|occupant|run over|rolling powered vehicle|aircraft|water vehicle|pedal cycle|transportation incident"),
    ("Fall to lower level", r"fall.*lower level|jump.*lower level|fall.*curtailed|fall through|fall from"),
    ("Caught in or crushed", r"caught|compressed|pinched|crushed|collaps|entangled|wedged|squeezed|cave-in"),
    ("Struck by or against object", r"struck by|struck against|slipping or swinging object|swinging or slipping object|rubbed|abraded|injured by (?:[a-z ]*)?object|injured by handheld"),
    ("Slip, trip or same-level fall", r"same level|slip|trip|stumble|fall while sitting"),
    ("Other", r".*"),
]


def cause_group(title):
    s = str(title).lower()
    for group, pattern in RULES:
        if re.search(pattern, s):
            return group
    return "Other"


FALL_BANDS = [  # OSHA puts the fall height band in the title of many fall codes
    (r"less than 6 feet", "Under 6 ft"), (r"6 to 10 feet", "6-10 ft"), (r"11 to 15 feet", "11-15 ft"),
    (r"16 to 20 feet", "16-20 ft"), (r"21 to 25 feet", "21-25 ft"), (r"26 to 30 feet", "26-30 ft"),
    (r"more than 30 feet|over 30 feet", "Over 30 ft"),
]


def fall_band(title):
    s = str(title).lower()
    for pattern, band in FALL_BANDS:
        if re.search(pattern, s):
            return band
    return ""


def add_labels(df):
    out = df.copy()
    out["cause_group"] = out["EventTitle"].map(cause_group)
    out["fall_band_osha"] = out["EventTitle"].map(fall_band)
    out["severity"] = out.apply(lambda r: "Amputation" if r["Amputation"] > 0 or r["Loss of Eye"] > 0
                                else ("Hospitalised" if r["Hospitalized"] > 0 else "Other severe"), axis=1)
    out["split"] = pd.cut(out["event_date"].dt.year, [2014, 2022, 2023, 2026], labels=["train", "validation", "test"]).astype(str)
    return out


def cause_map_table(df):
    t = (df.assign(code=df["Event"].str.strip())
           .groupby(["cause_group", "code", "EventTitle"]).size().reset_index(name="reports")
           .sort_values(["cause_group", "reports"], ascending=[True, False]))
    return t


# --------------------------------------------------------------------------------------
# 6. Final table
# --------------------------------------------------------------------------------------
KEEP = ["ID", "event_date", "split", "state", "naics", "naics4", "trade", "narrative", "employer_redacted",
        "Hospitalized", "Amputation", "Loss of Eye", "severity", "inspected",
        "Event", "EventTitle", "cause_group", "fall_band_osha",
        "Nature", "NatureTitle", "Part of Body", "Part of Body Title", "Source", "SourceTitle",
        "Secondary Source", "Secondary Source Title"]


def final_table(df):
    out = df[KEEP].rename(columns={"ID": "report_id", "Hospitalized": "hospitalised", "Amputation": "amputations",
                                   "Loss of Eye": "loss_of_eye", "Event": "event_code", "EventTitle": "event_title",
                                   "Nature": "nature_code", "NatureTitle": "nature", "Part of Body": "body_part_code",
                                   "Part of Body Title": "body_part", "Source": "source_code", "SourceTitle": "source",
                                   "Secondary Source": "secondary_source_code", "Secondary Source Title": "secondary_source"})
    out["event_date"] = out["event_date"].dt.strftime("%Y-%m-%d")
    out["event_code"] = out["event_code"].str.strip()
    return out.sort_values(["event_date", "report_id"]).reset_index(drop=True)


def quality_report(raw, con, final):
    """Numbers quoted in the README. Everything is recomputed from the raw file."""
    return {
        "raw_rows": len(raw),
        "construction_rows": len(con),
        "date_min": final["event_date"].min(), "date_max": final["event_date"].max(),
        "bad_dates": int(pd.to_datetime(con["EventDate"], format="%m/%d/%Y", errors="coerce").isna().sum()),
        "event_codes_distinct": int(con["Event"].str.strip().nunique()),
        "event_code_lengths": con["Event"].str.strip().str.len().value_counts().sort_index().to_dict(),
        "duplicate_narratives": int(con["Final Narrative"].duplicated().sum()),
        "missing_secondary_source": int(con["Secondary Source"].isna().sum()),
        "short_narratives_under_40_chars": int((final["narrative"].str.len() < 40).sum()),
        "employer_names_redacted": int(final["employer_redacted"].sum()),
        "unknown_cause": int((final["cause_group"] == UNKNOWN).sum()),
        "cause_groups": final["cause_group"].value_counts().to_dict(),
        "split_sizes": final["split"].value_counts().to_dict(),
    }
