# Zone.py
Gain information on other websites and their headers using zone.vision

The script is an interface made to use the full abilities of [zone.vision](https://zone.vision/#/) provided by DNSimple.

The script is solely made in python and I have not made any variants in different languages.

### Here's the Help and options to the script.

> ``zone.py [OPTION] [WEBSITE]``
>> ``Zone.py`` is an application used to get information about a website with its headers. It uses the website zone.vision to get all of its information. it will not longer work if the API is no longer existing or no longer free.
>> ``OPTIONS:``
>>> ``--all``       Will give all available infomration on the given website. Gives the same result as running with every option.
>>> ``-name``       Returns the name of the website.
>>> ``-dns``        Returns all dns servers that name the given website.
>>> ``-soa``        Returns important information including the primary server and its serial number
>>> ``-a``      Returns all IPv4 Authoritative servers with their ip addresses
>>> ``-aaaa``       Returns all IPv6 Authoritative servers with their ipv6 addresses, if there are any
>>> ``-mx``     Returns all mailing servers for the given website
>>> ``-cname``      Returns the cname for the website
>>> ``ADDITIONAL OPTIONS:``
>>>> ``-b``     Returns true or false whether or not the requested records are present. it prints true/false multiple times in order of first possible option to last.
>>>> ``--detail``   Returns details of which specific records are present
>>>> ``-h/-help/--help``    Returns the help page