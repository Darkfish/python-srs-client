# python-srs-client
Minimalist script for manually executing .nz SRS XML commands with GPG auth via gpgme

## Notes

Seems to work with the Ubuntu 14.04 versions of gpg and gpgme, but doesn't seem so happy on Ubuntu 16.04 yet (unable to locate signing key).

## Prerequisites
- gpg
- python-gpgme
- python-lxml

## Usage

```
$ python srsclient.py --gpgid 8165E239 --regid 945 test.xml
2018-02-14 07:34:08,882 INFO Running with lxml.etree
2018-02-14 07:34:08,884 INFO  - Making HTTPS connection to srstest.srs.net.nz
2018-02-14 07:34:09,821 INFO  - Trying to use GPG key "8165E239"
2018-02-14 07:34:10,754 INFO Sending test.xml
2018-02-14 07:34:11,281 INFO   - Making request to: /srs/registrar
2018-02-14 07:34:11,281 INFO   - Connection request headers:
2018-02-14 07:34:11,281 INFO   -- Content-type: application/x-www-form-urlencoded
2018-02-14 07:34:11,281 INFO   -- Accept: text/plain
2018-02-14 07:34:11,281 INFO   - HTTP 'n' parameter is: 945
2018-02-14 07:34:11,585 INFO   - Connection response headers:
2018-02-14 07:34:11,586 INFO   -- content-length: 782
2018-02-14 07:34:11,586 INFO   -- x-powered-by: Perl Dancer 1.312
2018-02-14 07:34:11,586 INFO   -- server: Perl Dancer 1.312
2018-02-14 07:34:11,586 INFO   -- date: Wed, 14 Feb 2018 07:34:09 GMT
2018-02-14 07:34:11,586 INFO   -- content-type: application/x-www-form-urlencoded
2018-02-14 07:34:11,586 INFO   -- x-resource-consent: RegistrarRequestLimit,1,15
2018-02-14 07:34:11,586 INFO   - Connection response: 200 OK
2018-02-14 07:34:11,587 INFO   - Done, printing XML response:

2018-02-14 07:34:11,588 INFO
<NZSRSResponse VerMinor="13" RegistrarId="945" VerMajor="7">
  <Response FeId="7" Action="Whois" FeSeq="1343241859" OrigRegistrarId="945" RecipientRegistrarId="945">
    <FeTimeStamp Hour="20" Second="09" Minute="34" Month="02" Year="2018" TimeZoneOffset="+13:00" Day="14"/>
    <Domain DomainName="nzrs.net.nz" Status="Active"/>
  </Response>
</NZSRSResponse>
```
