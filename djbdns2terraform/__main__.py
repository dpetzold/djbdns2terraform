#!/usr/bin/env python3

import argparse
from collections import defaultdict

from .models import (
    ARecord,
    MxRecord,
    CnameRecord,
    TxtRecord,
)


DEBUG = False

aws_route53_zone_tmpl = """\
resource "aws_route53_zone" "{name}" {{
  name = "{domain}"
}}

"""

aws_route53_record_tmpl = """\
resource "aws_route53_record" "{lowered_type}-{name}" {{
    zone_id = "${{aws_route53_zone.{zone_name}.zone_id}}"
    name = "{fqdn}"
    type = "{record_type}"
    records = ["{value}"]
    ttl = {ttl}
}}

"""


def get_hosted_zone(name, domain):

    return aws_route53_zone_tmpl.format(
        name=name,
        domain=domain,
    )


def get_resource_record(zone_name, record):

    return aws_route53_record_tmpl.format(
        name=record.name.replace('*', 'star'),
        zone_name=zone_name,
        fqdn=record.fqdn,
        record_type=record.record_type,
        value=record.record_value.replace('"', ''),
        lowered_type=record.record_type.lower(),
        ttl=record.ttl or 86400,
    )


def get_resource_records(zone_name, records):
    return ''.join([
        get_resource_record(zone_name, record) for record in records
    ])


def get_hcl(zone_name, hosted_zone, records):
    return get_hosted_zone(zone_name, hosted_zone) + get_resource_records(zone_name, records)


def parse_data_file(filepath):

    records = defaultdict(list)

    with open(filepath, 'r') as fp:

        for i, line in enumerate(fp):
            line = line.strip()
            if line.startswith('#') or line == '':
                continue

            parts = line.split(':')
            part0 = list(parts[0])
            prefix = part0.pop(0)
            parts[0] = ''.join(part0)

            split = parts[0].split('.')

            hosted_zone = '.'.join(split[-2:])

            if DEBUG:
                print(hosted_zone, parts)

            if prefix == '=' or prefix == '+':
                records[hosted_zone].append(ARecord(*parts))
            elif prefix == '@':
                records[hosted_zone].append(MxRecord(*parts))
            elif prefix == 'C':
                records[hosted_zone].append(CnameRecord(*parts))
            elif prefix == "'":
                records[hosted_zone].append(TxtRecord(*parts))
            elif prefix == '.':
                pass
            else:
                raise Exception(line)

    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    args = parser.parse_args()

    records = parse_data_file(args.config)

    for hosted_zone, zone_records in records.items():
        zone_name = hosted_zone.replace('.', '-')
        with open('terraform/{}-route53.tf'.format(zone_name), 'w') as f:
            f.write(get_hcl(zone_name, hosted_zone, zone_records))


if __name__ == '__main__':
    main()
