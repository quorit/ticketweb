import falcon
import jwt
import json
import re
import time
import os
import sys
import requests
import html
from ticketweb_applib.rt_module.handlers import SubmitTicket
from .config_data import config_data

class BadRequest(Exception):
    def __init__(self,message,status):
       self._message = message
       self.status = status

    def response_body(self):
       result = {
                  'message': self._message
                }
       cause = self.__cause__
       if cause:
          result['exception'] = str(cause)
       return result

    @staticmethod                     # This is like static in java
    def handle(e, req, resp, params): # These paramaters are required even though I'm only using resp and e
        resp.body = json.dumps(e.response_body())
        resp.status = e.status
        resp.content_type = falcon.MEDIA_JSON
    # i believe this function is a static because that allows me to refer to it even
    # when I don't have an object. I am registering the function with add_error_handler
    # and at that time no object is relevant




class BadRequestHeaderTooBig(BadRequest):
    def __init__(self):
         message = "'Authorization' header is too big"
         status = falcon.HTTP_REQUEST_HEADER_FIELDS_TOO_LARGE
         super().__init__(message,status)

class BadRequestHeaderBadFormatJWT(BadRequest):
    def __init__(self):
         message = "'Authorization' header does not have format, 'Bearer <jwt token>'"
         status = falcon.HTTP_BAD_REQUEST
         super().__init__(message,status)

class BadRequestHeaderBadFormatUserId(BadRequest):
    def __init__(self):
        message = "'UserId' header does not have correct format."
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)


class BadRequestHeaderBadFormatOTP(BadRequest):
    def __init__(self):
        message = "'OTP' header does not have correct format."
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)



class BadRequestHeaderBadFormatGSSAPI(BadRequest):
    def __init__(self):
         message = "'Authorization' header does not have format, 'Negotiate <token encoding>'"
         status = falcon.HTTP_BAD_REQUEST
         super().__init__(message,status)


class BadRequestExpiredToken(BadRequest):
    def __init__(self):
         message = "Token has expired."
         status = falcon.HTTP_UNAUTHORIZED # really means "unathenticated" in HTTP-speak
         super().__init__(message,status)

class BadRequestUnrecognizedMinion(BadRequest):
    def __init__(self,minion_id):
         message_fmt = "Unrecognized minion, {0}."
         message = message_fmt.format(minion_id)
         status = falcon.HTTP_UNAUTHORIZED # really means "unathenticated" in HTTP-speak
         super().__init__(message,status)

class BadRequestInvalidJWT_Token(BadRequest):
    def __init__(self):
         message = "Token is not valid."
         status = falcon.HTTP_BAD_REQUEST 
         super().__init__(message,status)

class BadRequestInvalidGSS_Token(BadRequest):
    def __init__(self):
         message = "GSS token is not valid."
         status = falcon.HTTP_BAD_REQUEST
         super().__init__(message,status)




class BadRequestRoleNotString(BadRequest):
    def __init__(self):
         message = "'role' field field in token payload is not a string."
         status = falcon.HTTP_BAD_REQUEST
         super().__init__(message,status)


class BadRequestContextNotString(BadRequest):
    def __init__(self):
         message = "'context' field field in token payload is not a string."
         status = falcon.HTTP_BAD_REQUEST
         super().__init__(message,status)


class BadRequestBadRoleName(BadRequest):
    def __init__(self):
         message =  "'role' field in token payload does not match pattern <computer_account_name>$@queensu.ca."
         status = falcon.HTTP_BAD_REQUEST
         super().__init__(message,status)

class BadRequestMissingHeader(BadRequest):
     def __init__(self,header):
          message = "'{0}' header is missing from the request.".format(header)
          status = falcon.HTTP_BAD_REQUEST
          super().__init__(message,status)

class BadRequestUnsupportedMechanism(BadRequest):
     def __init__(self):
          message = "GSSAPI Error: Unsupported mechanism requested."
          status = falcon.HTTP_BAD_REQUEST
          super().__init__(message,status)

class BadRequestBadQueryString(BadRequest):
     def __init__(self):
          message = "Unsupported query string for this route."
          status = falcon.HTTP_BAD_REQUEST
          super().__init__(message,status)

class BadRequestContextMismatch(BadRequest):
    def __init__(self):
        message = "Mismatching contexts."
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)


class BadRequestLDAPAuthFail(BadRequest):
    def __init__(self):
        message = "LDAP authentication fail."
        status = falcon.HTTP_UNAUTHORIZED
        # really means unauthenticated in HTTP-speak.
        super().__init__(message,status)


class BadRequestSecretFileIOFail(BadRequest):
    def __init__(self):
        message = "Could not open OTP secret file for user."
        status = falcon.HTTP_INTERNAL_SERVER_ERROR
        super().__init__(message,status)


class BadRequestInvalidOTP(BadRequest):
    def __init__(self):
        message = "Invalid OTP code."
        status = falcon.HTTP_UNAUTHORIZED
        # really means unauthenticated in HTTP-speak.
        super().__init__(message,status)

class BadRequestUnknownContext(BadRequest):
    def __init__(self, context):
        message = "Uknown application context, {0}".format(context)
        status = falcon.HTTP_BAD_REQUEST
        # really means unauthenticated in HTTP-speak.
        super().__init__(message,status)

class BadRequestUserNotFound(BadRequest):
    def __init__(self, user_id):
        message = "Failed to find user '{0}' in LDAP db.".format(user_id)
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)

class BadRequestNoContentReceived(BadRequest):
    def __init__(self):
        message = "No content received in request."
        status = falcon.HTTP_BAD_REQUEST
        # really means unauthenticated in HTTP-speak.
        super().__init__(message,status)

class BadRequestMultipleContentParts(BadRequest):
    def __init__(self):
        message = "Multiple parts with the 'json' name have been sent."
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)


class BadRequestContentNotJson(BadRequest):
    def __init__(self):
        message = "Part with the 'json' name cannot have mime type other than 'application/json'."
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)

class BadRequestContentNotMultipart(BadRequest):
    def __init__(self):
        message = "The request cannot have a type other than 'multipart/form-data'."
        status = falcon.HTTP_BAD_REQUEST
        super().__init__(message,status)





def create_response_body_user_data(display_name,mail):
    return {
            "display_name": display_name,
            "mail": mail
        }







def _build_dtdd(title, data,escape_data=True):
    if escape_data:
        out_data=html.escape(data)
    else:
        out_data=data
    return "<dt>" + title + ":</dt><dd>" + out_data + "</dd>"

if sys.base_prefix != sys.prefix:
    _data_path = sys.prefix + "/usr/local/share/ticketweb/applications/ithelp/shared-data"
else:
    _data_path = "/usr/local/share/ticketweb/applications/ithelp/shared-data"

def _get_shared_data():
    file = os.path.join(_data_path,"init_data.json")
    f = open(file,"r")
    shared_data = json.load(f)
    f.close()
    return shared_data




def _build_requested_before(prev_report_info):
    if not prev_report_info:
        result = _build_dtdd("Requested Before","No")
    else:
        result = _build_dtdd("Requested Before","Yes") + \
                  _build_dtdd("Previous Report Info",prev_report_info)
    return result






def _build_terms(heading,terms):
    def term_lookup(term):
        last_digit = term[-1]
        base_year= 1901
        base_strm= 1011
        season_lookup = {
            "1": "Winter",
            "5": "Summer",
            "9": "Fall"
        }
        season = season_lookup[last_digit]
        term_int = int(term)
        (year_delta,remainder) = divmod(term_int-base_strm,10)
        year_int = base_year + year_delta
        return str(year_int) + " " + season

    result = "<dt>" + heading + ":</dt>" \
             + "<dd><ul style='padding-left:0;'>" \
             + "".join(["<li>" + term_lookup(term) + " (" + term + ")</li>" for term in terms]) \
             + "</ul></dd>"

    return result


def _build_list_choices(list_choices):
    def build_list_choice(item):
        choices = list_choices[item]
        list_def = _get_shared_data()["data_lists"][item]
        header = list_def["heading"]
        result = "<dt>" + header + ":</dt>" \
                 + "<dd><ul style='padding-left:0;'>" \
                 + "".join(["<li>" + list_def["items"][choice] + "</li>" for choice in choices]) \
                 + "</ul></dd>"
        return result

    result  = "".join([build_list_choice(item) for item in list_choices])
    return result

def _build_requested_fields(requested_fields):
    result = "<dt>Requested Fields:</dt><dd><ul style='padding-left:0;'>" \
             + "".join(["<li>" + field + "</li>" for field in requested_fields]) \
             + "</ul></dd>"
    return result


def _get_xlat():
    return _get_shared_data()["xlat"]


class SubmitTicketOnboarding(SubmitTicket):
    def __init__(self):
        def get_subject(req_content):
            return "Onboarding request"

        def get_ticket_content(real_name,req_content):
            def render_f_employee_info():
                result = "<dl>" + \
                              _build_dtdd("Employee full name",req_content['employee_name']) + \
                              (_build_dtdd("Employee net id",req_content['employee_net_id']) if "employee_net_id" in req_content else "") + \
                              _build_dtdd("Employee start date",req_content['start_date']) + \
                         "</dl>"   
                return result
            
            def render_f_position_info():
                def build_employee_position():
                    job_title_data = req_content["job_title_path"]
                    if job_title_data["job_title_type"]=="standard":
                        result = " << ".join ([_get_xlat()[part] for part in job_title_data["job_title_path"]])
                    else:
                        result = html.escape(job_title_data["position_descr"]) + " <i>user input</i>"
                    
                    return result
                def build_employee_roles():
                    employee_roles = req_content["selected_roles"]
                    result = "<ul>" + \
                               "".join (["<li>" + html.escape(role) + "</li>" for role in employee_roles]) + \
                             "</ul>"                    
                    return result
                    
                replacement_pos_str = "Yes" if req_content['replacement_pos'] else 'No'
                result = "<dl>" + \
                              _build_dtdd("Is the employee replacing a former/outgoing one",
                                          replacement_pos_str) + \
                              (_build_dtdd("Name of former/outgoing employee",req_content['former_employee']) if "former_employee" in req_content else "") + \
                              _build_dtdd("Employee position",build_employee_position(),False) + \
                              (_build_dtdd("Employee roles",build_employee_roles(),False) if "selected_roles" in req_content else "") + \
                         "</dl>"   
                return result



            def render_f_work_model():
                result = "<dl>" + \
                                _build_dtdd("Employee work model",_get_xlat()[req_content['work_model_selection']]) + \
                                (_build_dtdd("Employee in-office location",_get_xlat()[req_content['room_selection']]) if 'room_selection' in req_content else "") + \
                                (_build_dtdd("Employee in-office sub-location",req_content['room_sublocation']) if 'room_sublocation' in req_content else "") + \
                        "</dl>"
                return result

            def render_f_hardware_info():
                result = "<dl>" + \
                                _build_dtdd("Employee hardware configuration",_get_xlat()[req_content['hw_choice']]) + \
                                (_build_dtdd("Reason for provisioning of laptop",req_content['laptop_explanation']) if 'laptop_explanation' in req_content else "") + \
                                (_build_dtdd("Extra hardware requirements",req_content['extra_hardware_reqs']) if 'extra_hardware_reqs' in req_content else "") + \
                        "</dl>"
                return result

            def render_f_phone_info():
                def build_ring_groups():
                    ring_groups=req_content['ring_groups']
                    return "<ul>" + \
                               "".join (["<li>" + html.escape(ring_group) + "</li>" for ring_group in ring_groups]) + \
                           "</ul>"
                def build_call_queues():
                    call_queues=req_content['call_queues']
                    return "<ul>" + \
                               "".join (["<li>" + html.escape(call_queue) + "</li>" for call_queue in call_queues]) + \
                           "</ul>"
                result = "<dl>" + \
                             _build_dtdd("Employee personal phone extension info",_get_xlat()[req_content['phone_ext_choice']]) + \
                             (_build_dtdd("Ring groups",build_ring_groups(),False) if "ring_groups" in req_content else "") + \
                             (_build_dtdd("Call queues",build_call_queues(),False) if "call_queues" in req_content else "") + \
                        "</dl>"
                return result



            def render_f_supplementary_prnts():
                    s_prnts = req_content['supp_print_choice']
                    result = "<ul>" + \
                                "".join (["<li>" + _get_xlat()[sp] + "</li>" for sp in s_prnts]) + \
                            "</ul>"    
                    return result
            def render_f_file_shares():
                    s_prnts = req_content['selected_file_shares']
                    result = "<ul>" + \
                                "".join (["<li>" + html.escape(sp) + "</li>" for sp in s_prnts]) + \
                            "</ul>"    
                    return result

            def render_f_supplementary_mls():
                def build_supp_mls():
                    supp_ml_choice=req_content['supp_ml_choice']
                    return "<ul>" + \
                               "".join (["<li>" + supp_ml + "</li>" for supp_ml in supp_ml_choice]) + \
                           "</ul>"
                def build_shared_emails():
                    shared_emails=req_content['shared_emails']
                    return "<ul>" + \
                               "".join (["<li>" + html.escape(shared_email) + "</li>" for shared_email in shared_emails]) + \
                           "</ul>"
                result = "<dl>" + \
                             (_build_dtdd("Supplementart mailing lists",build_supp_mls(),False) if "supp_ml_choice" in req_content else "") + \
                             (_build_dtdd("Shared emails",build_shared_emails(),False) if "shared_emails" in req_content else "") + \
                        "</dl>"
                return result
            def render_f_spec_software():
                    s_prnts = req_content['spec_software_items']
                    result = "<ul>" + \
                                "".join (["<li>" + html.escape(sp) + "</li>" for sp in s_prnts]) + \
                            "</ul>"    
                    return result
            sections = [
                {
                    "header": "Employee HR Info",
                    "render_f": render_f_employee_info
                },
                {
                    "header": "Employee Position Info",
                    "render_f": render_f_position_info
                },
                {
                    "header": "Employee Work-Model and Location Info",
                    "render_f": render_f_work_model
                }, 
                {
                    "header": "Employee Hardware Requirements",
                    "render_f": render_f_hardware_info
                },
                {
                    "header": "Employee Phone requirements",
                    "render_f": render_f_phone_info,
                },

                {
                    "header": "Supplementary Printers",
                    "render_f": render_f_supplementary_prnts,
                    "condition": "supp_print_choice" in req_content
                },
                {
                    "header": "File Share Locations",
                    "render_f": render_f_file_shares,
                    "condition": "selected_file_shares" in req_content
                },
                {
                    "header": "Supplementary Mailing Lists and Shared Emails",
                    "render_f": render_f_supplementary_mls,
                    "condition": "supp_ml_choice" in req_content or "shared_emails" in req_content
                },
                {
                    "header": "Specialised supplentary software",
                    "render_f": render_f_spec_software,
                    "condition": "spec_software_items" in req_content
                }







            ]
            result = "<br/>".join([("<h4>" + section["header"] +"</h4>" + section["render_f"]() if section.get("condition",True) else "") for section in sections ])
            return result
        super().__init__("onboarding",get_subject,get_ticket_content,config_data)




