#!/usr/bin/python

from pprint import pprint
import subprocess

from megaclioutputparser import MegaCLIOutputParser

if __name__ == "__main__":
    p = MegaCLIOutputParser()
    proc = subprocess.Popen(["megacli", "-pdList", "-a1"], stdout=subprocess.PIPE)
    pprint(p.parse_string(proc.communicate()[0]))
