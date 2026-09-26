import os

from dotenv import load_dotenv


load_dotenv()


def test_required_environment_variables():
    required = [
        "DB_HOST",
        "DB_PORT",
        "DB_USER",
        "DB_NAME",
    ]

    missing = [
        name
        for name in required
        if not os.getenv(name)
    ]

    assert not missing
