# !usr/bin/src python

import fire
from db import create_db, populate_db


if __name__ == "__main__":
    fire.Fire({"create": create_db, "populate": populate_db})
