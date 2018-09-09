import health_fhir_server.mappings.patient
import health_fhir_server.mappings.condition

"""
This module contains the pesky (and somewhat tedious) mappings for GNU Health.

To search for a patient by birthdate, for example, the correct Tryton field and model must be known.

Consequently, these mappings store the allowed search parameters, fields, models, and some other required information.

Each resource requires at least one mapping.

Each mapping is a namedtuple which stores the following information:

    1) root_search: <domain>
        - does searching along this resource require some base Tryton search query?
        - For example, the basic Lab report templates are stored as singleton entries and we do not search them

    2) search_mapping: <dict: parameter: (type, (reference))
        - all search parameters, type is None (if not supported) or type of allowed value (date, string, etc)
        - what model reference(s) to search for given parameter

    3) model: <string>
        - relevant data model (e.g., gnuhealth.patient)

    4) url_prefixes: <dict>
        - if url scheme gets complicated

    5) resource: <string>
        - the intended resource (e.g., Patient)

    6) chain_map: <dict: search_paramater: target model>
        - certain parameters allow references to other resources:
            For example, Condition?subject.name=Peter will find all conditions of patient(s) named Peter
        - Store the target resources
"""
