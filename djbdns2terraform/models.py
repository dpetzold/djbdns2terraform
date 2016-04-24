class Record():
    def __init__(self, fqdn, v, ttl, timestamp=None):
        self.fqdn = fqdn
        self.v = v
        self.ttl = ttl
        self.timestamp = timestamp

    @property
    def name(self):
        return self.fqdn.replace('.', '-')

    @property
    def record_value(self):
        return self.v

    def __str__(self):
        return '{} {}'.format(self.record_type, self.fqdn)


class ARecord(Record):
    record_type = 'A'


class TxtRecord(Record):
    record_type = 'TXT'


class CnameRecord(Record):
    record_type = 'CNAME'


class MxRecord(Record):
    record_type = 'MX'

    def __init__(self, *args):
        args = list(args)
        self.x = args.pop(2)
        super(MxRecord, self).__init__(*args)

    @property
    def record_value(self):
        return '10 {}'.format(self.x)
