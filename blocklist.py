""" 
blocklist.py

This file just contains the blocklist of the JWT tokens. It will be imported by 
app and the logout resource so that tokens can be added to the blocklist when the
user logs out.

Note that sets in Python do not persist in between app restarts. If the app restarts
the blocklist will get deleted and previous JWT will continue to work until it expires.

Better to store the BLOCKLIST in a database or Reddice for maximum performance!
"""

BLOCKLIST = set()
