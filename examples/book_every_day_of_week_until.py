"""
Nereo API script example
Book every {day of week} of a specific leave type
from {start_date} until {end_date}
"""

import argparse
import datetime
import requests

NEREO_API_BASE_URL = 'https://absences.nereo.com/api'


def parse_day_of_week(day_of_week):
    day_of_week = int(day_of_week)
    if (day_of_week < 1 or day_of_week > 7):
        raise argparse.ArgumentTypeError(
            'Day of week has to be between 1 and 7'
        )
    return day_of_week


def parse_iso_date(iso_date):
    return datetime.datetime.strptime(iso_date, '%Y-%m-%d').date()


# Define an argparser for command-line use
parser = argparse.ArgumentParser(
    description='Book every {day_of_week} of a specific \
    leave type {timed_account_id} until {end_date} on Nereo'
)
parser.add_argument(
    'token',
    help='Nereo API\'s authentication token'
)
parser.add_argument(
    'day_of_week',
    help='Day of the week you want to book where "1" \
    is Monday and "7" is Sunday',
    type=parse_day_of_week
)
parser.add_argument(
    'timed_account_id',
    help='ID of the Timed Account you want to book on',
    type=int
)
parser.add_argument(
    'start_date',
    help='Start date of the recursion in the format YYYY-MM-DD',
    type=parse_iso_date
)
parser.add_argument(
    'end_date',
    help='End date of the recursion in the format YYYY-MM-DD',
    type=parse_iso_date
)
args = parser.parse_args()

# Iterate from today until end_date on matching day_of_week
current_date = args.start_date
while (current_date <= args.end_date):
    if (current_date.isoweekday() == args.day_of_week):
        r = requests.post(
            '%s/leaverequests/quick/' % NEREO_API_BASE_URL,
            {
                'begin_date': current_date.isoformat(),
                'end_date': current_date.isoformat(),
                'morning_included': True,
                'afternoon_included': True,
                'timed_account': args.timed_account_id
            },
            headers={'Authorization': 'Token %s' % args.token}
        )
        if (r.status_code != 201):
            raise Exception(r.json())
        else:
            print('Request created for %s' % current_date.isoformat())
    current_date += datetime.timedelta(days=1)
