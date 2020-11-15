#!/usr/bin/env python3.7
import os
def run_bot():
    while True:
        try:
            os.system("clima_bot.py  start")
        except:
            pass
if __name__ == "__main__":
    run_bot()
