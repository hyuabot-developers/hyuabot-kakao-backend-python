# shuttle_stop = ['shuttleA', 'shuttleB', 'subway', 'terminal', 'dorm']
# 셔틀콕 > 한대앞/터미널, 셔틀콕 > 기숙사, 한대앞역, 터미널, 기숙사 순

# destination = ['toSubway', 'toTerminal', 'cycle']
import os, sys
sys.path.append(os.path.dirname(__file__))
from shuttle.strings import make_string, make2_string
def shuttle_main(where, destination = None):
    string = make_string(where, destination)
    return string

def schoolbus_main(route):
    string = make2_string(route)
    return string