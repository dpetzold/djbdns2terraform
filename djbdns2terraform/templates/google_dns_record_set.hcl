resource "google_dns_record_set" "${lowered_type}-${name}" {
  managed_zone = "$${google_dns_managed_zone.${zone_name}.name}"
  name = "${fqdn}."
  type = "${record_type}"
  ttl = ${ttl}
  rrdatas = ["${value}"]
  project = "${project}"
}

