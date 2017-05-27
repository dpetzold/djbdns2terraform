from .templates import render_template


def render_managed_zone(name, domain, **kwargs):
    return render_template(
        'google_dns_managed_zone.hcl',
        name=name,
        domain=domain,
        **kwargs
    )


def render_dns_record_set(zone_name, record, **kwargs):
    return render_template(
        'google_dns_record_set.hcl',
        name=record.name.replace('*', 'star'),
        zone_name=zone_name,
        fqdn=record.fqdn,
        record_type=record.record_type,
        value=record.record_value.replace('"', ''),
        lowered_type=record.record_type.lower(),
        ttl=record.ttl or 86400,
        **kwargs
    )


def render_gcloud(zone_name, hosted_zone, records, **kwargs):
    return render_managed_zone(zone_name, hosted_zone, **kwargs) + ''.join([
        render_dns_record_set(zone_name, record, **kwargs) for record in records
    ])
