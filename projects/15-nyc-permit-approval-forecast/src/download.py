"""
Download the raw extract used in Project 15 from NYC Open Data (Socrata API, no key needed).

    python src/download.py            -> data/raw/dob_major_jobs.csv (about 80 MB, ~131,500 rows)

Applicant and owner names, house numbers and street names are deliberately not requested.
If your network blocks scripted downloads, open the printed URL in a browser and save the file as
data/raw/dob_major_jobs.csv.
"""
import os
import urllib.parse
import urllib.request

COLUMNS = ("job_filing_number,filing_status,borough,block,lot,bin,commmunity_board,council_district,census_tract,nta,postcode,"
           "latitude,longitude,job_type,filing_review_type,building_type,existing_dwelling_units,proposed_dwelling_units,initial_cost,"
           "total_construction_floor_area,review_building_code,little_e,work_on_floor,owner_type,applicant_professional_title,"
           "sprinkler_work_type,plumbing_work_type,standpipe,antenna,sign,curb_cut,fence,scaffold,shed,boiler_equipment_work_type_,"
           "earth_work_work_type_,foundation_work_type_,general_construction_work_type_,mechanical_systems_work_type_,"
           "place_of_assembly_work_type_,protection_mechanical_methods_work_type_,sidewalk_shed_work_type_,structural_work_type_,"
           "support_of_excavation_work_type_,temporary_place_of_assembly_work_type_,green_roof_work_type_,solar_work_type_,"
           "full_demolition_work_type_,suspended_scaffold_work_type_,job_description,filing_date,current_status_date,"
           "first_permit_date,approved_date,signoff_date")
WHERE = "job_type in('New Building','Alteration CO','ALT-CO - New Building with Existing Elements to Remain','Full Demolition')"
URL = ("https://data.cityofnewyork.us/resource/w9ak-ipjd.csv?" +
       urllib.parse.urlencode({"$select": COLUMNS, "$where": WHERE, "$order": "job_filing_number", "$limit": 200000}))

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    print("Downloading:", URL)
    urllib.request.urlretrieve(URL, "data/raw/dob_major_jobs.csv")
    print("Saved data/raw/dob_major_jobs.csv")
