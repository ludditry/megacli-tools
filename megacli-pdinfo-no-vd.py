#!/usr/bin/python

from pprint import pprint
import subprocess

from megaclioutputparser import MegaCLIOutputParser

if __name__ == "__main__":
    p = MegaCLIOutputParser()
    proc = subprocess.Popen(["megacli", "-pdList", "-a1"],
                            stdout=subprocess.PIPE)
    output = p.parse_string(proc.communicate()[0])
    print "\n".join(["%s:%s" % (d['enclosure_device_id'], d['slot_number'])
                     for d in output if not d.has_key("drive_position")])
