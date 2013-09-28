import argparse

def parse_args():
    
    parser = argparse.ArgumentParser(description=
"""
Cortext Beacon:
A server that provides emo brain data over tcp

Format: all values separated by ',' followed by all qualities
X,Y,F3,FC5,AF3,F7,T7,P7,O1,O2,P8,T8,F8,AF4,FC6,F4,Unknown,... again for quality

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
