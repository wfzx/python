#!/usr/bin/env python

import logging

def log(info):
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='logs/release.log',
                    filemode='a')
    logging.info(info)

if __name__ == "__main__":
    log('This is a write test line')