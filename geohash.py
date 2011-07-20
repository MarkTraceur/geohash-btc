#!/usr/bin/python

# Copyright 2011 Mark Holmquist
# This script is free software, licensed under the GPLv3, of which you should have received a copy with this software.
# If you didn't, I apologize, but you'll be able to find it at /usr/share/common-licences/GPL-3 or http://www.gnu.org/licenses/gpl-3.0.txt

# This script will calculate a geohash location for you based on the opening price at Mt. Gox for BTC/USD trades.
# Usually, people use the DJIA for this algorithm, but I didn't think that was nerdy enough :)
# It will also automagically give you a link to a google map to the location.
# If you'd like any help with it, don't hesitate to open up an issue at github.
# Have fun!

import datetime
import hashlib
import json
import urllib

latitude = 33
longitude = -116

btcinfo = urllib.urlopen("http://bitcoincharts.com/t/markets.json")
jsoninfo = btcinfo.read()

dictinfo = json.loads(jsoninfo)

todayopen = -1
for sym in dictinfo:
    if sym["symbol"] == "mtgoxUSD":
        todayopen = sym["open"]
    else:
        continue

if todayopen < 0:
    raise ValueError("No data from bitcoincharts, is it down?")

thestring = str(datetime.date.today()) + "-" + str(todayopen)

thehash = hashlib.md5(thestring).hexdigest()

hexnum = (thehash[0:16], thehash[16:32])

curpow = 1
decnum = [0.0, 0.0]

while curpow <= len(hexnum[0]):
    decnum[0] += int(hexnum[0][curpow-1], 16) * (1.0 / (16.0 ** curpow))
    decnum[1] += int(hexnum[1][curpow-1], 16) * (1.0 / (16.0 ** curpow))
    curpow += 1

if latitude >= 0:
    decnum[0] += latitude
else:
    decnum[0] -= latitude
    decnum[0] *= -1

if longitude >= 0:
    decnum[1] += longitude
else:
    decnum[1] -= longitude
    decnum[1] *= -1

print "http://maps.google.com/maps?q=" + str(decnum[0]) + "," + str(decnum[1]) + "(Geohash+for+" + str(datetime.date.today()) + ")&iwloc=A"
