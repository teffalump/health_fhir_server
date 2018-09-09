from health_fhir_server.mappings.dataclass import ResourceMap

__all__=['Patient']

model_mapping={
            'gnuhealth.patient': {
                'active': 'name.active',
                'birthDate': 'name.dob',
                'identifier': 'puid',
                'alternative': 'name.alternative_ids',
                'gender': 'name.sex',
                'contacts': 'name.contact_mechanisms',
                'photo': 'photo',
                'phone': 'name.phone',
                'email': 'name.email',
                'mobile': 'name.mobile',
                'given': 'name.name',
                'family': 'name.lastname',
                'nickname': 'name.alias',
                'maritalStatus': 'name.marital_status',
                'careProvider': 'primary_care_doctor',
                'communication': 'name.lang',
                'deceased': 'deceased',
                'deceasedDateTime': 'dod',
                'address': 'name.du',
                }}

search_mapping={
                '_id': ('token', ('id')),
                '_language': (None, ()),
                'active': (None, ('name.active')), #FIX boolean conversion
                'address': (None, ('name.du')), #TODO Add searcher
                'address-city': (None, ()),
                'address-country': (None, ()),
                'address-postalcode': (None, ()),
                'address-state': (None, ()),
                'address-use': (None, ()),
                'animal-breed': (None, ()),
                'animal-species': (None, ()),
                'birthdate': ('date', ('name.dob')),
                'death-date': (None, ('deceasedDateTime')), #TODO Test
                'deceased': (None, ('deceased')), #FIX boolean conversion
                'email': (None, ('name.email')), #FIX No searcher
                'family': ('string', ('name.lastname')),
                'gender': ('token', ('name.sex')),
                'general-practitioner': (None, ('primary_care_doctor')),
                'given': ('string', ('name.name')),
                'identifier': ('token', ('puid')),
                'language': ('token', ('name.lang.code')),
                'link': (None, ()),
                'name': ('string', ('name.lastname', 'name.name')),
                'organization': (None, ()),
                'phonetic': (None, ()),
                'phone': (None, ('name.phone', 'name.mobile')), #FIX No searcher
                'telecom': (None, ('name.email', 'name.phone', 'name.mobile')) #FIX No searcher
                }

Patient = ResourceMap('Patient', resource='Patient', model='gnuhealth.patient', root_search=[], search_mapping=search_mapping, url_prefixes={}, chain_map={})
