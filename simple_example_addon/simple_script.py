import os
import time

MESSAGE = os.getenv('MESSAGE', 'Hello from Home Assistant add-on')

def main():
    while True:
        print(MESSAGE)
        time.sleep(10)

if __name__ == "__main__":
    main()
