import logging
import time

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
    """
    Generate a new DataFrame by grouping the data based on the 'line' column and creating a list of 'npi' values for each group.

    Args:
        data_loc (str): The file path of the CSV data.

    Returns:
        pd.DataFrame: The new DataFrame with grouped data.
    """
    df = pd.read_csv(data_loc)
    return df.groupby("line")["npi"].apply(list).reset_index()


def create_new_npi_list(account_id: int, new_lists: list) -> pd.DataFrame:
    """
    Create a new NPI list for a given account.

    Args:
        account_id (int): The ID of the account.
        new_lists (list): A list of dictionaries containing the new NPI lists to be created. Each dictionary should have the following keys:
            - name (str): The name of the list.
            - npis (list): A list of NPIs (National Provider Identifiers) to be included in the list.

    Raises:
        HTTPError: If there is an error while making the API request.

    Returns:
        None
    """
    conn = napi_token.establish_connection(token)

    list = {}
    newly_created_lists = []

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
                data = res.json()

                logging.info(
                    {
                        "id": data["id"],
                        "name": data["name"],
                        "npis": data["npis"],
                    }
                )

                newly_created_lists.append(
                    {
                        "id": data["id"],
                        "name": data["name"],
                    }
                )

                # sleep for 5 seconds to reduce request load
                time.sleep(5)

        except HTTPError as error:
            raise error

    return pd.DataFrame(newly_created_lists, columns=["id", "name"])
