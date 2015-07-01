DDNS Script for Route 53
==========================================

3rd party DDNS "providers" are expensive/annoying or both, and Amazon Route 53 is inexpensive, so after moving my DNS servers to route 53, I wrote a quick python script to update DNS entries if my IP address changes.

Requires [Bolo](https://github.com/boto/boto) and [Requests](http://docs.python-requests.org/en/latest/) to run.

The script should be run periodically depending on how often your ISP changes your IP address.  You can use windows task scheduler, cron under linux, etc.  It can also be installed on a router or NAS if it supports python.
