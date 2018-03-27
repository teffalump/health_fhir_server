from flask import Response
from server.common.fhir_exception import FHIRException
from server.fhir.base_classes import Resource

class FHIRResponse(Response):
    """This class handles all FHIR responses"""

    def __init__(self, *args, **kwargs):
        """Handle FHIRException, FHIR classes, and dicts"""

        r = kwargs.get('response')
        if isinstance(r, FHIRException):
            if r.status is not None:
                kwargs['status'] = r.status
            if r.response is not None:
                r = r.getUnicodeResponseString()

        elif isinstance(r, Resource):
            r = unicode(r.export_to_xml_string())

        elif isinstance(r, dict):
            r = unicode(r.get('message', 'Unknown return'))

        else:
            pass

        # Set correct value (possibly unchanged)
        kwargs['response'] = r

        super(FHIRResponse, self).__init__(*args, **kwargs)
