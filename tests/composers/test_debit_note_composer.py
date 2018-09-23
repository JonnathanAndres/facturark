import io
from pytest import fixture, mark
from lxml.etree import QName, fromstring, tostring
from facturark.xsd_parser import parse_xsd
from facturark.composers import NS
from facturark.resolver import resolve_debit_note_composer


@fixture
def composer():
    return resolve_debit_note_composer()


@fixture
def data_dict():
    return {
        'extensions': [
            {
                'extension_content': {}
            }
        ],
        "id": "F0001",
        "uuid": "a3d6c86a71cbc066aaa19fd363c0fe4b5778d4a0",
        "issue_date": "2018-09-13",
        "issue_time": "00:31:40",
        "document_currency_code": "COP",
        "accounting_supplier_party": {
            'additional_account_id': 1,
            'party': {
                'party_identification': {
                    'id': {
                        '@attributes': {
                            'schemeAgencyID': '123',
                            'schemeAgencyName': 'CIA',
                            'schemeID': '007'
                        },
                        '#text':  '900555666'
                    }
                },
                'party_tax_scheme': {
                    'tax_level_code': '0'
                },
                'party_legal_entity': {
                    'registration_name': '800777555'
                },
                'person': {
                    'first_name': "Gabriel",
                    'family_name': "Echeverry"
                },
                'physical_location': {
                    'address': {
                        'department': u'Valle',
                        'city_name': u'Cali',
                    }
                }
            }
        },
        "accounting_customer_party": {
            'additional_account_id': 1,
            'party': {
                'party_identification': {
                    'id': {
                        '@attributes': {
                            'schemeAgencyID': '123',
                            'schemeAgencyName': 'CIA',
                            'schemeID': '007'
                        },
                        '#text':  '900555666'
                    }
                },
                'party_tax_scheme': {
                    'tax_level_code': '0'
                },
                'party_legal_entity': {
                    'registration_name': '800777555'
                },
                'person': {
                    'first_name': "Gabriel",
                    'family_name': "Echeverry"
                },
                'physical_location': {
                    'address': {
                        'department': u'Valle',
                        'city_name': u'Cali',
                    }
                }
            }
        },
        "legal_monetary_total": {
            'line_extension_amount': {
                '@attributes': {'currencyID': 'COP'},
                '#text': 888888
            },
            'tax_exclusive_amount': {
                '@attributes': {'currencyID': 'COP'},
                '#text': 55555
            },
            'payable_amount': {
                '@attributes': {'currencyID': 'COP'},
                '#text': 4444
            }
        },
        "debit_note_lines": [
            {
                'id': '1',
                'invoiced_quantity': '99',
                'line_extension_amount': {
                    '@attributes': {'currencyID': 'COP'},
                    '#text': 9876000
                },
                'item': {
                    'description': "Line 1"
                },
                'price': {
                    'price_amount': {
                        '@currency_id': 'COP',
                        '#text': 567
                    }
                }
            }
        ]
    }


def test_compose(composer, data_dict, schema):
    debit_note = composer.compose(data_dict)

    assert debit_note.prefix == "fe"
    assert debit_note.tag == QName(NS.fe, "DebitNote").text
    assert debit_note.findtext(QName(NS.cbc, "UBLVersionID")) == "UBL 2.0"
    assert debit_note.findtext(QName(NS.cbc, "ProfileID")) == "DIAN 1.0"
    assert debit_note.findtext(QName(NS.cbc, "ID")) == "F0001"
    assert debit_note.findtext(QName(NS.cbc, "UUID")) == (
        "a3d6c86a71cbc066aaa19fd363c0fe4b5778d4a0")
    assert debit_note.findtext(QName(NS.cbc, "IssueDate")) == "2018-09-13"
    assert debit_note.findtext(QName(NS.cbc, "IssueTime")) == "00:31:40"
    assert debit_note.findtext(QName(NS.cbc, "DocumentCurrencyCode")) == "COP"

    schema.assertValid(debit_note)