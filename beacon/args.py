import argparse

def parse_args():
    
    parser = argparse.ArgumentParser(description=
"""
Cortext Beacon:
A server that provides emo brain data over tcp

Format is this:
<F3>,<O1>,...
""",
    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-p', '--port',
                        default=1337, type=int,
                        metavar='N', help='The port the server should listen to (default: %(default)s)')
    parser.add_argument('--mock',
                        action='store_true',
                        help='Generate mock data. Don\'t try to use emo hardware.')

    
    return parser.parse_args()
