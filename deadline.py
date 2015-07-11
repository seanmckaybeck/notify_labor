import argparse
import datetime
import sys
import time


HOUR=0
MINUTE=0


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', type=int, help='Year to use')
    parser.add_argument('-m', type=int, help='Month to use')
    parser.add_argument('-d', type=int, help='Day to use')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    if not args.y or not args.m or not args.d:
        sys.stdout.write('Specify a year, month, and day\n')
        sys.stdout.flush()
        sys.exit(1)
    dt = datetime.datetime(args.y, args.m, args.d, HOUR, MINUTE, 0, 0)
    stamp = time.mktime(dt.timetuple())
    sys.stdout.write(str(stamp)+'\n')
    sys.stdout.flush()
