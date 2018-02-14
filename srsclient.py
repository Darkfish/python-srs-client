import time
import gpgme
import logging
import argparse
import httplib
import urllib
import urlparse

#: Log items
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)

try:
    from lxml import etree
    logging.info("Running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
        logging.info("Running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
            logging.info("Running with ElementTree on Python 2.5+")
        except ImportError:
            logging.error("Failed to import ElementTree")

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


#: Parse arguments
parser = argparse.ArgumentParser(
    description='Send prepared XML files to EPP server'
)
parser.add_argument(
    'xmlfiles',
    metavar='xmlfile',
    type=str,
    nargs='+',
    help='XML Input Files'
)
parser.add_argument(
    '--regid',
    nargs='?',
    default='60',
    help='Registrar ID'
)
parser.add_argument(
    '--gpgid',
    nargs='?',
    default='',
    help='GPG key ID used to sign request'
)
parser.add_argument(
    '--server',
    nargs='?',
    default='srstest.srs.net.nz',
    help='EPP server hostname or ip'
)

args = parser.parse_args()


class srs(object):
    def __init__(self):
        #: Make connection to SRS
        logging.info(' - Making HTTPS connection to {0}'.format(args.server))
        self.connection = httplib.HTTPSConnection(args.server, timeout=301)
        self.signer = srsgpg()
        self.key = self.signer.find_key(args.gpgid)
        self.reg = args.regid
        self.url = '/srs/registrar'

    def __del__(self):
        #: Close connection to SRS
        self.connection.close()

    def request(self, req_input):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"
        }

        try:
            parser = etree.XMLParser(resolve_entities=False)
        except TypeError:
            parser = etree.XMLParser()

        #: Sign our message with GPG key
        req_sig = self.signer.sign(req_input, self.key)

        #: Send request
        params = urllib.urlencode(
            {'n': self.reg, 'r': req_input, 's': req_sig}
        )

        #: Set URL
        url = self.url

        #: Print debug header items (WR#213484)
        logging.info("  - Making request to: {0}".format(url))
        logging.info("  - Connection request headers:")
        for header, value in headers.iteritems():
            logging.info('  -- {0}: {1}'.format(header, value))
        logging.info("  - HTTP 'n' parameter is: {0}".format(self.reg))

        #: Send request
        self.connection.request("POST", url, params, headers)

        #: Parse response
        httpresponse = self.connection.getresponse()
        logging.info("  - Connection response headers:")
        for header, value in httpresponse.getheaders():
            logging.info('  -- {0}: {1}'.format(header, value))
        logging.info("  - Connection response: {0} {1}".format(
            httpresponse.status,
            httpresponse.reason.strip())
        )
        querystring = urlparse.parse_qs(httpresponse.read())

        #: Import the XML
        try:
            xml = etree.fromstring(querystring['r'][0], parser)
        except TypeError:
            xml = etree.fromstring(querystring['r'][0])

        #: Try to pretty print the XML to STDOUT
        try:
            xml_string = etree.tostring(xml, pretty_print=True)
        except TypeError:
            xml_string = etree.tostring(xml)
        logging.info('  - Done, printing XML response:\n')
        logging.info('\n'+xml_string)


class srsgpg(object):
    def __init__(self):
        self.ctx = gpgme.Context()

    def find_key(self, keyitem):
        logging.info(' - Trying to use GPG key "{0}"'.format(keyitem))
        return(self.ctx.get_key(keyitem))

    def sign(self, message, key):
        self.ctx.armor = True
        self.ctx.signers = [key]
        plaintext = BytesIO(message)
        signature = BytesIO()

        #: Sign message with key
        self.ctx.sign(plaintext, signature, gpgme.SIG_MODE_DETACH)
        signature.seek(0, 0)
        return(signature.read())

#: Connect to SRS server
client = srs()

for fname in args.xmlfiles:
    with open(fname, 'r') as f:
        logging.info('Sending {0}'.format(fname))
        client.request(f.read())
        time.sleep(1)
