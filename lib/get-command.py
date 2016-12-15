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
import riak_util


def main(argv) :
    parser = riak_util.create_option_parser()
    (options, args) = parser.parse_args()
    try:
        if not options.bucket_type:
            parser.print_help()
            return 1
        if not options.bucket_name:
            parser.print_help()
            return 1
        if not options.key:
            parser.print_help()
            return 1
        connection = riak_util.Connection(
            options.host, options.port
        )
        context = "/types/{}/buckets/{}/keys/{}/".format(
            options.bucket_type, options.bucket_name, options.key
        )
        print(connection.get(context))
        return 0
    except Exception as e:
        print("An error occurred creating {{{{{}, {}}}, {}}}: {}".format(
            options.bucket_type, options.bucket_name, options.key, e
        ))
        #import traceback
        #traceback.print_exc()
        return -1

if __name__ == "__main__" :
    import sys
    sys.exit(main(sys.argv))

