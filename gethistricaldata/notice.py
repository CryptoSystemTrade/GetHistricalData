from typing import List

import const
import requests


class Notice:
    def __init__(self) -> None:
        self.url = const.DISCORD_WEBHOOK

    def send_notice(self, success: List[str], failure: List[str]) -> None:
        message = ""
        success_str = ",".join(success)
        failure_str = ",".join(failure)
        if len(failure) == 0:
            message = f"✅ All Success\r Target: {success_str}"
        else:
            message = f"✅ Success: {success_str} \r ❌ Failure: {failure_str}"

        data = {"content": message}
        requests.post(self.url, data=data)


notice = Notice()
