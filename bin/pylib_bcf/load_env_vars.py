# load_env_vars.py
# -*- coding: utf-8 -*-
# Hagan Franks 2017-02-03 franks ȦŦ email Ḓ0Ŧ arizona Ḓ0Ŧ edu

import os
import re
import pprint
import string
import sys
from .Itpl import Itpl
from os.path import join, dirname
from copy import deepcopy
from functools import reduce


pp = pprint.PrettyPrinter(indent=4)
module = sys.modules[__name__]
load_env_script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_best_guess = os.path.realpath(os.path.join(load_env_script_dir, '../../bcfsrc/.env'))
dotenv_2nd_guess = os.path.realpath(os.path.join(load_env_script_dir, '../../django_project/.env'))

__all__ = []


def parse_dotenv(dotenv_path):
    with open(dotenv_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            v = v.strip("'").strip('"')
            yield k, v


def assemble_string(chunks, finished_dictionary):
    """
    returns the new string
    """
    result = []
    for live, chunk in chunks:
        if(live == 1):
            if(chunk in finished_dictionary):
                result.append(finished_dictionary[chunk])

            elif(chunk in os.environ):
                result.append(os.environ[chunk])
            else:
                result.append('${{{chunk}}}'.format(chunk=chunk))
        else:
            result.append(chunk)
    # print("--->{}".format(string.join(result, "")))
    return "".join(result)


def process_dictionary(counter, input_dictionary, **finished_dictionary):
    """
    Recursive strategy to digest the .env file using the Itpl library and dotenv scripts
    """
    # print(
    #     "counter: {}  size of input_dictionary: {} size of finished_dictionary: {}".format(
    #         counter, len(input_dictionary), len(finished_dictionary)
    #     )
    # )
    if(counter >= 15):
        pp.pprint(input_dictionary)
        raise Exception("Reached maximum recursion: {}".format(counter))

    if(not input_dictionary):
        return finished_dictionary

    # print("~~~~~~~START~~~~~~~~~")
    # print("{} pass input_dictionary:".format(counter))
    # pp.pprint(input_dictionary)
    # print("{} pass finished_dictionary:".format(counter))
    # pp.pprint(finished_dictionary)
    # print("~~~~~~~~~~~~~~~~~~~~~")

    new_input_dictionary = {}

    # Skip var that clearly wouldn't need expansion such as SECRET_KEY
    for skip_key in ['SECRET_KEY', ]:
        if( skip_key in input_dictionary ):
            finished_dictionary[skip_key] = input_dictionary[skip_key]
            del input_dictionary[skip_key]

    for key, value in input_dictionary.items():
        itpl_process = Itpl(value)
        # No value is set!
        if(len(itpl_process.chunks) == 0):
            finished_dictionary[key] = None
        # Simple (no substitution)
        elif(
            (len(itpl_process.chunks) >= 1) and
            # collapse the chunks 'live' field and looks for all set to 0
            (reduce(lambda a, b: a or b, [x_y[0] for x_y in itpl_process.chunks]) == 0)
        ):
            finished_dictionary[key] = assemble_string(itpl_process.chunks, finished_dictionary)
        elif(
            (len(itpl_process.chunks) >= 1) and
            # collapse the chunks 'live' field and looks for any set to 1
            (reduce(lambda a, b: a or b, [x_y1[0] for x_y1 in itpl_process.chunks]) == 1)
        ):
            new_input_dictionary[key] = assemble_string(itpl_process.chunks, finished_dictionary)
        else:
            # We shouldn't reach this bit.. Possible corruption from chunks?
            pp.pprint(itpl_process.chunks)
            raise Exception("KEY: {} VALUE: {} Possible corrupted chunk from itpl library?".format(key, value))

    return process_dictionary(counter + 1, new_input_dictionary, **finished_dictionary)


def set_module_values(finished_dictionary):
    """
    After expanding the .env file into the finished_dictonary, load them into this module
    """
    for key, value in finished_dictionary.items():
        setattr(module, key, value)
        __all__.append(key)


if(os.path.exists(dotenv_best_guess)):
    env_file = dotenv_best_guess
elif(os.path.exists(dotenv_2nd_guess)):
    env_file = dotenv_2nd_guess
else:
    raise Exception("Missing .env file at: {}".format(dotenv_best_guess))

input_dictionary = { k: v for k,v in parse_dotenv(env_file)}
finished_dictionary = {}
result_dict = process_dictionary(1, input_dictionary, **finished_dictionary)
set_module_values(result_dict)
