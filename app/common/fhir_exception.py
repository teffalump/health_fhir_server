from server.fhir.operation_outcome import OperationOutcome

class FHIRException(Exception):
    """Base exception class for FHIR

    Attributes:
        http_status (int): HTTP status code to return
        response (str or OperationOutcome): The response to return
    """

    def __init__(self, http_status=400, details='', response=None):
        """Initialize status code and response"""

        super(FHIRException, self).__init__(details)
        self.http_status =  http_status
        self.response = response

        if not isinstance(self.http_status, int):
            raise ValueError('Must be integer status code')

        if self.response is None:
            raise ValueError('Need an OperationOutcome or message')

        if not isinstance(self.response, (basestring, OperationOutcome)):
            raise ValueError('Not a valid response object: string or OperationOutcome')

    def getUnicodeResponseString(self):
        """Output unicode string for response"""

        if self.response:
            if hasattr(self.response, 'export_to_xml_string'):
                return unicode(self.response.export_to_xml_string())
            else:
                return unicode(self.response)

class SearchException(FHIRException):
    """Search related errors (e.g., bad parameters)"""

    def __init__(self, *args, **kwargs):
        """Force 403 HTTP status code"""

        t = kwargs.pop('http_status')
        kwargs['http_status']=403
        if not isinstance(kwargs.get('response'), OperationOutcome):
            raise ValueError("This error must have an OperationOutcome")
        super(SearchException, self).__init__(*args, **kwargs)

class ParseException(FHIRException):
    """Syntax errors related to the document"""

    def __init__(self, *args, **kwargs):
        if not isinstance(kwargs.get('response'), OperationOutcome):
            raise ValueError("This error must have an OperationOutcome")
        super(ParseException, self).__init__(*args, **kwargs)

class ValidationException(FHIRException): 
    """Various errors related to validation"""

    def __init__(self, *args, **kwargs):
        if not isinstance(kwargs.get('response'), OperationOutcome):
            raise ValueError("This error must have an OperationOutcome")
        super(ValidationException, self).__init__(*args, **kwargs)

class ResourceException(FHIRException):
    """Handles general resource errors (e.g., unsupported)"""

    pass
