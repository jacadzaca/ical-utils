#!/usr/bin/env python3
import sys
import signal
import pathlib
import itertools
import datetime
from argparse import ArgumentParser
from icalendar import Calendar, Event, vText

def display_event(event):
    timezone = datetime.datetime.utcnow().astimezone().tzinfo
    start = None
    end = None
    try:
        start = event.decoded('dtstart').astimezone(timezone).strftime('%c')
        end = event.decoded('dtend').astimezone(timezone).strftime('%c')
    except KeyError:
        pass
    return f"name: {event['summary']}\nstart: {start}\nend: {end}"

def create_calendar(name, items):
    try:
        with open(f'{name}.ics') as f:
            return Calendar.from_ical(f.read())
    except FileNotFoundError:
        calendar = Calendar(items)
        calendar['prodid'] = vText('split-calendar')
        calendar['x-wr-calname'] = vText(name)
        return calendar

def quit(calendars, last_event_index):
    for calendar in calendars:
        name = calendar['x-wr-calname']
        with open(f'{name}.ics', 'wb') as f:
            f.write(calendar.to_ical())

    print(f'If you wish to continue splitting this calendar, run same the command setting --start set: {last_event_index}')
    sys.exit(0)

def input_int(prompt, input_range):
    x = ''
    while not isinstance(x, int) or x not in input_range:
        try:
            x = int(input(prompt))
        except ValueError:
            pass
    return x

if __name__ == '__main__':
    parser = ArgumentParser(description='Split an ical calendar into several smaller calendars with the help of a simple TUI')
    parser.add_argument('-s', '--start', type=int, help='from which event should the splitting start? Usually used when you want to resume the splitting', default=0)
    parser.add_argument('calendar_names', nargs='+', help='how to name the new calendars? If you wish to use an existing calendar, pass the filename (without the .ics extension)')
    parser.add_argument('calendar_file', type=pathlib.Path)
    argv = parser.parse_args()
    current_event_index = argv.start

    events = None
    calendars = None
    with open(argv.calendar_file) as f:
        calendar = Calendar.from_ical(f.read())
        calendars = [create_calendar(name, calendar.items()) for name in argv.calendar_names]
        events = itertools.islice(filter(lambda x: isinstance(x, Event), calendar.subcomponents), current_event_index, None)

    prompt = f'Pick a calendar:\n'
    prompt += '\n'.join([f'\t{i} for {name}' for i, name in enumerate(argv.calendar_names)])
    prompt += '\nPress ctrl-c to exit\n'

    signal.signal(signal.SIGINT, lambda _, __: quit(calendars, current_event_index))

    for event in events:
        print(display_event(event))
        calendar_choice = input_int(prompt, range(len(argv.calendar_names)))
        calendars[calendar_choice].add_component(event)
        current_event_index += 1
    print('Calendar has been split. Exiting...')

