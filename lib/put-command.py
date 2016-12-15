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
        "--content_type",
        dest="content_type",
        help="Riak value content type (text/plain)",
        default="text/plain",
    )
    parser.add_option(
        "--value", "-v",
        dest="value",
        help="value to put in Riak object",
    )
    parser.add_option(
        "--file",
        dest="file",
        help="value to put in Riak object, from file",
    )
    parser.add_option(
        "--force", "-f",
        dest="force",
        action="store_true",
        help="Do not read before write to resolve vclocks, if the object already exists",
    )
    parser.add_option(
        "--w",
        dest="w",
        help="w value (default: quorum)",
    )
    parser.add_option(
        "--pw",
        dest="pw",
        help="pw value (default: 0)",
    )
    parser.add_option(
        "--dw",
        dest="dw",
        help="dw value (default: quorum)",
    )
    parser.add_option(
        "--returnbody",
        dest="returnbody",
        action="store_true",
        help="return the body in the response",
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
    if options.w:
        ret['w'] = options.w
    if options.pw:
        ret['pw'] = options.pw
    if options.dw:
        ret['dw'] = options.dw
    if options.returnbody:
        ret['returnbody'] = "true"
    return ret


def main(argv) :
    parser = create_option_parser()
    (options, args) = parser.parse_args()
    try:
        (options, args) = parser.parse_args()
        if not options.bucket_type:
            parser.print_help()
            return 1
        if not options.bucket_name:
            parser.print_help()
            return 1
        if not options.key:
            parser.print_help()
            return 1
        if not options.value and not options.file:
            parser.print_help()
            return 1
        params = get_params(options)
        connection = riak_util.Connection(
            options.host, options.port
        )
        context = "/types/{}/buckets/{}/keys/{}/".format(
            options.bucket_type, options.bucket_name, options.key
        )
        vclock = None
        if not options.force:
            result = connection.get(context)
            if result['status'] != 404:
                vclock = result['headers']['X-Riak-Vclock']
        body = riak_util.read_file(options.file) if options.file else options.value
        headers = {'X-Riak-Vclock': vclock} if vclock else {}
        response = connection.put(context, body=body, content_type=options.content_type, headers=headers, params=params)
        riak_util.pretty_print_response(response, options.verbose)
        return 0
    except Exception as e:
        print("An error occurred creating {{{{{}, {}}}, {}}}: {}".format(
            options.bucket_type, options.bucket_name, options.key, e
        ))
        import traceback
        traceback.print_exc()
        return -1

if __name__ == "__main__" :
    import sys
    sys.exit(main(sys.argv))

