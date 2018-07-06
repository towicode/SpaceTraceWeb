#!/usr/bin/env python
import socket
from kombu import Connection

# Needs to find the pylib_bcf module relative to this file
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
else:
    raise Exception("Cannot load pylib_bcf modules")

from pylib_bcf.load_env_vars import *

if 'RABBITMQ_HOST' not in globals():
    raise Exception("Is RABBITMQ_HOST set in the .env file?")

if 'RABBITMQ_PORT' not in globals():
    raise Exception("Is RABBITMQ_PORT set in the .env file?")

if 'RABBITMQ_USER' not in globals():
    raise Exception("Is RABBITMQ_USER set in the .env file?")

if 'RABBITMQ_PASS' not in globals():
    raise Exception("Is RABBITMQ_PASS set in the .env file?")

if 'RABBITMQ_VHOST' not in globals():
    raise Exception("Is RABBITMQ_VHOST set in the .env file?")


connection_creditals = {
    'user': RABBITMQ_USER,
    'password': RABBITMQ_PASS,
    'hostname': RABBITMQ_HOST,
    'port': RABBITMQ_PORT,
    'vhost': RABBITMQ_VHOST,
}

url = 'amqp://{user}:{password}@{hostname}:{port}/{vhost}'.format(**connection_creditals)
with Connection(url) as c:
    try:
        c.connect()
    except socket.error:
        raise ValueError("Received socket.error, "
                         "rabbitmq server probably isn't running")
    except IOError:
        raise ValueError("Received IOError, probably bad credentials")
    else:
        print("Credentials are valid")