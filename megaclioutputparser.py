import sys
import StringIO

def position_parser(s):
    # looks like this:
    # DiskGroup: 44, Span: 0, Arm: 0
    d = {}
    for info in s.split(","):
        key, value = info.split(":")
        d[key.strip()] = int(value.strip())
    return d


def int_parser(s):
    return int(s.strip())


def key_sanitize(s):
    # strip extra whitespace
    # replace spaces with underscores
    # replace 's with nothing
    # replace .s with nothing
    # lower case
    return s.strip().replace(" ", "_").replace("'s", "").replace(".", "").lower()


class MegaCLIOutputParser(object):
    def __init__(self):
        self.file = None
        self.reset()

    def reset(self):
        if self.file is not None:
            self.file.close()
            self.file = None
        self.states = {
            "START": 0,
            "ADAPTER": 1,
            "NEW_RECORD": 2,
            "MIGHT_COULD_NEW_RECORD": 3,
            "INFO": 4,
            "EXIT": 5
        }
        self.field_parsers = {
            "drive_position": position_parser,
            "media_error_count": int_parser,
            "other_error_count": int_parser,
            "predictive_failure_count": int_parser,
            "device_id": int_parser,
            "slot_number": int_parser,
            "enclosure_device_id": int_parser,
            "sector_size": int_parser,
            "sequence_number": int_parser,
            "shield_counter": int_parser
        }
        self.state = self.states['START']
        self.adapter = None
        self.records = []
        self.record = {}
        self.file = None

    def parse_file(self, f):
        self.reset()
        self.file = open(f, "r")
        return self.parse()

    def parse_string(self, s):
        self.reset()
        self.file = StringIO.StringIO(s)
        return self.parse()

    def parse_record_file(self, f):
        self.reset()
        self.file = open(f, "r")
        self.state = self.states['NEW_RECORD']
        return self.parse()[0]

    def parse_record_string(self, s):
        self.reset()
        self.file = StringIO.StringIO(s)
        self.state = self.states['NEW_RECORD']
        return self.parse()[0]

    def parse(self):
        for line in self.file.readlines():
            if self.state == self.states['START']:
                self.state = self.states['ADAPTER']
                next
            elif self.state == self.states['ADAPTER']:
                self.adapter = int(line[line.strip().find("#") + 1:].strip())
                self.state = self.states['NEW_RECORD']
                next
            elif self.state == self.states['NEW_RECORD']:
                if self.record is not None and len(self.record.keys()) > 1:
                    self.records.append(self.record)
                    self.record = {"Adapter": self.adapter}
                self.state = self.states['INFO']
                next
            elif self.state == self.states['MIGHT_COULD_NEW_RECORD']:
                if len(line.strip()) == 0:
                    self.state = self.states['NEW_RECORD']
                    next
                else:
                    # intentionally not nexting here
                    self.state = self.states['INFO']
            # Intentionally not elifing in case MIGHT_COULD_NEW_RECORD is actually INFO
            if self.state == self.states['INFO']:
                if len(line.strip()) == 0:
                    self.state = self.states['MIGHT_COULD_NEW_RECORD']
                    next
                elif line.find("Exit Code") == 0:
                    self.state = self.states['EXIT']
                    break
                else:
                    try:
                        (key, value) = [ x.strip() for x in line.split(":", 1)]
                        key = key_sanitize(key)
                    except Exception, e:
                        print e
                        pass
                    self.record[key] = self.field_parsers.get(key, lambda x: x)(value)
        return self.records
