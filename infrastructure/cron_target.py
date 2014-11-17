import time
from subprocess import call

__author__ = 'sxh112430'

# run this once every half second. Start this script once every minute.
for i in range((59 * 2) + 1):
    time.sleep(.5) # wait one half second
    call(['wget','http://np.spencer-hawkins.com/cron_trigger/'])