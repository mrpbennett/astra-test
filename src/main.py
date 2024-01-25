import json
import logging
from datetime import datetime

import pandas as pd
import tomli

from create_npi_list import create_new_npi_list, generate_data_for_new_list
from getting_list_ids import get_all_npi_lists

# Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(filename)s:%(funcName)s -> %(message)s",
)

# CONFIG FILE
with open("../config.toml", mode="rb") as conf:
    c = tomli.load(conf)


def main():
    new_lists = []

    for index, row in generate_data_for_new_list(
        "../data/pulsepoint_az_test_file.csv"
    ).iterrows():
        # Create a dictionary for each row
        dict_entry = {"name": row.iloc[0], "npis": row.iloc[1]}
        # Append the dictionary to the list
        new_lists.append(dict_entry)

    create_new_npi_list(c["user"]["account_id"], new_lists).to_csv(
        f'../dumps/news_lists_{datetime.now().strftime("%Y-%m-%d")}.csv', index=False
    )


if __name__ == "__main__":
    main()
