from fr import get_fr_rate
from ls import get_ls_rate
from util import hdf_into_space


def main() -> None:
    print("fr")
    get_fr_rate()

    print("ls")
    get_ls_rate()

    print("hdf into space")
    hdf_into_space()


if __name__ == "__main__":
    main()
