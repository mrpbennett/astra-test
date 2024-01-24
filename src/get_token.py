import logging

import tomli
from authlib.integrations.requests_client import OAuth2Session
from requests.exceptions import HTTPError

# CONFIG FILE
with open("../config.toml", mode="rb") as conf:
    c = tomli.load(conf)


# Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(filename)s:%(funcName)s -> %(message)s",
)


# NPI API CLASS
class TokenGeneration:
    def __init__(self, token=None):
        self.token = token

    @staticmethod
    def get_user_token(username, password):
        """
        Generates user token for connection

        Params:
            - username (string): The users username
            - password (string): The users password

        Returns:
            Created user token via .fetch_token
        """
        try:
            if not c["pp_auth"]["client_id"] or not c["pp_auth"]["client_secret"]:
                raise ValueError("client_id or client_secret missing")

            client = OAuth2Session(
                c["pp_auth"]["client_id"], c["pp_auth"]["client_secret"]
            )

            return client.fetch_token(
                c["pp_auth"]["url"],
                authorization_response=c["pp_auth"]["url"],
                username=username,
                password=password,
                grant_type="password",
            )
        except HTTPError as err:
            logging.error(f"username={username}, {err}")
            raise err

    def return_client(self, token):
        """
        Creates client requiered to connect

        Params:
            - token (string): Returned token

        Returns
            OAuth2 Session
        """
        return OAuth2Session(
            c["pp_auth"]["client_id"],
            c["pp_auth"]["client_secret"],
            token=token,
        )

    def establish_connection(self, token):
        return self.return_client(token)
