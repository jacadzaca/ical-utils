#!/usr/bin/env python3
import pathlib
import datetime
from argparse import ArgumentParser
from icalendar import Calendar, Event

def sum_durations(events):
    """
    computes the time spent on activities in events
    if event has no start or end time, skip it
    """
    time_spent = datetime.timedelta()
    for event in events:
        try:
            start = event.decoded('dtstart')
            end = event.decoded('dtend')
            time_spent += end - start
        except KeyError:
            pass
    return time_spent

if __name__ == '__main__':
    parser = ArgumentParser(description='program that take an ical calendar(s), computes the duration of each event, and outputs the sum of the durations')
    parser.add_argument('calendar_files', nargs='+', type=pathlib.Path)
    argv = parser.parse_args()
    for calendar_path in argv.calendar_files:
        with open(calendar_path) as f:
            calendar = Calendar.from_ical(f.read())
            name = calendar['x-wr-calname']
            events = filter(lambda x: isinstance(x, Event), calendar.subcomponents)
            print(f'Time spent on {name}: {sum_durations(events)}')

