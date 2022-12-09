import sys
from pathlib import Path
from dotenv import dotenv_values
from log import Logger

path = Path(__file__).parent.parent

def load_env():
    sys.stdout = Logger()
    
    # Essential env variables
    envs = ["BINARY_EXECUTABLE", "USER", "KEY", "SQL_USER_NAME", "SQL_USER_PASS", "SQL_HOST"]

    if path / ".env" not in path.iterdir():
        print(f"==>\n.env file not found in: \n{path}\n<==")
        exit()

    config = dotenv_values(path / ".env")

    for env in envs:
        try:
            _ = config[env]
        except KeyError:
            print(f"{env} not found in .env file")
    
    return config

config = load_env()

    
if __name__ == '__main__':
    load_env()
