# pylibpack

A simple way to pack a multiple-files library into a single .py

BEWARE! This is a proof of concept (but works ok). 

## How to use it


Take for a example a library with several modules inside; here we have `superlib` which has some attributes at "root level", and a function in other module:

```bash
~/test $ tree 
.
└── superlib
    ├── __init__.py
    └── othermod.py

1 directory, 2 files

~/test $ cat superlib/__init__.py
"""This is an example of a super packed library."""

# generic lib attributes
version = "3.14"

# bring the (public) rest of the lib to this namespace
from .othermod import helloworld  # NOQA

~/test $ cat superlib/othermod.py 
def helloworld():
    print("For those about to rock, we salute you!")
```

Pack it:

```bash
~/test $ python3 pylibpack.py superlib
10:18:23|facundo@almudix:~/temp/pypack$ ll
total 8
drwxrwxr-x 3 facundo facundo 4096 nov  3 10:18 superlib
-rw-rw-r-- 1 facundo facundo 1392 nov  3 10:18 superlib.py
```

Move it to somewhere else, or a different machine:

```bash
~/test $ mv superlib.py /tmp/
~/test $ cd /tmp/
/tmp $
```

And just use it:

```
/tmp $ python3
Python 3.10.4 (main, Jun 29 2022, 12:14:53) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import superlib
>>> superlib.version
'3.14'
>>> superlib.helloworld()
For those about to rock, we salute you!
```
