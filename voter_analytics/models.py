from django.db import models
import csv
from datetime import datetime
from django.conf import settings
import os
from .constants import PARTY_AFFILIATION_MAP


class Voter(models.Model):
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField(default="N/A", blank=True)
    zip_code = models.TextField()
    date_of_birth = models.DateField()

    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.TextField()

    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()

    voter_score = models.IntegerField(default=0)

    def __str__(self):
        """return a string representation of this model instance"""
        return f"{self.first_name} {self.last_name}"


def load_data():
    """Load data records from a CSV file into model instances."""

    # delete all records: clear out the database:
    Voter.objects.all().delete()

    # open the file for reading:
    filename = "/Users/ahmadsadiq/Documents/cs412-restaurant/newton_voters.csv"
    with open(filename) as f:
        headers = f.readline()  # read/discard the headers

        # loop to read all the lines in the file
        for line in f:
            try:
                fields = line.split(",")  # create a list of fields

                # parse date fields
                dob = (
                    datetime.strptime(fields[7], "%Y-%m-%d").date()
                    if fields[7]
                    else None
                )
                dor = (
                    datetime.strptime(fields[8], "%Y-%m-%d").date()
                    if fields[8]
                    else None
                )

                # create a new instance of Voter object with this record from CSV
                voter = Voter(
                    first_name=fields[2],
                    last_name=fields[1],
                    street_number=int(fields[3]) if fields[3].isdigit() else None,
                    street_name=fields[4],
                    apartment_number=fields[5] if fields[5] else None,
                    zip_code=fields[6],
                    date_of_birth=dob,
                    date_of_registration=dor,
                    party_affiliation=fields[9].strip(),
                    precinct_number=fields[10],
                    v20state=fields[11],
                    v21town=fields[12],
                    v21primary=fields[13],
                    v22general=fields[14],
                    v23town=fields[15],
                    voter_score=(
                        int(fields[16].strip()) if fields[16].strip().isdigit() else 0
                    ),
                )

                voter.save()  # save this instance to the database
                print(f"Created voter: {voter}")

            except Exception as e:
                print(f"Exception on {fields}: {e}")
