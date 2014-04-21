#!/usr/bin/python

import sys
import StringIO
from pprint import pprint
import subprocess

from megaclioutputparser import MegaCLIOutputParser

if __name__ == "__main__":
    p = MegaCLIOutputParser()
    proc = subprocess.Popen(["megacli", "-pdinfo", "-physdrv[%s:%s]" % (
        sys.argv[1], sys.argv[2]), "-a1"], stdout=subprocess.PIPE)
    pprint(p.parse_record_string(proc.communicate()[0]))
