"""Could be put somewhere better probably, temporarily moved to avoid circular imports"""
import os
import re
import socket
import logging

from whois.patterns import IPV4_OR_V6

logger = logging.getLogger(__name__)


SUFFIXES = None


def extract_domain(url):
    """Extract the domain from the given URL

    >>> logger.info(extract_domain('http://www.google.com.au/tos.html'))
    google.com.au
    >>> logger.info(extract_domain('abc.def.com'))
    def.com
    >>> logger.info(extract_domain(u'www.公司.hk'))
    公司.hk
    >>> logger.info(extract_domain('chambagri.fr'))
    chambagri.fr
    >>> logger.info(extract_domain('www.webscraping.com'))
    webscraping.com
    >>> logger.info(extract_domain('198.252.206.140'))
    stackoverflow.com
    >>> logger.info(extract_domain('102.112.2O7.net'))
    2o7.net
    >>> logger.info(extract_domain('globoesporte.globo.com'))
    globo.com
    >>> logger.info(extract_domain('1-0-1-1-1-0-1-1-1-1-1-1-1-.0-0-0-0-0-0-0-0-0-0-0-0-0-10-0-0-0-0-0-0-0-0-0-0-0-0-0.info'))
    0-0-0-0-0-0-0-0-0-0-0-0-0-10-0-0-0-0-0-0-0-0-0-0-0-0-0.info
    >>> logger.info(extract_domain('2607:f8b0:4006:802::200e'))
    1e100.net
    >>> logger.info(extract_domain('172.217.3.110'))
    1e100.net
    """
    if IPV4_OR_V6.match(url):
        # this is an IP address
        return socket.gethostbyaddr(url)[0]

    # load known TLD suffixes
    global SUFFIXES
    if not SUFFIXES:
        # downloaded from https://publicsuffix.org/list/public_suffix_list.dat
        tlds_path = os.path.join(
            os.getcwd(), os.path.dirname(__file__), "data", "public_suffix_list.dat"
        )
        with open(tlds_path, encoding="utf-8") as tlds_fp:
            SUFFIXES = set(
                line.encode("utf-8")
                for line in tlds_fp.read().splitlines()
                if line and not line.startswith("//")
            )

    if not isinstance(url, str):
        url = url.decode("utf-8")
    url = re.sub("^.*://", "", url)
    url = url.split("/")[0].lower()

    # find the longest suffix match
    domain = b""
    split_url = url.split(".")
    for section in reversed(split_url):
        if domain:
            domain = b"." + domain
        domain = section.encode("utf-8") + domain
        if domain not in SUFFIXES:
            if b"." not in domain and len(split_url) >= 2:
                # If this is the first section and there wasn't a match, try to
                # match the first two sections - if that works, keep going
                # See https://github.com/richardpenman/whois/issues/50
                second_order_tld = ".".join([split_url[-2], split_url[-1]])
                if not second_order_tld.encode("utf-8") in SUFFIXES:
                    break
            else:
                break
    return domain.decode("utf-8")
