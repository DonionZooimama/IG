import time
import os
import sys
from threading import Thread
sys.path.append(os.path.join(sys.path[0], 'src'))

from InstaAccount import *

#info format [username, password, target audience, follows per hour, unfollows per hour, min following, max following per day]
accountInfo = [["books_cars_business", "dRuc*bawr5du", "cars", 70, 60, 500, 1000]]

for a in accountInfo:
	temp = Account(a[0], a[1], a[2], a[3], a[4], a[5], a[6]).start()