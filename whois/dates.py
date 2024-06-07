from contextlib import suppress
from typing import Union
import datetime

from dateutil import parser as dp
from dateutil.utils import default_tzinfo

from whois.time_zones import TZ_DATA

KNOWN_FORMATS = [
    "%d-%b-%Y",  # 02-jan-2000
    "%d-%B-%Y",  # 11-February-2000
    "%d-%m-%Y",  # 20-10-2000
    "%Y-%m-%d",  # 2000-01-02
    "%d.%m.%Y",  # 2.1.2000
    "%Y.%m.%d",  # 2000.01.02
    "%Y/%m/%d",  # 2000/01/02
    "%Y/%m/%d %H:%M:%S",  # 2011/06/01 01:05:01
    "%Y/%m/%d %H:%M:%S (%z)",  # 2011/06/01 01:05:01 (+0900)
    "%Y%m%d",  # 20170209
    "%Y%m%d %H:%M:%S",  # 20110908 14:44:51
    "%d/%m/%Y",  # 02/01/2013
    "%Y. %m. %d.",  # 2000. 01. 02.
    "%Y.%m.%d %H:%M:%S",  # 2014.03.08 10:28:24
    "%d-%b-%Y %H:%M:%S %Z",  # 24-Jul-2009 13:20:03 UTC
    "%a %b %d %H:%M:%S %Z %Y",  # Tue Jun 21 23:59:59 GMT 2011
    "%a %b %d %Y",  # Tue Dec 12 2000
    "%Y-%m-%dT%H:%M:%S",  # 2007-01-26T19:10:31
    "%Y-%m-%dT%H:%M:%SZ",  # 2007-01-26T19:10:31Z
    "%Y-%m-%dT%H:%M:%SZ[%Z]",  # 2007-01-26T19:10:31Z[UTC]
    "%Y-%m-%dT%H:%M:%S.%fZ",  # 2018-12-01T16:17:30.568Z
    "%Y-%m-%dT%H:%M:%S.%f%z",  # 2011-09-08T14:44:51.622265+03:00
    "%Y-%m-%dT%H:%M:%S%z",  # 2013-12-06T08:17:22-0800
    "%Y-%m-%dT%H:%M:%S%zZ",  # 1970-01-01T02:00:00+02:00Z
    "%Y-%m-%dt%H:%M:%S.%f",  # 2011-09-08t14:44:51.622265
    "%Y-%m-%dt%H:%M:%S",  # 2007-01-26T19:10:31
    "%Y-%m-%dt%H:%M:%SZ",  # 2007-01-26T19:10:31Z
    "%Y-%m-%dt%H:%M:%S.%fz",  # 2007-01-26t19:10:31.00z
    "%Y-%m-%dt%H:%M:%S%z",  # 2011-03-30T19:36:27+0200
    "%Y-%m-%dt%H:%M:%S.%f%z",  # 2011-09-08T14:44:51.622265+03:00
    "%Y-%m-%d %H:%M:%SZ",  # 2000-08-22 18:55:20Z
    "%Y-%m-%d %H:%M:%S",  # 2000-08-22 18:55:20
    "%d %b %Y %H:%M:%S",  # 08 Apr 2013 05:44:00
    "%d/%m/%Y %H:%M:%S",  # 23/04/2015 12:00:07 EEST
    "%d/%m/%Y %H:%M:%S %Z",  # 23/04/2015 12:00:07 EEST
    "%d/%m/%Y %H:%M:%S.%f %Z",  # 23/04/2015 12:00:07.619546 EEST
    "%B %d %Y",  # August 14 2017
    "%d.%m.%Y %H:%M:%S",  # 08.03.2014 10:28:24
    "before %b-%Y",  # before aug-1996
    "before %Y-%m-%d",  # before 1996-01-01
    "before %Y%m%d",  # before 19960821
    "%Y-%m-%d %H:%M:%S (%Z%z)",  # 2017-09-26 11:38:29 (GMT+00:00)
    "%Y-%b-%d.",  # 2024-Apr-02.
]


def datetime_parse(date_string: str) -> Union[str, datetime.datetime]:
    """Return a datetime if the string can be parsed, otherwise return the original value as a string"""
    for known_format in KNOWN_FORMATS:
        with suppress(ValueError):
            return datetime.datetime.strptime(date_string, known_format)
    return date_string


def cast_date(s, day_first=False, year_first=False) -> Union[str, datetime.datetime]:
    """Convert any date string found in WHOIS to a datetime object."""
    # Since Python 3.11, there also exists datetime.UTC which is equivalent to datetime.timezone.utc
    # So you can also do datetime.datetime.now(datetime.UTC).
    # NOTE: Python 3.10 and earlier do **NOT** have datetime.UTC, so probably shouldn't use it
    with suppress(Exception):
        return default_tzinfo(
            dp.parse(s, tzinfos=TZ_DATA, dayfirst=day_first, yearfirst=year_first),
            datetime.timezone.utc,
        )
    return datetime_parse(s)
