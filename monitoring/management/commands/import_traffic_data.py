import csv
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from monitoring.models import RoadSegment, SpeedReading


class Command(BaseCommand):
    help = "Import traffic speed data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to CSV file")
        parser.add_argument(
            "--start-date",
            type=str,
            default="2023-01-01",
            help="Start date for timestamps (YYYY-MM-DD). Default: 2023-01-01",
        )
        parser.add_argument(
            "--hours-apart",
            type=int,
            default=1,
            help="Hours between readings. Default: 1",
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        start_date_str = options["start_date"]
        hours_apart = options["hours_apart"]

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        start_date = timezone.make_aware(start_date)

        current_timestamp = start_date

        segments_created = 0
        segments_existing = 0
        readings_created = 0
        errors = 0

        self.stdout.write(self.style.SUCCESS(f"Starting import from {csv_file}"))

        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row_num, row in enumerate(
                    reader, start=2
                ):  # 1-indexed, start at 2 (header is 1)
                    try:
                        # Extract data from CSV row
                        start_long = Decimal(row["Long_start"])
                        start_lat = Decimal(row["Lat_start"])
                        end_long = Decimal(row["Long_end"])
                        end_lat = Decimal(row["Lat_end"])
                        length = Decimal(row["Length"])
                        speed = Decimal(row["Speed"])

                        # Get or create RoadSegment
                        # Using get_or_create with coordinates to handle duplicates
                        segment, segment_created = RoadSegment.objects.get_or_create(
                            start_longitude=start_long,
                            start_latitude=start_lat,
                            end_longitude=end_long,
                            end_latitude=end_lat,
                            defaults={
                                "length": length,
                            },
                        )

                        if segment_created:
                            segments_created += 1
                        else:
                            segments_existing += 1

                        # Create SpeedReading
                        # Check if reading already exists for this segment and timestamp
                        reading, reading_created = SpeedReading.objects.get_or_create(
                            road_segment=segment,
                            timestamp=current_timestamp,
                            defaults={
                                "average_speed": speed,
                            },
                        )

                        if reading_created:
                            readings_created += 1

                        current_timestamp += timedelta(hours=hours_apart)

                    except Exception as e:
                        errors += 1
                        self.stdout.write(
                            self.style.WARNING(f"Error on row {row_num}: {str(e)}")
                        )
                        continue

            self.stdout.write(
                self.style.SUCCESS(
                    f"\nImport completed!\n"
                    f"Segments created: {segments_created}\n"
                    f"Segments existing: {segments_existing}\n"
                    f"Readings created: {readings_created}\n"
                    f"Errors: {errors}"
                )
            )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
