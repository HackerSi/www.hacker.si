#!/usr/bin/env python

from datetime import datetime
from sys import argv, exit


format = """
Title
==========================

:date: %s
:tags: mpd, fun
:category: GNU-linux
:status: draft
"""

if len(argv) == 1:
    print "%s: missing file to write" % argv[0]
    exit(1)

now_ = datetime.now()
date_ = now_.strftime('%Y-%m-%d %H:%M')

header = format % date_
with open(argv[1], 'w+') as f:
    f.write(header)

