import os

# Set test defaults if they are not available in the environment
# This works well when running the tests on a local machine.
# As well as in CI and Docker where we can override the environment variables


if not os.getenv('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'A_NOT_SO_SECRET_DEFAULT_KEY'  # noqa: S105

if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///db.sqlite3'

from config.settings.base import *
