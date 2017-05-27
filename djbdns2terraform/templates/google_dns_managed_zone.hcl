resource "google_dns_managed_zone" "${name}" {
  name = "${name}"
  dns_name = "${domain}"
  project = "${project}"
}

