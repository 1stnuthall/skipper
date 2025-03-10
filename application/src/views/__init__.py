from .blocks import *
from config import app, logging

logging.basicConfig(level=logging.DEBUG)

###########################################################
## Middleware Declaration - it's there because it's there
###########################################################
@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logging.debug(body)
    return next()