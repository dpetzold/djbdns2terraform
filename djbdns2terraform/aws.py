from .templates import render_template


def render_hosted_zone(name, domain):

    return render_template(
        'aws_route53_zone.hcl',
        name=name,
        domain=domain,
    )


def render_resource_record(zone_name, record):

    return render_template(
        'aws_route53_record.hcl',
        name=record.name.replace('*', 'star'),
        zone_name=zone_name,
        fqdn=record.fqdn,
        record_type=record.record_type,
        value=record.record_value.replace('"', ''),
        lowered_type=record.record_type.lower(),
        ttl=record.ttl or 86400,
    )


def render_aws(zone_name, hosted_zone, records):
    return render_hosted_zone(zone_name, hosted_zone) + ''.join([
        render_resource_record(zone_name, record) for record in records
    ])
