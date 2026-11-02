"""Independent daily-event oracle by Nova (GPT, OpenAI), 2026-11-02."""
import json
from pathlib import Path


def schedule(stagger=14):
    cohorts = []
    occupancy = {}
    collisions = []
    events = []
    heads = 0
    for day in range(200):
        # Release before admitting the replacement on the same day.
        for c in cohorts:
            if c.get('harvest') == day:
                heads += 6
                for port in c['ports']:
                    if occupancy.get(port) == c['name']:
                        del occupancy[port]
                events.append(dict(day=day, kind='harvest', cohort=c['name']))
        for c in cohorts:
            if c['seed'] + 14 == day:
                c['entry'] = day
                c['harvest'] = day + 28
                for port in c['ports']:
                    if port in occupancy:
                        collisions.append(dict(day=day, port=port, outgoing=occupancy[port], incoming=c['name']))
                    occupancy[port] = c['name']
                events.append(dict(day=day, kind='entry', cohort=c['name']))
        if day % stagger == 0 and len(cohorts) < 8:
            idx = len(cohorts)
            c = dict(name=chr(65+idx), seed=day, ports=list(range(5,11)) if idx%2==0 else list(range(11,17)))
            cohorts.append(c)
            events.append(dict(day=day, kind='seed', cohort=c['name']))
    return dict(stagger=stagger, cohorts=cohorts, events=events,
                collisions=collisions, total_heads=heads)


if __name__ == '__main__':
    result = dict(baseline=schedule(14), stagger7=schedule(7))
    base = result['baseline']
    assert [c['harvest'] for c in base['cohorts']] == list(range(42,141,14))
    assert base['total_heads'] == 48 and not base['collisions']
    assert result['stagger7']['collisions']
    Path(__file__).with_name('expected.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Own oracle: baseline 8 cohorts / days 42..140 / 48 heads / no collisions; stagger7 has collisions.')
