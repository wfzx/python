#!/usr/bin/env python

import logging

def log(info,ProjectName="release"):
    logging.basicConfig(level=logging.INFO,
                    format='DevOps Release Logs: %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/data/release/logs/%s.log' % (ProjectName),
                    # filename='logs/%s.log' % (ProjectName),
                    filemode='a')
    logging.info(info)

if __name__ == "__main__":
    log('This is a write test line')