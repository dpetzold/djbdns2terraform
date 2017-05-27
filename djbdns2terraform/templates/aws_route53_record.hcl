resource "aws_route53_record" "${lowered_type}-${name}" {
    zone_id = "$${{aws_route53_zone.${zone_name}.zone_id}}"
    name = "${fqdn}"
    type = "${record_type}"
    records = ["${value}"]
    ttl = ${ttl}
}

