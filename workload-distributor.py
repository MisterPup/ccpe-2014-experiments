# Copyright 2012 Anton Beloglazov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
logging.basicConfig(
    filename='/home/ubuntu/git/ccpe-2014-experiments/workload-distributor.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG)

import sys
import os
import bottle


def is_distribution_enabled():
    enabled = False
    with open('workload-distributor.conf', 'r') as f:
        enabled = bool(int(f.read()))
        logging.info('Workload distribution enabled: ' +
                     str(enabled))
    return enabled


@bottle.get('/')
def poll():
    logging.info('Received a request from %s', bottle.request.remote_addr)
    try:
        if is_distribution_enabled():
            exec_path = '/usr/bin/python2 /home/ubuntu/git/cpu-load-generator/cpu-load-generator.py'
            trace_path = '/home/ubuntu/git/ccpe-2014-experiments/{0}/{1}'.format(dir, files.pop())

            command = (exec_path + ' -n ' + str(ncpus) + ' -m' + str(mem_util) + ' ' +
                                    str(interval) + ' ' + trace_path)
            logging.info('Returning: %s', command)
            return command
    except:
        logging.exception('Exception during request processing:')
        raise

if len(sys.argv) < 2:
    print 'You must specify an argument: a directory containing workload trace files'
    sys.exit(1)

dir = sys.argv[1]
ncpus = sys.argv[2] if len(sys.argv) > 2 else 0 #autodetect
interval = sys.argv[3] if len(sys.argv) > 3 else 300
mem_util = sys.argv[4] if len(sys.argv) > 4 else 0

files = os.listdir(dir)

logging.info('Starting listening on localhost:8081')
bottle.debug(True)
bottle.run(host='controller', port=8081)
