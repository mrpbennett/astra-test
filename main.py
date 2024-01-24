import logging
from datetime import datetime

import tomli

from npi_class import TokenGeneration

# Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(filename)s:%(funcName)s -> %(message)s",
)

# CONFIG FILE
with open("config.toml", mode="rb") as conf:
    c = tomli.load(conf)


# CURRENT TIME
now = datetime.now()
current_time = now.strftime("%H:%M:%S")


# Token Generation
napi_token = TokenGeneration()


def main():
    token = napi_token.get_user_token(c["user"]["username"], c["user"]["password"])
    print(token)


if __name__ == "__main__":
    main()
