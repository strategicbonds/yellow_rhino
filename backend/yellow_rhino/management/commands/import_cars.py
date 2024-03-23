import csv
import os
import shutil
from django.core.management.base import BaseCommand, CommandError
from yellow_rhino.models import Car, CarRecord  # Adjust the import path as needed
from django.db.utils import IntegrityError
from datetime import date, datetime

class Command(BaseCommand):
    help = 'Import cars from CSV files, create Car or CarRecord as appropriate, and archive the files'

    def log_to_csv(self, log_message):
        log_file_path = r'C:\Users\tyler\OneDrive\Onedrive\Coding\yellow_rhino\get_cars_data\import_log.csv'
        with open(log_file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([log_message['date'], log_message['filename'], log_message['action'], log_message['details']])

    def handle(self, *args, **kwargs):
        directory = r'C:\Users\tyler\OneDrive\Onedrive\Coding\yellow_rhino\get_cars_data\cars_data'
        archive_directory = r'C:\Users\tyler\OneDrive\Onedrive\Coding\yellow_rhino\get_cars_data\cars_data\archive'

        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                # Extract the date part from the filename
                # Assuming filename format is 'cars_YYYYMMDD_HHMMSS.csv'
                date_str = filename.split('_')[1]  # This gets 'YYYYMMDD'
                source = filename.split('_')[0]  # This gets 'source'
                
                # Parse the date string into a datetime.date object
                record_date = datetime.strptime(date_str, '%Y%m%d').date()
                
                # Now you can use 'record_date' when creating a CarRecord
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        car, created = Car.objects.get_or_create(
                            vin=row['vin'],
                            defaults={
                                'make': row['make'],
                                'model': row['model'],
                                'year': row['year'],
                                'fuel_type': row['fueltype'],  
                                'packages': row['packages'],
                                'drive_type': row['driveType'],
                                'engine': row['engine'],
                                'color_ext': row['color_ext'],
                                'color_int': row['color_int'],
                                'transmission': row['transmission'],
                                'trim': row['trim'],
                            }
                        )

                        CarRecord.objects.create(
                            car=car,
                            price=row['price'],
                            mileage=int(float(row['mileage'])),  # Convert mileage to integer
                            date=record_date,  # Use the parsed date
                            source=source
                        )

                # After processing all rows, move the file to the archive directory
                shutil.move(filepath, os.path.join(archive_directory, filename))
                self.stdout.write(self.style.SUCCESS(f'Successfully processed {filename}'))
                if created:
                    log_detail = f'New car created with VIN {row["vin"]} and a corresponding record'
                else:
                    log_detail = f'New record added for car with VIN {row["vin"]}'

                log_message = {
                    'date': date.today().isoformat(),
                    'filename': filename,
                    'action': 'Car Data Update',
                    'details': log_detail
                }
                self.log_to_csv(log_message)

