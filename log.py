# encoding: utf-8
import logging
import os

# logging config

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=os.path.dirname(__file__) + 'myapp.log',
                    filemode='w')

if __name__ == '__main__':
    logging.debug('This is debug message')
    logging.info('This is info message')
    logging.warning('This is warning message')
    logging.error('This is warning message')