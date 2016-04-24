import os

CONFIG = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
HCL = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data.tf'))

from djbdns2terraform.__main__ import parse_data_file, get_hcl


def test_get_hcl():

    records = parse_data_file(CONFIG)
    zone_data = get_hcl('example.com', 'example-com', records['example.com'])
    assert zone_data == open(HCL).read()
