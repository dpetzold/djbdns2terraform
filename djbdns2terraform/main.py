import logging
import argparse
import os

from collections import defaultdict

from .aws import render_aws
from .gcloud import render_gcloud
from .models import (
    ARecord,
    MxRecord,
    CnameRecord,
    TxtRecord,
)

logger = logging.getLogger(__name__)


class UnknownRecordType(Exception):
    pass


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

            logger.debug(hosted_zone, parts)

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
                raise UnknownRecordType(line)

    return records


def write_records(zone_name, data, postfix):

    with open('terraform/{}{}'.format(zone_name, postfix), 'w') as f:
        f.write(data)


def process_records(records, func, postfix, stdout, **kwargs):

    for hosted_zone, zone_records in records.items():
        zone_name = hosted_zone.replace('.', '-')
        output = func(zone_name, hosted_zone + '.', zone_records, **kwargs)
        if stdout:
            print(output)
        else:
            write_records(hosted_zone, output, postfix)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gcloud', help='Generate tf for the specified project')
    parser.add_argument('--aws', action='store_true', default=False)
    parser.add_argument('--stdout', action='store_true', default=False)
    parser.add_argument('config')
    args = parser.parse_args()

    records = parse_data_file(args.config)

    if not os.path.exists('terraform'):
        os.mkdir('terraform')

    if args.aws:
        process_records(records, render_aws, '-route53.tf', args.stdout)
    elif args.gcloud:
        process_records(records, render_gcloud, '-managed-zone.tf', args.stdout, project=args.gcloud)
    else:
        parser.print_help()
