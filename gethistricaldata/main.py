import logging
import sys
from typing import List

from fr import get_fr_rate
from ls import get_ls_rate
from notice import notice
from oi import get_oi_rate
from util import error_handle, hdf_into_space
from vol import get_vol_rate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def main() -> None:
    target = sys.argv
    successes: List[str] = []
    failures: List[str] = []

    for i in target:
        try:
            logger.info(f"Get Histrical Data : [{i}]")
            if i == "fr":
                get_fr_rate()
            elif i == "ls":
                get_ls_rate()
            elif i == "oi":
                get_oi_rate()
            elif i == "vol":
                get_vol_rate()
            successes.append(i)
        except Exception:
            error_handle()
            failures.append(i)
    logger.info("HDF into space")
    hdf_into_space()

    # discord への通知
    notice.send_notice(successes, failures)


if __name__ == "__main__":
    main()
