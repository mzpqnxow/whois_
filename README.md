Goal
====

-  Create a simple importable Python module which will produce parsed
   WHOIS data for a given domain.
-  Able to extract data for all the popular TLDs (com, org, net, ...)
-  Query a WHOIS server directly instead of going through an
   intermediate web service like many others do.

Experimental Refactor Branch
============================

In this branch, the following has been done:

- To reduce boilerplate, the base class and per-TLD subclasses were changed a bit
  - They no longer need a boilerplate `__init__()`
  - Tried to make a quick pass at accommodating for some one-off patterns in a generic way
- Refactoring of modules
  - Not suggesting this is a final state, partially it was done to deal with circular imports
- A bunch of small bits of subjective improvements (style, some type annotations here and there)
- A tiny number of objective "fixes" (e.g. the `datetime.UTC` does not seem to exist before Python 3.11,
  so that was replaced)
- Some not so desired renames of things that should be considered temporary

*NOT* yet done:

- Separating TLD subclasses into individual modules in a package (e.g. `whois.tld.com`)
  - To be loaded dynamically, rather than using a large `if`/`else`
- Broader refactor of the modules
  - I believe the networking code would be best in its own module. It makes
    caching easier if that's something desired later, and it's a natural
    separation in my opinion
- Full PEP-484 annotation; this is a quick task but I didn't want to muck up
  the more substantive changes with changes to every single function and class
  if it could be avoided
- Formatting based on `black`; though some modules probably did get reformatted
  by `black` by my IDE, if so, sorry for that - it makes diffs impossible to
  read

Beware, this was done in 4 hours on a Saturday morning. I did some basic testing
on a few domains, but don't expect it to work 100% on everything. Especially
the more exotic classes that had implemented 5-10 lines of their own logic in
`__init__()`. I believe I ported those to a cleaner style, but it's possible
I made a mistake or three :>

Example
=======

```python
>>> import whois
>>> w = whois.whois('example.com')
>>> w.expiration_date  # dates converted to datetime object
datetime.datetime(2022, 8, 13, 4, 0)
>>> w.text  # the content downloaded from whois server
u'\nDomain Name: EXAMPLE.COM
Registry Domain ID: 2336799_DOMAIN_COM-VRSN
...'

>>> print(w)  # print values of all found attributes (as a dict)
{'creation_date': [datetime.datetime(1995, 2, 23, 5, 0, tzinfo=tzoffset('UTC', 0)), ...

>>> print(w.json(indent=2))  # print values of all found attributes as pretty-printed JSON
{
  "creation_date": "1995-08-14 04:00:00",
  "expiration_date": "2022-08-13 04:00:00",
  "updated_date": "2021-08-14 07:01:44",
  "domain_name": "EXAMPLE.COM",
  "name_servers": [
      "A.IANA-SERVERS.NET",
      "B.IANA-SERVERS.NET"
  ],
  ...

```

Install
=======

Install from pypi:

```bash
pip install python-whois
```

Or checkout latest version from repository:

```bash
git clone git@github.com:richardpenman/whois.git
pip install -r requirements.txt
```

Run test cases:

```bash
python -m pytest
```

Problems?
=========

Pull requests are welcome! 

Thanks to the many who have sent patches for additional TLDs. If you want to add or fix a TLD it's quite straightforward. 
See example domains in [whois/parser.py](https://github.com/richardpenman/whois/blob/master/whois/parser.py)

Basically each TLD has a similar format to the following:

```python
class WhoisOrg(WhoisEntry):
  """Whois parser for .org domains
  """
  regex = {
    'domain_name':      'Domain Name: *(.+)',
    'registrar':        'Registrar: *(.+)',
    'whois_server':     'Whois Server: *(.+)',
    ...
  }

  def __init__(self, domain, text):
    if text.strip() == 'NOT FOUND':
      raise PywhoisError(text)
    else:
      WhoisEntry.__init__(self, domain, text)
```
