from flask import Blueprint, request, url_for
from StringIO import StringIO
from lxml.etree import XMLSyntaxError
from server.health_fhir import (health_RelatedPerson, health_OperationOutcome,
                parse, parseEtree, Bundle, find_record, health_Search)
from trytond.transaction import Transaction
from server.common import tryton, Resource, search_error_string, get_userid
import lxml
import os.path
import sys

# RelatedPerson models
related_person = tryton.pool.get('gnuhealth.family_member')
patient = tryton.pool.get('gnuhealth.patient')

class RP_Create(Resource):
    @tryton.transaction(user=get_userid)
    def post(self):
        '''Create interaction'''
        return 'Not implemented', 405

class RP_Search(Resource):
    @tryton.transaction(user=get_userid)
    def get(self):
        '''Search interaction'''
        # NOTE We search from patient first, not related_person
        try:
            # FIX This is so ugly, I'm ashamed

            # If there is a patient reference
            #   we need to use the patient search
            s = health_Search(endpoint='related_person')
            full_search_info=s.parse_url_string(request.args)
            pat_info=[x for x in full_search_info if x['key'] == 'patient']
            patients=[]
            if pat_info:
                full_search_info=[x for x in full_search_info if x not in pat_info]

            pat_query=s.single_model_query_generate(pat_info)
            pat_query.append(('family', '!=', None))

            # Patients who have families and pass the tests
            patients = [x for x in patient.search(pat_query)]

            # Now generate the rest of the query
            rp_query=s.single_model_query_generate(full_search_info)

            # There must be patients who have family members
            if patients:
                rp_query.extend('name.id', 'in', [x.family.id for x in patients])
            else:
                return 'no members', 404

            total_recs = related_person.search_count(query)
            per_page = int(request.args.get('_count', 10))
            page = int(request.args.get('page', 1))
            bd=Bundle(request=request,
                            total=total_recs,
                            per_page = per_page,
                            page = page)
            offset = (page-1) * per_page

            for rp in related_person.search(query,
                                        offset=offset,
                                        limit=per_page):
                # Multiple patients in same family
                for pat in patients:
                    try:
                        p = health_RelatedPerson(gnu_record=rp)
                    except:
                        continue
                    else:
                        bd.add_entry(p)
            if bd.entries:
                return bd, 200
            else:
                oo=health_OperationOutcome()
                oo.add_issue(details=search_error_string(request.args),
                        severity='warning')
                return oo, 403
        except:
            oo=health_OperationOutcome()
            oo.add_issue(details=sys.exc_info()[1], severity='fatal')
            return oo, 400

class RP_Validate(Resource):
    @tryton.transaction(user=get_userid)
    def post(self, log_id=None):
        '''Validate interaction'''
        try:
            # 1) Must correctly parse as XML
            c=StringIO(request.data)
            doc=lxml.etree.parse(c)
            c.close()
        except XMLSyntaxError as e:
            oo=health_OperationOutcome()
            oo.add_issue(details=e, severity='fatal')
            return oo, 400

        except:
            e = sys.exc_info()[1]
            oo=health_OperationOutcome()
            oo.add_issue(details=e, severity='fatal')
            return oo, 400

        else:
            if os.path.isfile('schemas/related_person.xsd'):
                # 2) Validate against XMLSchema
                with open('schemas/related_person.xsd') as t:
                    sch=lxml.etree.parse(t)

                xmlschema=lxml.etree.XMLSchema(sch)
                if not xmlschema.validate(doc):
                    error = xmlschema.error_log.last_error
                    oo=health_OperationOutcome()
                    oo.add_issue(details=error.message, severity='error')
                    return oo, 400
            else:
                # 2) If no schema, check if it correctly parses to a RelatedPerson
                try:
                    pat=parseEtree(StringIO(doc))
                    if not isinstance(pat, health_RelatedPerson):
                        oo=health_OperationOutcome()
                        oo.add_issue(details='Not a related_person resource', severity='error')
                        return oo, 400
                except:
                    e = sys.exc_info()[1]
                    oo=health_OperationOutcome()
                    oo.add_issue(details=e, severity='fatal')
                    return oo, 400

            if log_id:
                # 3) Check if related_person exists
                record = related_person.search([('id', '=', log_id)])
                if not record:
                    oo=health_OperationOutcome()
                    oo.add_issue(details='No related_person', severity='error')
                    return oo, 422
                else:
                    #TODO: More checks
                    return 'Valid update', 200
            else:
                # 3) Passed checks
                return 'Valid', 200

class RP_Record(Resource):
    @tryton.transaction(user=get_userid)
    def get(self, log_id):
        '''Read interaction'''
        records = related_person.search([('id', '=', log_id)])
        if records:
            d=health_RelatedPerson(gnu_record=record)
            return d, 200
        else:
            oo=health_OperationOutcome()
            oo.add_issue(details='No record', severity='error')
            return oo, 404

    @tryton.transaction(user=get_userid)
    def put(self, log_id):
        '''Update interaction'''
        return 'Not supported', 405

    @tryton.transaction(user=get_userid)
    def delete(self, log_id):
        '''Delete interaction'''
        return 'Not implemented', 405

class RP_Version(Resource):
    @tryton.transaction(user=get_userid)
    def get(self, log_id, v_id=None):
        '''Vread interaction'''
        return 'Not supported', 405

__all__=['RP_Create', 'RP_Search', 'RP_Version', 'RP_Validate', 'RP_Record']
