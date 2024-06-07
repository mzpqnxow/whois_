import socket
import subprocess

from whois.parser import TLDBase
from whois.whois import NICClient

from whois.patterns import IPV4_OR_V6
from whois.domains import extract_domain


def whois(url, command=False, flags=0, executable="whois", inc_raw=False, quiet=False):
    """Highest-level interface for making a query and parsing it

    Moved out of __init__.py to avoid circular imports and because it was crowded (for my taste, at least)
    """
    # clean domain to expose netloc
    ip_match = IPV4_OR_V6.match(url)
    if ip_match:
        try:
            result = socket.gethostbyaddr(url)
        except socket.herror:
            domain = url
        else:
            domain = extract_domain(result[0])
    else:
        domain = extract_domain(url)
    if command:
        # try native whois command
        r = subprocess.Popen([executable, domain], stdout=subprocess.PIPE)
        text = r.stdout.read().decode()  # type: ignore
    else:
        # try builtin client
        nic_client = NICClient()
        text = nic_client.whois_lookup(None, domain.encode("idna"), flags, quiet=quiet)

    entry = TLDBase.load(domain, text)
    if inc_raw:
        entry["raw"] = text
    return entry
