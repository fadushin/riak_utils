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


def create_option_parser():
    parser = riak_util.create_option_parser()
    parser.add_option(
        "--r",
        dest="r",
        help="r value (default: quorum)",
    )
    parser.add_option(
        "--pr",
        dest="pr",
        help="pr value (default: 0)",
    )
    parser.add_option(
        "--notfound_ok",
        dest="notfound_ok",
        help="notfound_ok value (default: true)",
    )
    parser.add_option(
        "--b64",
        dest="b64",
        help="print base64-encoded value",
        action="store_true",
        default=False
    )
    parser.add_option(
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Print the results verbosely",
    )
    return parser


def get_params(options):
    ret = {}
    if options.r:
        ret['r'] = options.r
    if options.pr:
        ret['pr'] = options.pr
    if options.notfound_ok:
        ret['notfound_ok'] = "true"
    return ret


def main(argv) :
    parser = create_option_parser()
    (options, args) = parser.parse_args()
    try:
        if not options.bucket_name:
            parser.print_help()
            return 1
        if not options.key:
            parser.print_help()
            return 1
        params = get_params(options)
        connection = riak_util.Connection(
            options.host, options.port
        )
        if options.bucket_type:
            context = "/types/{}/buckets/{}/keys/{}/".format(
                riak_util.escape_slash(options.bucket_type), 
                riak_util.escape_slash(options.bucket_name), 
                riak_util.escape_slash(options.key)
            )
        else:
            context = "/buckets/{}/keys/{}/".format(
                riak_util.escape_slash(options.bucket_name), 
                riak_util.escape_slash(options.key)
            )
        response = connection.get(context, params=params)
        riak_util.pretty_print_response(response, options.verbose, options.b64)
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

