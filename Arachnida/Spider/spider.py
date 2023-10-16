#!/usr/bin/env python3.10

from caerostris import Caerostris
import time


def main() -> None:
    """
    Spider program executing the Caerostris class
    """
    try:
        spider = Caerostris()
        spider.execute()
    except Exception as e:
        print(f"Error : {e}")
        print(f"Please refer to the program manual :\n{spider.__doc__}")


if __name__ == "__main__":
    timestamp = 0
    st = time.time()
    main()
    if timestamp:
        elapsed_time = time.time() - st
        print('Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
