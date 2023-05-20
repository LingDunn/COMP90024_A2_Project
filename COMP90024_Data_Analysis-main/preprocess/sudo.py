import re
import csv
import json


states = ['new south wales',
          'victoria',
          'queensland',
          'south australia',
          'western australia',
          'tasmania',
          'northern territory',
          'australian capital territory',
          'Other Territories'
          ]

state_gcc = {'1gsyd': 'new south wales',
             '2gmel': 'victoria',
             '3gbri': 'queensland',
             '4gade': 'south australia',
             '5gper': 'western australia',
             '6ghob': 'tasmania',
             '7gdar': 'northern territory',
             '8acte': 'australian capital territory'
             }


def load_save_state_avg():
    input_file = "../sudo/state-avg.csv"
    output_file = "../sudo/state-avg.json"
    data = []

    # inc: income
    # fam: family
    # psn: person
    # hhd: household

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            gcc = row[" gccsa_code_2021"]
            if gcc.lower() in state_gcc.keys():
                state = state_gcc[gcc.lower()]
            else:
                continue
            item = {
                "state": state,
                "med_age": int(row[" median_age_persons"]),
                "med_month_mortgage": int(row[" median_mortgage_repay_monthly"]),
                "med_week_inc": int(row[" median_tot_prsnl_inc_weekly"]),
                "med_week_rent": int(row[" median_rent_weekly"]),
                "med_week_fam_inc": int(row[" median_tot_fam_inc_weekly"]),
                "avg_num_psn_per_bd": float(row[" average_num_psns_per_bedroom"]),
                "med_week_hhd_inc": int(row["median_tot_hhd_inc_weekly"]),
                "avg_hhd_size": float(row[" average_household_size"])
            }
            data.append(item)

    with open(output_file, "w") as f:
        json.dump(data, f)


def load_save_suburb_stat():
    input_file = "../sudo/suburb-stat.csv"
    output_file = "../sudo/suburb-stat.json"
    data = []
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            state = states[int(row[" ssc2011"][0]) - 1]
            suburb = row[" ssc_name"]
            suburb = re.match(r'^([^(]+)', suburb).group(1).strip().lower()

            item = {
                "state": state,
                "suburb": suburb,
                "med_inc": row[" median11"],
                "uni_rate": row[" uni"],
                "y12_rate": row[" y12"],
                "part_rate": row[" part_rate"],
                "tafe_rate": row[" cert"],
                "emp_rate": row["emp_to_pop"],
                "female_part": row[" female_par"],
                "male_part": row[" male_part_"],
                "part_less": row[" male_less_"]
            }
            data.append(item)

    with open(output_file, "w") as f:
        json.dump(data, f)


load_save_state_avg()
# load_save_suburb_stat()
