# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import subprocess

from django.conf import settings


# XXX: Workaround fix threading bug without modifying python core source
# https://stackoverflow.com/questions/13193278/understand-python-threading-bug
import threading
threading._DummyThread._Thread__stop = lambda x: 42


APP_DIR = os.path.abspath(os.path.dirname(__file__))
TOOLS_DIR = os.path.join(APP_DIR, 'tools')

logger = logging.getLogger(__name__)

def runner(cmd):
    retcode = None
    outputs = None
    if isinstance(cmd, list):
        shell = False
    else:
        shell = True
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE
    try:
        p = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, shell=shell)
        outputs, errors = p.communicate()
        retcode = p.returncode
        if retcode != 0:
            logger.error('cmd: %s' % cmd)
            logger.error('retcode: %s' % retcode)
            logger.error('errors: %s' % errors)
    except (OSError, e):
        logger.error('Cannot run command: %s' % cmd)
    return (retcode, outputs)

def get_goaccess_html():
    logger.debug(settings.APACHE_LOG)
    html = ''
    cmd = (
            'zcat -f %(apache_log)s '
#            'zcat -f %(apache_log)s %(apache_log)s*.gz '
            '| %(goaccess)s --config-file=%(goaccess_conf)s - '
    ) % {
            'apache_log': settings.APACHE_LOG,
            'goaccess': os.path.join(TOOLS_DIR, 'goaccess'),
            'goaccess_conf': os.path.join(TOOLS_DIR, 'goaccess.conf'),
    }
    logger.debug(cmd)
    ret, outs = runner(cmd)
    if ret == 0:
        html = outs
    else:
        logger.error('failed to generate GoAccess report page.')
    return html


