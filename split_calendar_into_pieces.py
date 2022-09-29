#!/usr/bin/env python3
import pathlib
from argparse import ArgumentParser
from icalendar import Calendar, Event, vText

def create_calendar(items):
    calendar = Calendar(items)
    calendar['prodid'] = vText('split-calendar-into-pieces')
    return calendar

def main(argv):
    created_calendars = []
    with open(argv.input_file) as f:
        input_calendar = Calendar.from_ical(f.read())

    calendar = create_calendar(input_calendar.items())
    for i, event in enumerate(input_calendar.walk('vevent')):
        if i % argv.pieces_number == 0:
            created_calendars.append(calendar)
            calendar = create_calendar(input_calendar.items())
        calendar.add_component(event)

    for i, calendar in enumerate(created_calendars):
        with open(f'{argv.input_file}_{i}.ics', 'wb+') as f:
            f.write(calendar.to_ical())

if __name__ == '__main__':
    parser = ArgumentParser(description='Split an ical calendar into several smaller calendars with a fixed number of events (for example, Google Calendar rejects too big imports)')
    parser.add_argument('input_file', type=pathlib.Path)
    parser.add_argument('pieces_number', type=int)
    main(parser.parse_args())
