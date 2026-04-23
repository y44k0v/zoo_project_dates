"""
animals/management/commands/import_animals_csv.py
--------------------------------------------------
Django management command that reads animals_data.csv and bulk-inserts
the records into the Animal table.

Place this file at:
    animals/
    └── management/
        ├── __init__.py
        └── commands/
            ├── __init__.py
            └── import_animals_csv.py

Usage (from the project root, with the virtualenv active):
    python manage.py import_animals_csv
    python manage.py import_animals_csv --file path/to/other.csv
    python manage.py import_animals_csv --clear   # wipe table first
"""

import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_date

from animals.models import Animal


class Command(BaseCommand):
    help = "Import animals from a CSV file into the Animal table."

    # ------------------------------------------------------------------
    # CLI argument definition
    # ------------------------------------------------------------------
    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="animals_data.csv",
            help="Path to the CSV file (default: animals_data.csv in the project root).",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing Animal records before importing.",
        )

    # ------------------------------------------------------------------
    # Main handler
    # ------------------------------------------------------------------
    def handle(self, *args, **options):
        csv_path = Path(options["file"])

        if not csv_path.exists():
            raise CommandError(f"File not found: {csv_path.resolve()}")

        if options["clear"]:
            deleted, _ = Animal.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing animal(s)."))

        animals_to_create = []
        errors = []

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            required_columns = {"name", "age", "weight", "born_in_captivity", "date_added"}
            if not required_columns.issubset(set(reader.fieldnames or [])):
                missing = required_columns - set(reader.fieldnames or [])
                raise CommandError(f"CSV is missing required columns: {missing}")

            for line_num, row in enumerate(reader, start=2):  # start=2 because row 1 is the header
                try:
                    name = row["name"].strip()
                    if not name:
                        raise ValueError("'name' is empty.")

                    age = int(row["age"])
                    if age < 0:
                        raise ValueError(f"'age' must be non-negative, got {age}.")

                    weight = float(row["weight"])
                    if weight <= 0:
                        raise ValueError(f"'weight' must be positive, got {weight}.")

                    # Accept True/False/true/false/1/0/yes/no
                    raw_captivity = row["born_in_captivity"].strip().lower()
                    if raw_captivity in ("true", "1", "yes"):
                        born_in_captivity = True
                    elif raw_captivity in ("false", "0", "no"):
                        born_in_captivity = False
                    else:
                        raise ValueError(
                            f"'born_in_captivity' must be True/False, got '{row['born_in_captivity']}'."
                        )

                    date_added = parse_date(row["date_added"].strip())
                    if date_added is None:
                        raise ValueError(
                            f"'date_added' could not be parsed: '{row['date_added']}'. "
                            "Expected YYYY-MM-DD."
                        )

                    animals_to_create.append(
                        Animal(
                            name=name,
                            age=age,
                            weight=weight,
                            born_in_captivity=born_in_captivity,
                            date_added=date_added,
                        )
                    )

                except (ValueError, KeyError) as exc:
                    errors.append(f"  Line {line_num}: {exc}")

        # Report any row-level errors but do not abort the whole import
        if errors:
            self.stdout.write(self.style.ERROR("Skipped rows with errors:"))
            for err in errors:
                self.stdout.write(self.style.ERROR(err))

        if not animals_to_create:
            raise CommandError("No valid rows found in the CSV. Nothing was imported.")

        # bulk_create inserts all rows in a single SQL statement — much
        # faster than calling Animal.objects.create() in a loop.
        created = Animal.objects.bulk_create(animals_to_create)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {len(created)} animal(s) from '{csv_path}'."
            )
        )
