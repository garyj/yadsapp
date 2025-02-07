from io import StringIO

import pytest
from django.core.management import call_command

pytestmark = pytest.mark.django_db


class TestPendingMigrations:
    """Test to make sure there are no pending migrations

    .. Django: Test for pending migrations: https://adamj.eu/tech/2024/06/23/django-test-pending-migrations/

    """

    def test_no_pending_migrations(self) -> None:
        out = StringIO()
        try:
            call_command(
                'makemigrations',
                '--dry-run',
                '--check',
                stdout=out,
                stderr=StringIO(),
            )
        except SystemExit:  # pragma: no cover
            raise AssertionError('Pending migrations:\n' + out.getvalue()) from None
