#!/usr/bin/env python
"""A CLI to Movies2HDD"""
print("Loading libraries...") #Not very helpful
from movies2hdd import Movies2HDD
movies2hdd = Movies2HDD()
#implement a command line parser
import argparse


parser = argparse.ArgumentParser(description="A command line interface to Movies2HDD.")
parser.add_argument("command", metavar="command", type=str, help="The command to execute.")
args = parser.parse_args()
print (args)
