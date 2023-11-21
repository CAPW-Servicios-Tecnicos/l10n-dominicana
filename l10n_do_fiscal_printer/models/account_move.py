from odoo import fields, models
import requests


def _print_fiscal_invoice():

    # SOAP request URL
    url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"

    # structured XML
    payload = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
                <soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">
                    <soap:Body>
                        <CountryIntPhoneCode xmlns=\"http://www.oorsprong.org/websamples.countryinfo\">
                            <sCountryISOCode>IN</sCountryISOCode>
                        </CountryIntPhoneCode>
                    </soap:Body>
                </soap:Envelope>"""
    # headers
    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }
    # POST request
    response = requests.request("POST", url, headers=headers, data=payload)

    # prints the response
    print(response.text)
    print(response)


class AccountMove(models.Model):
    _inherit = ['account.move']

    subsidiary = fields.Char(string="Sucursal", required=False)
    pos = fields.Char(string="Caja", required=False)
    nif = fields.Char(string="NIF", required=False)

    # def _prepare_vals_for_fiscal_invoices(self):
    #     for rec in self:
    #         rnc = rec.partner_id.nif
    #         sucursal = rec.subsidiary
    #         caja = rec.pos
    #         nif = rec.l10n_do_fiscal_number
