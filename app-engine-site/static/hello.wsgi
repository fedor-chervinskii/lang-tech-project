#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/nikita/server/")

from hello import app as application
application.secret_key = 'Add your secret key'
