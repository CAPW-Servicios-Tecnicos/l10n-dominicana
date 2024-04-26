from odoo import models, fields, api, _
import requests
import xml.etree.ElementTree as ET
import json


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def get_contribuyentes(self, vat):
        rnc = vat  # Use the passed parameter directly
        if not rnc or len(rnc) not in (9, 11):
            warning_message = _(
                'No es una secuencia valida de Cedula o RNC, puede continuar si no estas validando este dato de lo '
                'contrario verificar %s') % rnc
            return {'warning': {'title': _('Warning'), 'message': warning_message}}

        # SOAP Request Setup
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
        url = "https://dgii.gov.do/wsMovilDGII/WSMovilDGII.asmx?WSDL"
        headers = {"Content-Type": "application/soap+xml; charset=utf-8"}

        # Sending the SOAP request
        response = requests.post(url, data=soap_request, headers=headers)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                result_element = root.find('.//{http://dgii.gov.do/}GetContribuyentesResult')
                if result_element is None:
                    raise ValueError("The desired element was not found in the XML response")

                data_dict = json.loads(result_element.text)
                estatus = data_dict.get('ESTATUS')
                if estatus == "0":
                    return self._generate_warning_message(rnc, data_dict, 'SUSPENDIDO')
                elif estatus == "2":
                    return {'name': data_dict['RGE_NOMBRE']}
                elif estatus == "3":
                    return self._generate_warning_message(rnc, data_dict, 'DADO DE BAJA')

            except Exception as e:
                error_message = _('Error processing response from DGII: %s') % str(e)
                return {'warning': {'title': _('Error'), 'message': error_message}}
        else:
            error_message = _('Request failed with status code: %s') % response.status_code
            return {'warning': {'title': _('Error'), 'message': error_message}}

    def _generate_warning_message(self, rnc, data_dict, status):
        warning_message = _(
            'Este contribuyente se encuentra inactivo. \n\nCédula/RNC: %s\nNombre/Razón Social: %s\nEstado: %s') % (
                          rnc, data_dict["RGE_NOMBRE"], status)
        return {'warning': {'title': _('Warning'), 'message': warning_message}}
