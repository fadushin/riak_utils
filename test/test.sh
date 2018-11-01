#!/bin/bash -e
#
# Copyright (c) dushin.net
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of dushin.net nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY dushin.net ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL dushin.net BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

##
## Syntax:
##  test.sh
##
## Optional environment variables:
##
##  RIAK_HOST       Riak host (default: localhost)
##  RIAk_PORT       Riak port (default: 8098)
##
## Example: 
##
## shell$ RIAK_PORT=10018 test.sh
## .....Tests passed.
##

: ${RIAK_HOST:="localhost"}
: ${RIAK_PORT:="8098"}

ROOT_DIR=$(cd $(dirname $0)/.. && pwd)


function assert_equal {
    if [ "${1}" != "${2}" ]; then
        echo "!! ERROR: Expected '${1}' to equal '${2}'"
        exit -1
    fi
}

${ROOT_DIR}/bin/riak-util delete --host=${RIAK_HOST} --port ${RIAK_PORT} -n foo -k bar
assert_equal "$(${ROOT_DIR}/bin/riak-util get --host=${RIAK_HOST} --port ${RIAK_PORT} -n foo -k bar)" "not found"
echo -n "."

${ROOT_DIR}/bin/riak-util put --host=${RIAK_HOST} --port ${RIAK_PORT} -n foo -k bar -v tapas
assert_equal "$(${ROOT_DIR}/bin/riak-util get --host=${RIAK_HOST} --port ${RIAK_PORT} -n foo -k bar)" "tapas"
echo -n "."

${ROOT_DIR}/bin/riak-util put --host=${RIAK_HOST} --port ${RIAK_PORT} -n foo -k bar -v "wiskey"
assert_equal "$(${ROOT_DIR}/bin/riak-util get --host=${RIAK_HOST} --port ${RIAK_PORT} -n foo -k bar)" "wiskey"
echo -n "."

${ROOT_DIR}/bin/riak-util put --host=${RIAK_HOST} --port ${RIAK_PORT} -n foo -k bar -v "hash" -f
assert_equal "$(${ROOT_DIR}/bin/riak-util get --host=${RIAK_HOST} --port ${RIAK_PORT} -n foo -k bar)" "hash"
echo -n "."


## TODO list

${ROOT_DIR}/bin/riak-util delete --host=${RIAK_HOST} --port ${RIAK_PORT} -n foo -k bar
assert_equal "$(${ROOT_DIR}/bin/riak-util get --host=${RIAK_HOST} --port ${RIAK_PORT} -n foo -k bar)" "not found"
echo -n "."

echo "Tests passed."
exit 0