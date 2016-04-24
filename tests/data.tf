resource "aws_route53_zone" "example.com" {
  name = "example-com"
}

resource "aws_route53_record" "a-www-example-com" {
    zone_id = "${aws_route53_zone.example.com.zone_id}"
    name = "www.example.com"
    type = "A"
    records = ["184.73.222.205"]
    ttl = 86400
}

resource "aws_route53_record" "mx-mx-example-com" {
    zone_id = "${aws_route53_zone.example.com.zone_id}"
    name = "mx.example.com"
    type = "MX"
    records = ["10 mx.sendgrid.com."]
    ttl = 86400
}

resource "aws_route53_record" "cname-sendgrid-example-com" {
    zone_id = "${aws_route53_zone.example.com.zone_id}"
    name = "sendgrid.example.com"
    type = "CNAME"
    records = ["u1958070.wl.sendgrid.net."]
    ttl = 86400
}

resource "aws_route53_record" "cname-media-example-com" {
    zone_id = "${aws_route53_zone.example.com.zone_id}"
    name = "media.example.com"
    type = "CNAME"
    records = ["s3.amazonaws.com"]
    ttl = 86400
}

resource "aws_route53_record" "txt-example-com" {
    zone_id = "${aws_route53_zone.example.com.zone_id}"
    name = "example.com"
    type = "TXT"
    records = ["v=spf1 a mx include\072u1958070.wl.sendgrid.net -all"]
    ttl = 86400
}

resource "aws_route53_record" "txt-mail-_domainkey-example-com" {
    zone_id = "${aws_route53_zone.example.com.zone_id}"
    name = "mail._domainkey.example.com"
    type = "TXT"
    records = ["k=rsa; t=y; p= MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDNepxMEiaxBmNZTpC2c557qCXuFdLvxiJwHNCfBjncf1Ju9wCENCwggW7L/6G7tSBDAHBscEwD3JEpBwinkevaSGlgFuMAfygHGICcZkzJAMs3LxxYoudz3R2twHzm4oCI1A6ZRXBhIZuiPZLJRY7me8hE+bjyUIXrA2245SDlHwIDAQAB"]
    ttl = 600
}

