#!/usr/bin/env python3
import pathlib
from argparse import ArgumentParser
from icalendar import Calendar, Event, vText

def create_calendar(name, items):
    calendar = Calendar(items)
    calendar['prodid'] = vText('split-calendar')
    calendar['x-wr-calname'] = vText(name.strip())
    return calendar

if __name__ == '__main__':
    parser = ArgumentParser(description='Split an ical calendar into several smaller calendars')
    parser.add_argument('calendar_file', type=pathlib.Path)
    parser.add_argument('mapping_file', type=pathlib.Path, help="the file containg the mappings of event names' to calendar names. One mapping per line. Format: [event_name][SPACE][calendar_name]\\n. An event's name can contain spaces")
    argv = parser.parse_args()

    mapping = {}
    with open(argv.mapping_file) as f:
        for line in f.readlines():
            words = line.split(' ')
            mapping[' '.join(words[0:-1]).strip()] = words[-1]
    names = set(mapping.values())

    events = None
    calendars = None
    with open(argv.calendar_file) as f:
        calendar = Calendar.from_ical(f.read())
        calendars = {name:create_calendar(name, calendar.items()) for name in names}
        events = filter(lambda x: isinstance(x, Event), calendar.subcomponents)

    for event in events:
        event_name = event.decoded('summary').decode('utf-8').strip()
        calendars[mapping[event_name]].add_component(event)

    for calendar in calendars.values():
        name = calendar['x-wr-calname']
        with open(f'{name}.ics', 'wb') as f:
            f.write(calendar.to_ical())

