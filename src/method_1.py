import logging
from typing import Literal

import pandas as pd
import requests
import tomli
from requests.exceptions import HTTPError

from get_token import TokenGeneration

with open("../config.toml", mode="rb") as conf:
    c = tomli.load(conf)

# LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(filename)s:%(funcName)s -> %(message)s",
)

# Token Generation
napi_token = TokenGeneration()
token = napi_token.get_user_token(c["user"]["username"], c["user"]["password"])


def generate_data_for_new_list(data_loc: str) -> pd.DataFrame:
    df = pd.read_csv(data_loc)
    return df.groupby("line")["npi"].apply(list).reset_index()


def create_new_npi_list(account_id: int, new_lists: list):
    conn = napi_token.establish_connection(token)

    list = {}

    for l in new_lists:
        list = {
            "name": l["name"],
            "npis": l["npis"],
            "advertisers": ["TAMTESTING ACCOUNT"],
        }

        try:
            res = conn.post(
                f"https://lifeapi.pulsepoint.com/RestApi/v1/npi/npi-list/account/{account_id}",
                json=list,
            )
            res.raise_for_status()

            if res.status_code == requests.codes.ok:
                logging.info(f"New list created: {res.json()}")

        except HTTPError as error:
            raise error
