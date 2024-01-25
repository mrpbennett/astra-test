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
token_inst = TokenGeneration()
token = token_inst.get_user_token(c["user"]["username"], c["user"]["password"])


def get_all_npi_lists(account_id: str) -> dict:
    """
    Retrieves a specified number of NPI lists associated with the given account ID.

    Args:
        account_id (str): The ID of the account.
        num_to_extract (int): The number of NPI lists to extract.

    Returns:
        list: A list of dictionaries containing the ID and name of the NPI lists.
    """
    conn = token_inst.establish_connection(token)
    data = {}

    try:
        res = conn.get(
            f"https://lifeapi.pulsepoint.com/RestApi/v1/npi/npi-list/account/{account_id}",
        )
        res.raise_for_status()

        if res.status_code == requests.codes.ok:
            data = res.json()

    except HTTPError as error:
        raise error

    return data
