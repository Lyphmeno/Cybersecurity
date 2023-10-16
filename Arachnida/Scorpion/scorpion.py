#!/usr/bin/env python3.10

from leiurus import Leiurus


def main() -> None:
    """
    Scorpion program executing the Leiurus class
    """
    try:
        scorpion = Leiurus()
        scorpion.execute()
    except Exception as e:
        print(f"Error : {e}")
        print(f"Please refer to the program manual :\n{scorpion.__doc__}")


if __name__ == '__main__':
    main()
