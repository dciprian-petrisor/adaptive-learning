import sys

import manage
import socket
from contextlib import closing
import os
import time

host = os.getenv('ADAPTIVE_LEARNING_DB_HOST', 'localhost')
port = os.getenv('ADAPTIVE_LEARNING_DB_PORT', '5432')


def migrate():
    # max out at 30 seconds
    timeout_time = time.time() + 30
    # save the initial time the DB responded
    start_time = None
    while start_time is None and time.time() < timeout_time:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            if sock.connect_ex((host, int(port))) == 0:
                if start_time is None:
                    # set the start time when the db responded after no previous response
                    start_time = time.time()
                elif start_time + 5 > time.time():
                    # migrate and get out of loop if the db responded as active for 5 seconds
                    sys.argv = ["manage.py", "migrate"]
                    manage.main()
                    break
            else:
                # if at any point the db doesn't respond, reset the start_time
                start_time = None


if __name__ == '__main__':
    migrate()
