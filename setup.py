import os
import re
import json
from setuptools import setup

with open('setup.json') as f:
    c = json.loads(f.read())

with open(os.path.join(c['name'], '__init__.py')) as f:
    version = re.findall("^__version__ = '(.*)'", f.read())[0]

kwargs = {
        'name': c['name'],
        'version': version,
        'description': c.get('description',''),
        'url': c.get('url',''),
        'author': c.get('author',''),
        'author_email': c.get('author_email',''),
        'license': c.get('license',''),
        'packages': c.get('packages', []),
        'zip_safe': False,
        'scripts': c.get('scripts',[]),
        'package_data': c.get('package_data',{}),
        'classifiers': c.get('classifiers', [])
        }

setup(**kwargs)



