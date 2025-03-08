from .api_request import apiRequest
from .modal_open import formOpen
from .modal_update import formUpdate
from .send_message import sendMessage
from .approval_get_id import getInterventionId
from .validate_input import validateInput

from .slash_oncall import *
from .slash_request import *
from .slash_usage import *

from .cache import get_cache, write_cache

from config import *

###########################################################
## Middleware Declaration - it's there because it's there
###########################################################
@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logging.debug(body)
    return next()