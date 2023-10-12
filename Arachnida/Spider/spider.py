#!/usr/bin/env python3.10

from crawler import Crawl
import time


def main() -> None:
    try:
        tarantula = Crawl()
        tarantula.execute()
    except Exception as e:
        print(f"Error : {e}")
        print(f"Please refer to the program manual :\n{tarantula.__doc__}")
        return 1


if __name__ == "__main__":
    st = time.time()
    main()
    elapsed_time = time.time() - st
print('Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
