import json
import logging
from datetime import datetime

import tomli

from create_npi_list import create_new_npi_list, generate_data_for_new_list
from get_token import TokenGeneration
from getting_list_ids import get_all_npi_lists

# Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(filename)s:%(funcName)s -> %(message)s",
)

# CONFIG FILE
with open("../config.toml", mode="rb") as conf:
    c = tomli.load(conf)


# CURRENT TIME
now = datetime.now()
current_time = now.strftime("%H:%M:%S")


# Token Generation
napi_token = TokenGeneration()


def main():
    new_lists = []

    for index, row in generate_data_for_new_list("../data/method_1.csv").iterrows():
        # Create a dictionary for each row
        dict_entry = {"name": row.iloc[0], "npis": row.iloc[1]}
        # Append the dictionary to the list
        new_lists.append(dict_entry)

    create_new_npi_list(c["user"]["account_id"], new_lists)

    # GETTING LISTS FROM ACCOUNT
    all_lists = get_all_npi_lists(c["user"]["account_id"], len(new_lists))

    # Prints only the lists that were created
    print(json.dumps(all_lists, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
