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

import json
import riak_util
from http_client import HttpClient
import urllib
import base64


def create_option_parser():
    parser = riak_util.create_option_parser()
    parser.add_option(
        "--values",
        dest="values",
        help="list values",
        action="store_true"
    )
    parser.add_option(
        "--b64",
        dest="b64",
        help="print base64-encoded value",
        action="store_true",
        default=False
    )
    return parser


def get_value(host, port, bucket_type, bucket_name, key):
    #quoted_key = urllib.quote(key.encode('utf8'), safe="")
    context = "/types/{}/buckets/{}/keys/{}".format(
        HttpClient.escape_slash(bucket_type), HttpClient.escape_slash(bucket_name), HttpClient.escape_slash(key)
    )
    riak_util.log("Context: {}".format(context))
    client = HttpClient(host, port)
    return client.get(context)['body']


def main(argv):
    parser = create_option_parser()
    (options, args) = parser.parse_args()
    # hash of hashes of keylists
    model = riak_util.build_bucket_type_model(
        options.host, options.port,
        options.bucket_type,
        options.bucket_name,
        options.key
    )
    for bucket_type, bucket in model.items():
        for bucket_name, keys in bucket.items():
            for key in keys:
                if options.values:
                    value = get_value(
                        options.host, options.port, bucket_type, bucket_name, key
                    )
                    if options.b64:
                        value = "{}".format(base64.b64encode(value).decode())
                    print("{}, {}, {} {}".format(
                        bucket_type, bucket_name, key, value)
                    )
                else:
                    print("{}, {}, {}".format(bucket_type, bucket_name, key))

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
