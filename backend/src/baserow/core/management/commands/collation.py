from django.core.management.base import BaseCommand
from django.db import connection

from loguru import logger

EXPECTED_CHARSET = "UTF8"
BASEROW_COLLATION = "en-x-icu"


class Command(BaseCommand):
    help = "Displays the current charset and collation and checks if desired collation is available"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix",
            action="store_true",
            help="Will attempt to change the default collation",
        )

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT character_set_name, default_collate_name FROM information_schema.character_sets"
            )
            row = cursor.fetchone()
            current_character_set = row[0]
            current_default_collation = row[1]
            logger.info(f"Current character set: {current_character_set}")
            logger.info(f"Current default collation: {current_default_collation}")

            if options["fix"]:
                if current_default_collation == BASEROW_COLLATION:
                    logger.info("Correct collation is set already.")
                    return

                if current_character_set != EXPECTED_CHARSET:
                    logger.error(
                        f"Current database charset '{current_character_set}' is not '{EXPECTED_CHARSET}'"
                    )
                    return

                cursor.execute("SELECT * FROM pg_collation WHERE collname = 'blbost'")
                result = cursor.fetchone()
                if result is None:
                    logger.error(
                        f"Can't change the default collation. Collation not available."
                    )
