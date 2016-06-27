### Use Mocks for adapter tests

from proteus import Model, config
from ..health_fhir.adapters import patient_adapter
from datetime import datetime

# Test database with required modules already installed
config = config.set_trytond(config_file='trytond.conf',
                            database='gnuhealth_test')

Patient = Model.get('gnuhealth.patient')
Address = Model.get('gnuhealth.du')
Alt = Model.get('gnuhealth.person_alternative_identification')
Name = Model.get('gnuhealth.person_name')
Party = Model.get('party.party')

# A name
name = Mock(spec=Name)
name.use = 'official'
name.family = 'Weird'
name.given = 'NotTest'
name.prefix = 'Dr.'
name.suffix = 'III'

# Alt Identifiers
alt = Mock(spec=Alt)
alt.code = '43543534534588-TEST' 
alt.type = 'country_id'

# An address
add = Mock(spec=Address)
add.address_street_number = 1
add.address_street = 'Test Drive Road'
add.address_zip = 94949
add.address_city = 'Test City'
add.address_subdivision.name = 'Test Subdivision'
add.address_country.name = 'Great Test Country'

# A contact
contact = Mock(spec=Contact)
contact.type = 'phone'
contact.value = '345-234-2343'

# A person
party = Mock(spec=Party)
party.person_names = [name]
party.contact_mechanisms = [contact]
party.dob = datetime.now() - datetime(1980,1,1)
party.du = add
party.marital_status = 'm'
party.lang.code = 'UTF_345E'
party.lang.name = 'Binary'
party.active = True

# A patient
pat = Mock(spec=Patient)
pat.puid = '435348BN'
pat.alternative_ids = [alt]
pat.biological_sex = 'f'
pat.deceased = False
pat.primary_care_doctor.rec_name = 'Test, Dr.'
pat.primary_care_doctor.id = 34
pat.name = party

adapter = patient_adapter(pat)
