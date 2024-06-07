import datetime
import json
from collections import UserDict


class WhoisEncoder(json.JSONEncoder):
    """JSON Serialization for Whois records"""

    def default(self, *args, **kwargs):  # pylint: disable=unused-argument
        if not args:
            raise ValueError("Unexpected empty *args tuple!")

        if len(args) != 1:
            raise ValueError(
                "Unexpected length for *args tuple: {}, expected 1 ({})".format(
                    len(args), str(args)
                )
            )

        obj = args[0]

        if isinstance(obj, tuple):
            return list(obj)

        if isinstance(obj, bytes):
            # Should this be IDNA?
            return obj.decode("utf-8")

        if isinstance(obj, UserDict):
            return dict(obj)

        if isinstance(obj, datetime.datetime):
            return str(obj)

        return json.JSONEncoder.default(self, obj)
