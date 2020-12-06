#!/usr/bin/env python3.7
import os
import urllib3.exceptions
def run_bot():
    while True:
        try:
            os.system("clima_bot.py  start resources/credibility-0.0.7.jar")
        except urllib3.exceptions.ProtocolError:
            print('skipped urllib3.exceptions.ProtocolError')
            pass
if __name__ == "__main__":
    run_bot()
