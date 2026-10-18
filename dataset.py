import pandas as pd

def load_transport_data():
    # using mins from midnight so its easier to subtract
    # 480 = 8:00 AM, 510 = 8:30 AM, 540 = 9:00 AM, 600 = 10:00 AM
    raw_data = {
        'route': [
            'R101', 'R101', 'R101', 'R101', 'R101',
            'R202', 'R202', 'R202', 'R202', 'R202',
            'R305', 'R305', 'R305', 'R305', 'R305',
            'R404', 'R404', 'R404', 'R404', 'R404'
        ],
        'day': [
            'Mon', 'Tue', 'Wed', 'Thu', 'Fri',
            'Mon', 'Tue', 'Wed', 'Thu', 'Fri',
            'Mon', 'Tue', 'Wed', 'Thu', 'Fri',
            'Mon', 'Tue', 'Wed', 'Thu', 'Fri'
        ],
        'sched_time': [
            480, 480, 480, 480, 480,
            510, 510, 510, 510, 510,
            540, 540, 540, 540, 540,
            600, 600, 600, 600, 600
        ],
        # R101 = mostly on time
        # R202 = one massive delay on wednesday (outlier)
        # R305 = always late
        # R404 = inconsistent (late twice a week)
        'actual_time': [
            482, 480, 481, 478, 483,
            512, 510, 575, 511, 513,
            555, 560, 552, 558, 565,
            602, 620, 601, 625, 600
        ]
    }

    df = pd.DataFrame(raw_data)

    # arithmetic column for delay in mins
    df['delay_mins'] = df['actual_time'] - df['sched_time']

    # not sure if early bus (-2 mins) should be 0 or stay negative, leaving it for now
    # df['delay_mins'] = df['delay_mins'].clip(lower=0)

    # bus counts as late if delay is more than 5 mins
    df['is_late'] = df['delay_mins'] > 5

    return df

# testing if file works on its own
# print(load_transport_data())