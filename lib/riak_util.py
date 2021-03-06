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

from http_client import HttpClient
import subprocess
import json
import base64

def get_bucket_types():
    ret = []
    lines = invoke("riak-admin bucket-type list").decode()
    for line in lines.split("\n"):
        if line.strip() != "":
            fields = line.split(" ")
            ret.append(fields[0])
    return ret


def get_bucket_names(host, port, bucket_type):
    context = "/types/{}/buckets?buckets=true".format(bucket_type)
    client = HttpClient(host, port)
    try :
        data = json.loads(client.get(context)['body'].decode())
    except Exception as e :
        print("An error ocurred decoding JSON payload from request for bucket names.  Error: {}; body: {}".format(e, client.get(context)['body']))
    #print("data: {}".format(data))
    return data['buckets']


def get_keys(host, port, bucket):
    bucket_type, bucket_name = bucket
    context = "/types/{}/buckets/{}/keys?keys=true".format(HttpClient.escape_slash(bucket_type), HttpClient.escape_slash(bucket_name))
    client = HttpClient(host, port)
    body = client.get(context)['body']
    log("Context: {} BODY: {}".format(context, body))
    data = json.loads(body.decode())
    return data['keys']


def build_key_model(host, port, bucket_type, bucket_name, key=None):
    if key is None:
        return get_keys(host, port, (bucket_type, bucket_name))
    else:
        return [key]


def build_bucket_model(host, port, bucket_type, bucket_name=None, key=None):
    ret = {}
    if bucket_name is None:
        bucket_names = get_bucket_names(host, port, bucket_type)
        log("bucket_names: {}".format(bucket_names))
        for _bucket_name in bucket_names:
            ret[_bucket_name] = build_key_model(host, port, bucket_type, _bucket_name, key)
    else:
        ret[bucket_name] = build_key_model(host, port, bucket_type, bucket_name, key)
    return ret


def build_bucket_type_model(host, port, bucket_type=None, bucket_name=None, key=None):
    ret = {}
    if bucket_type is None:
        bucket_types = get_bucket_types()
        log("bucket_types: {}".format(bucket_types))
        for type_ in bucket_types:
            ret[type_] = build_bucket_model(host, port, type_, bucket_name, key)
    else:
        ret[bucket_type] = build_bucket_model(host, port, bucket_type, bucket_name, key)
    return ret


def create_option_parser():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option(
        "--host",
        dest="host",
        help="Riak host (localhost)",
        type="string",
        default="localhost"
    )
    parser.add_option(
        "--port",
        dest="port",
        help="Riak port (8098)",
        type="int",
        default=8098
    )
    parser.add_option(
        "--bucket_type", "-t",
        dest="bucket_type",
        help="Riak Bucket Type",
    )
    parser.add_option(
        "--bucket_name",  "-n",
        dest="bucket_name",
        help="Riak Bucket Name",
    )
    parser.add_option(
        "--key", "-k",
        dest="key",
        help="Riak Key",
    )
    return parser


def invoke(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    (stdout, stderr) = proc.communicate()
    if proc.returncode != 0:
        raise Exception(
            "An error occurred executing command '%s'.  Return code: %s.  stdout: '%s'.  stderr: '%s'" %
            (command, proc.returncode, stdout, stderr)
        )
    return stdout

def log(message):
    #print("LOG> {}".format(message))
    pass