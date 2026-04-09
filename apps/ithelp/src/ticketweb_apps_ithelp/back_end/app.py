import falcon

from .handlers import SubmitTicketOnboarding



from .handlers import BadRequest
from .config_data import config_data




def main():
   api = falcon.App()
   api.add_route('/submit-ticket/onboarding', SubmitTicketOnboarding())
   api.add_error_handler(BadRequest) 
   return api
