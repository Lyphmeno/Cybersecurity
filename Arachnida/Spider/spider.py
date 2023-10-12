#!/usr/bin/env python3.10

from crawler import Crawl


def main() -> None:
    try:
        tarantula = Crawl()
        tarantula.execute()
    except Exception as e:
        print(f"Error : {e}")
        print(f"Please refer to the program manual :\n{main.__doc__}")
        return 1


if __name__ == "__main__":
    main()
