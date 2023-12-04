from odoo import models, fields, api, _
import requests
import xml.etree.ElementTree as ET
import json
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = "res.partner"

    search_successful = fields.Boolean(string='Search Successful', default=False)
    search_result = fields.Char(string='Search Result')

    @api.onchange('vat')
    def get_contribuyentes(self):
        rnc = self.vat
        if rnc:
            # Define the SOAP envelope with your request
            soap_request = f"""<?xml version="1.0" encoding="utf-8"?>
                <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                    xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
                    <soap12:Body>
                        <GetContribuyentes xmlns="http://dgii.gov.do/">
                            <value>{rnc}</value>
                            <patronBusqueda>0</patronBusqueda>
                            <inicioFilas>0</inicioFilas>
                            <filaFilas>1</filaFilas>
                            <IMEI></IMEI>
                        </GetContribuyentes>
                    </soap12:Body>
                </soap12:Envelope>"""

            # Define the URL of the SOAP web service
            url = "https://dgii.gov.do/wsMovilDGII/WSMovilDGII.asmx?WSDL"

            # Define the headers for the SOAP request
            headers = {
                "Content-Type": "application/soap+xml; charset=utf-8",
            }

            # Make a POST request with the SOAP envelope as the request body
            response = requests.post(url, data=soap_request, headers=headers)

            # Check the status code of the response
            if response.status_code == 200:
                # Decode the binary response content to a string
                response_xml = response.content.decode('utf-8')

                # Parse the XML response
                root = ET.fromstring(response_xml)

                # Find the desired element by its tag name
                result_element = root.find('.//{http://dgii.gov.do/}GetContribuyentesResult')
                data_dict = json.loads(result_element.text)

                # Check if the element exists
                if data_dict:
                    # Print the text content of the element
                    print(result_element.text)
                    self.name = data_dict["RGE_NOMBRE"]
                    self.search_result = "DATOS ENCONTRADOS"
                else:
                    self.search_result = False
                    warning_message = 'No se encontraron datos registrados de este contribuyente (%s)' % rnc
                    return {'warning': {'title': _('Warning'), 'message': warning_message}}

                # notificacion = {
                #     'type': 'ir.actions.client',
                #     'tag': 'display_notification',
                #     'params': {
                #         'title': _('Warning'),
                #         'message': 'No se encontraron datos registrados de este contribuyente (%s)' % rnc,
                #         'sticky': False,
                #         'type': 'warning',
                #         'next': {'type': 'ir.actions.act_window_close'},
                #     }
                # }
                # return notificacion
            else:
                # Handle any errors, such as non-200 status codes
                print(f"Request failed with status code {response.status_code}")
