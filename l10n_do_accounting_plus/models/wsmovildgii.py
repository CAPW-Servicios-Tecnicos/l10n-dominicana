import requests


def get_contribuyentes(rnc):

    # Define the SOAP envelope with your request
    soap_request = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
      <soap12:Body>
        <GetContribuyentes xmlns="http://dgii.gov.do/">
          <value>{rnc}</value>
          <patronBusqueda>0</patronBusqueda>
          <inicioFilas>0</inicioFilas>
          <filaFilas>1</filaFilas>
          <IMEI></IMEI>
        </GetContribuyentes>
      </soap12:Body>
    </soap12:Envelope>
    """

    # Define the URL of the SOAP web service
    url = "https://dgii.gov.do/wsMovilDGII/WSMovilDGII.asmx?WSDL"

    # Define the headers for the SOAP request
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8",
        "Content-Length": str(len(soap_request)),
    }

    # Make a POST request with the SOAP envelope as the request body
    response = requests.post(url, data=soap_request, headers=headers)

    # Check the status code of the response
    if response.status_code == 200:
        # The request was successful, and you can access the response content (XML)
        response_xml = response.content
        # Process the response XML as needed
        print(response_xml.decode('utf-8'))  # Decode the binary response content to a string
    else:
        # Handle any errors, such as non-200 status codes
        print(f"Request failed with status code {response.status_code}")
