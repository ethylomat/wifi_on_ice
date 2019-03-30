#!/usr/bin/env python3
import argparse
import os
import signal
import sys
import time

from robobrowser import RoboBrowser
import requests
from wireless import Wireless


parser = argparse.ArgumentParser(description='Enables unlimited WiFi Data at the Deutsch Bahn ICE WiFi network')
parser.add_argument('-I', '--interface', type=str, help='defines the wlan interface to use', default='wlan0')
parser.add_argument('-s', '--sleep', type=int, help='sleep n second(s) beetween each update', default=30)
args = parser.parse_args()

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    driver.quit()
    print('wifi_on_ice has stopped.')
    sys.exit(0)

def connect_wifi():
    wireless = Wireless()
    wireless.connect(ssid='WIFIonICE', password=False)

def wifi_login():
    browser = RoboBrowser()
    browser.open('http://login.wifionice.de/')
    login_form = browser.get_form()
    browser.submit_form(login_form)

def get_current_quota():
    usage = float(requests.get('http://login.wifionice.de/usage_info/').content)
    return usage

print("wifi on ice started, press Ctrl+C to exit.")

while True:
    try:
        time.sleep(2)
        quota_now = get_current_quota()
        print('Currently {0.2f}% of your quota are used.'.format(quota_now))
        if int(quota_now) > 90:
            print('More than 90% of your quota are used, reconnecting!!!')
            os.system('sudo macchanger -r {}'.format(args.interface))
            time.sleep(1)
            connect_wifi()
            time.sleep(2)
            wifi_login()
    except Exception, e:
        print(e)
        pass

    os.system('sudo true')  # keep sudo active
    time.sleep(args.sleep)
