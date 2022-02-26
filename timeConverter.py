from lib2to3.pytree import convert
from dateutil.parser import parse, ParserError
import datetime
import pytz

import time
from dateutil.tz import gettz


def stringToDatetimeParser(stringToParse):
    try:
        tzinfo = {"CST": gettz("America/Chicago"),
                  "CT": gettz("America/Chicago"),
                  "PT": gettz("America/Los_Angeles"),
                  "PST": gettz("America/Los_Angeles"),
                  "ET": gettz("Canada/Eastern"),
                  "EST": gettz("Canada/Eastern"),
                  "UTC": gettz("ETC/UTC")
                  }
        parsed = parse(stringToParse, fuzzy=True, tzinfos=tzinfo)
        return parsed
    except ParserError:
        return None


def convertToUnix(timeToConvert):
    utc = pytz.timezone("ETC/UTC")
    cst = pytz.timezone("America/Chicago")
    timeCheck = timeToConvert.astimezone(utc)
    back = timeCheck.astimezone(cst)
    return time.mktime(timeCheck.timetuple())


if __name__ == "__main__":
    CST = stringToDatetimeParser("1:00 PM CST")
    PST = stringToDatetimeParser("1:00 PM PST")
    UTC = stringToDatetimeParser("1:00 PM UTC")

    print(f"CST: {CST} \nPST: {PST} \nUTC: {UTC}")

    CST = convertToUnix(CST)
    PST = convertToUnix(PST)
    UTC = convertToUnix(UTC)

    print(f"CST: {CST} \nPST: {PST} \nUTC: {UTC}")
