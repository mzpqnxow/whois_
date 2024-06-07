import logging
import sys

from whois.whois import NICClient
from whois.query import whois


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == "__main__":
    try:
        url_arg = sys.argv[1]
    except IndexError:
        logger.error("Usage: %s url" % sys.argv[0])
    else:
        logger.info(whois(url_arg))


__all__ = ["NICClient", "whois"]
