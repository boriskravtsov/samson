# Aug-25-2025
# timer.py

import time

global timer_start


def init_timer():
    global timer_start
    timer_start = time.time()


def get_elapsed_time_hour_min_sec():
    global timer_start
    timer_end = time.time()
    seconds = int(timer_end - timer_start)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return h, m, s


def save_elapsed_time_hour_min_sec(path_time):
    h, m, s = get_elapsed_time_hour_min_sec()
    string_time = f'Elapsed time = {h:02d} hour(s)  {m:02d} min  {s:02d} sec\n'
    print('\n' + string_time)
    with open(path_time, 'w') as fp:
        fp.write(string_time)
