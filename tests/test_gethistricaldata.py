from gethistricaldata import __version__
from gethistricaldata.notice import notice

def test_version() -> None:
    assert __version__ == "0.1.0"

def test_notice() -> None:
    success = ["success","test"]
    failure = ["failure","test"]
    assert notice.send_notice(success,failure) == None



