#!/usr/bin/env python
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

from optparse import OptionParser
import json
import riak_utils

optparser = OptionParser()
optparser.add_option(
    "--bucket_type", 
    dest="bucket_type",
    help="Riak Bucket Type", 
    metavar="BUCKET_TYPE",
)
optparser.add_option(
    "--bucket_name", 
    dest="bucket_name",
    help="Riak Bucket Name", 
    metavar="BUCKET_NAME",
)
optparser.add_option(
    "--key", 
    dest="key",
    help="Riak Key", 
    metavar="Key",
)
optparser.add_option(
    "--host", 
    dest="host",
    help="Riak host", 
    metavar="HOST",
    type="string",
    default="localhost"
)
optparser.add_option(
    "--port", 
    dest="port",
    help="Riak endpoint port", 
    metavar="PORT",
    type="int",
    default=8098
)


def main(argv) :
    (options, args) = optparser.parse_args()
    
    connection = riak_utils.Connection(
        host, port, "/types/%s/buckets/%s/keys/%s/" 
        % (options.bucket_type, options.bucket_name, options.key)
    )
    print connection.get()
    return 0

if __name__ == "__main__" :
    import sys
    sys.exit(main(sys.argv))

