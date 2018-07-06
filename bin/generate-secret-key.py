#!/usr/bin/env python
# -*- coding: utf-8 -*-
# bin/generate-secret-key.py



import string
import re
import random

"""
Pseudo-random django secret key generator.
- Does print SECRET key to terminal which can be seen as unsafe.
"""

# Get ascii Characters numbers and punctuation (minus quote characters as they could terminate string).
chars = ''.join([string.ascii_letters, string.digits, re.sub(r'[\'"`$%]', '', string.punctuation), ])

SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

print(SECRET_KEY)
