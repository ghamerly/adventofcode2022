#!/usr/bin/env python3

# List solution events in time order (per task) from the AoC API JSON; can merge
# multiple JSON files.

import sys
import json
import datetime

def events(obj):
    '''Generate a list of solution events with the day, which star it is, the
    timestamp (in seconds from the unix epoch), and person's name.'''
    for member_id, member in obj['members'].items():
        name = member['name']
        for day_id, day in member['completion_day_level'].items():
            for level_id, level in day.items():
                yield (int(day_id), int(level_id), level['get_star_ts'], name)

def main():
    # gather all the events, merge them, deduplicate them
    all_events = []
    for f in sys.argv[1:]:
        print(f)
        with open(f) as file_contents:
            obj = json.load(file_contents)
        e = list(events(obj))
        all_events.extend(e)

    # remove duplicates from the same user across multiple leaderboards, map
    # each tuple to a list (so we can modify it later), and sort
    all_events = sorted(map(list, set(all_events)))

    # print everything
    last_task = None
    min_completion = None
    for e in all_events:
        task = e[0:2]
        if task != last_task:
            print()
            last_task = task
            min_completion = e[2]
            e[2] = datetime.datetime.fromtimestamp(min_completion).isoformat()
        else:
            d = e[2] - min_completion
            if d <= 3 * 60:
                e[2] = f'+{d} seconds'
            elif d <= 120 * 60:
                e[2] = f'+{d // 60} minutes'
            elif d <= 48 * 60 * 60:
                e[2] = f'+{d // (60 * 60)} hours'
            else:
                e[2] = f'+{d // (24 * 60 * 60)} days'
        print(e)

if __name__ == '__main__':
    main()
