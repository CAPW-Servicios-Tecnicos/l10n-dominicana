from odoo import models, fields, api, _
import requests
import xml.etree.ElementTree as ET
import json


def get_contribuyentes(self):
    rnc = self.vat
    data_dict = {}
    if rnc:
        if len(rnc) not in (9, 11):
            warning_message = (f'No es una secuencia valida de Cedula o RNC, puede continuar si no estas validando este '
                               f'dato de lo contrario verificar {rnc}')
            return {'warning': {'title': _('Warning'), 'message': warning_message}}
        else:
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
            headers = {
                "Content-Type": "application/soap+xml; charset=utf-8",
            }

            response = requests.post(url, data=soap_request, headers=headers)

            if response.status_code == 200:
                response_xml = response.content.decode('utf-8')
                root = ET.fromstring(response_xml)
                result_element = root.find('.//{http://dgii.gov.do/}GetContribuyentesResult')

                if result_element is not None:
                    try:
                        data_dict = json.loads(result_element.text)
                    except json.JSONDecodeError:
                        warning_message = 'Error en la conexion con la DGII trate un poco mas tarde' % rnc
                        return {'warning': {'title': _('Warning'), 'message': warning_message}}
                else:
                    print("The desired element was not found in the XML response")

                if data_dict:
                    if data_dict['ESTATUS'] == "0":
                        warning_message = ('Este contribuyente se escuentra inativo. \n\nCédula/RNC: %s\nNombre/Razón '
                                           'Social: %s\nEstado: SUSPENDIDO') % (
                            rnc, data_dict["RGE_NOMBRE"])
                        return {'warning': {'title': _('Warning'), 'message': warning_message}}
                    elif data_dict['ESTATUS'] == "2":
                        self.name = data_dict['RGE_NOMBRE']
                    elif data_dict['ESTATUS'] == "3":
                        warning_message = ('Este contribuyente se escuentra Dado de Baja. \n\nCédula/RNC: %s\nNombre/Razón '
                                           'Social: %s\nEstado: DADO DE BAJA') % (
                            rnc, data_dict["RGE_NOMBRE"])
                        return {'warning': {'title': _('Warning'), 'message': warning_message}}
                else:
                    warning_message = 'No se encontraron datos registrados de este contribuyente (%s)' % rnc
                    return {'warning': {'title': _('Warning'), 'message': warning_message}}
            else:
                print(f"Request failed with status code {response.status_code}")
