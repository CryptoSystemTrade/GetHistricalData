import sys

from fr import get_fr_rate
from ls import get_ls_rate
from oi import get_oi_rate
from util import hdf_into_space
from vol import get_vol_rate


def main() -> None:
    target = sys.argv

    if "fr" in target:
        print("fr")
        get_fr_rate()

    if "ls" in target:
        print("ls")
        get_ls_rate()

    if "oi" in target:
        print("oi")
        get_oi_rate()

    if "vol" in target:
        print("vol")
        get_vol_rate()

    print("hdf into space")
    hdf_into_space()


if __name__ == "__main__":
    main()
