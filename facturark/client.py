import zeep
from random import randint
from base64 import b64encode
from datetime import datetime
from lxml.etree import tostring
from zeep.wsse.username import UsernameToken


class Client:

    def __init__(self, username, password, wsdl_url):
        nonce = b64encode(bytes(randint(0, 100000000)))
        created = datetime.now().isoformat(sep='T')

        self.client = zeep.Client(
            wsdl_url,
            wsse=UsernameToken(
                username, password,
                use_digest=False,
                nonce=None, created=None))

    def send(self, vat, invoice_number, issue_date, document):
        issue_date = datetime.strptime(
            issue_date, '%Y-%m-%dT%H:%M:%S')

        response = self.client.service.EnvioFacturaElectronica(
            vat, invoice_number, issue_date, document)

        return tostring(response)

    def assemble(self, vat, invoice_number, issue_date, document):
        issue_date = datetime.strptime(
            issue_date, '%Y-%m-%dT%H:%M:%S')

        root = self.client.create_message(
            self.client.service, 'EnvioFacturaElectronica',
            vat, invoice_number, issue_date, document)

        return root

    def serialize(self, vat, invoice_number, issue_date, document):
        root = self.assemble(vat, invoice_number, issue_date, document)
        request_document = tostring(root)

        return request_document
