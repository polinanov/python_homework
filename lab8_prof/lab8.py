import os
import pandas
import datetime
import re
from datetime import timedelta


def time_tracking(time_start, datetime_str, max_duration: int):
    max_ = timedelta(minutes=max_duration)
    if datetime_str - time_start > max_:
        return False
    return True


def prepare_train_set(logs_path: str, session_length: int, window_size: int, max_duration: int):
    list_session = []
    windows = [[None] * 2 for _ in range(window_size)]
    for x in range(1, session_length + 1):
        list_session.append('timestamp' + str(x))
        list_session.append('site' + str(x))
    list_session.append('user_id')
    panda = pandas.DataFrame(columns=list_session)
    os.chdir(logs_path)
    counter_line = -1
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            counter_session = 0
            counter_line += 1
            time_start = 0
            # counter_offset
            offset = 0
            f = open(name)
            for _ in f:
                break
            for line in f:
                df = line.strip().split(',')
                datetime_str = datetime.datetime.strptime(df[0], '%Y-%m-%d %H:%M:%S')
                made_it = False
                # write to end
                if counter_session == 0:
                    time_start = datetime_str
                if time_tracking(time_start, datetime_str, max_duration):
                    panda.loc[counter_line, 'timestamp' + str(counter_session + 1)] = datetime_str
                    panda.loc[counter_line, 'site' + str(counter_session + 1)] = df[1]
                    if counter_session >= session_length - window_size:
                        windows[offset][0] = datetime_str
                        windows[offset][1] = df[1]
                        offset += 1
                    made_it = True
                else:
                    counter_session = session_length - 1
                counter_session += 1
                # start new line
                if counter_session == session_length:
                    panda.loc[counter_line, 'user_id'] = re.findall(r'\d+', os.path.join(root, name))[0]
                    counter_line += 1
                    counter_session = 0
                    # rewrite offset
                    if offset > 0:
                        move = 0
                        while offset > 0:
                            panda.loc[counter_line, 'timestamp' + str(counter_session + 1)] = windows[move][0]
                            panda.loc[counter_line, 'site' + str(counter_session + 1)] = windows[move][1]
                            if counter_session == 0:
                                time_start = windows[move][0]
                            move += 1
                            offset -= 1
                            counter_session += 1
                        for _ in windows:
                            _[0] = None
                            _[1] = None
                    # write to end if wasn't done (1 comment)
                    if not made_it:
                        if time_tracking(time_start, datetime_str, max_duration):
                            panda.loc[counter_line, 'timestamp' + str(counter_session + 1)] = datetime_str
                            panda.loc[counter_line, 'site' + str(counter_session + 1)] = df[1]
                        else:
                            panda.loc[counter_line, 'user_id'] = re.findall(r'\d+', os.path.join(root, name))[0]
                            counter_line += 1
                            counter_session = 0
                            panda.loc[counter_line, 'timestamp' + str(counter_session + 1)] = datetime_str
                            panda.loc[counter_line, 'site' + str(counter_session + 1)] = df[1]
                            time_start = datetime_str
                        counter_session += 1
            panda.loc[counter_line, 'user_id'] = re.findall(r'\d+', os.path.join(root, name))[0]
            print(panda.to_string())
            return panda



if __name__ == '__main__':
    a = datetime.datetime.now()
    panda = prepare_train_set("test_path/", 4, 2, 30)
    b = datetime.datetime.now()
    print(b - a)
