from health_fhir_server.mappings.dataclass import ResourceMap

__all__=['Condition']

root_search=[]
url_prefixes={}
search_mapping={
        '_id': ('token', ('id')),
        '_language': None,
        'abatement-age': (None, ()),
        'abatement-boolean': (None, ()),
        'abatement-date': (None, ()),
        'abatement-string': (None, ()),
        'asserted-date': ('date', ('diagnosed_date')),
        'asserter': ('reference', ('healthprof')),
        'body-site': (None, ()),
        'category': (None, ()),
        'clinical-status': (None, ()),
        'code': ('token', ('pathology.code')),
        'code:text': ('token', ('pathology.name')),
        'context': (None, ()),
        'encounter': (None, ()),
        'evidence': (None, ()),
        'evidence-detail': (None, ()),
        'identifier': (None, ('id')),
        'onset-age': (None, ()),
        'onset-date': (None, ()),
        'onset-info': (None, ()),
        'patient': ('reference', ('name')),
        'severity': ('token', ('disease_severity')),
        'stage': (None, ()),
        'subject': ('reference', ('name')),
        'verification-status': (None, ())
        }

chain_map={'subject': 'Patient', 'patient': 'Patient'}
search_mapping={
        '_id': ['id'],
        'subject': ['name'],
        'asserter': ['healthprof'],
        'date-asserted': ['diagnosed_date'],
        'severity': ['disease_severity'],
        'code': ['pathology.code'],
        'code:text': ['pathology.name']}

model_mapping={'gnuhealth.patient.disease':
        {
            'asserter': 'healthprof',
            'dateAsserted': 'diagnosed_date',
            'severity': 'disease_severity',
            'abatementDate': 'healed_date',
            'code': 'pathology'
        }}

Condition = ResourceMap(resource='Condition', model='gnuhealth.patient.disease', search_mapping=search_mapping, root_search=[], chain_map=chain_map, url_prefixes={})
