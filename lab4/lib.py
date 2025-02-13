# 4:     Write a Python program to calculate two date difference in seconds.

from datetime import datetime, timedelta


d_y = datetime.now() - timedelta(seconds=50)
d_t = datetime.now()

diff = int(d_t.strftime("%S")) - int(d_y.strftime("%S"))

print (diff)