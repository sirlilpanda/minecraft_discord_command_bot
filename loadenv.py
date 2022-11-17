from pprint import pprint
from typing import Any

def load_env(path: str) -> dict[str, str]:
    with open(path, "r+") as txt:
        info = txt.readlines()
        return {k.strip():v.strip() for (k,v) in [x.split("=", 1) for x in info]}

if __name__ == "__main__":
    print(load_env(".env"))