#!/usr/bin/python
activate_this = '/home/vagrant/itemcatalog/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import os

sys.path.insert(0, '/home/vagrant/itemcatalog')

from itemcatalog import create_app
application = create_app()
