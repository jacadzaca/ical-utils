## About
This repository contains small programs that can help you mange your calendar (ical)

- a [program](https://raw.githubusercontent.com/jacadzaca/ical-utils/main/split_calendar_interactive.py) that iterates over all events in your calendar and asks you to which calendar it should be alloted.
- a [program](https://raw.githubusercontent.com/jacadzaca/ical-utils/main/split_calendar.py) that allotes events in your big calendar based on a mapping file
- a [program](https://raw.githubusercontent.com/jacadzaca/ical-utils/main/time_spent.py) that tells you how much time you've alloted in your calendar.
- a [program](https://raw.githubusercontent.com/jacadzaca/ical-utils/main/split_calendar_into_pieces.py) to split an ical calendar into several smaller calendars with a fixed number of events (for example, Google Calendar rejects too big imports, so that's useful)

## Generate the mapping file
You can extract all your events' names from your calendar with this command:

```bash
grep 'SUMMARY' calendar.ics | cut -d ':' -f2 | sort -u | tr "\r" "\n" | awk NF > events.txt
```
Then, you can edit the events.txt file with your [favourite text editor](https://neovim.io/) and append the name of the calendar
at the end of each line, so the program can split your big ical file.

