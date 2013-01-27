import logging
import sys
#~ http://docs.python.org/3/howto/logging.html#logging-basic-tutorial

logger  	= logging.getLogger('OUR EPIC LOGGING')
hdlr		= logging.StreamHandler(sys.stdout)
formatter	= logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
# logger.setLevel(logging.ERROR)
