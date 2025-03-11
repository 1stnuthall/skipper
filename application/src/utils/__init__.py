from .modal_open import formOpen
# from .modal_update import formUpdate
from .send_message import sendMessage
from .validate_input import validateInput
# from .validate_request import view_submission

# from .slash_request import *
# from .slash_usage import *

from .cache import get_cache, write_cache

from config import *

###########################################################
## Middleware Declaration - it's there because it's there
###########################################################
@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logging.debug(body)
    return next()