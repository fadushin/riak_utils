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
import urllib

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
    "--host", 
    dest="host",
    help="Riak host", 
    metavar="HOST",
    type="string",
    default="localhost"
)
optparser.add_option(
    "--values",
    dest="values",
    help="list values",
    action="store_true"
)
optparser.add_option(
    "--port", 
    dest="port",
    help="Riak endpoint port", 
    metavar="PORT",
    type="int",
    default=8098
)

def get_bucket_types() :
    ret = []
    lines = riak_utils.invoke("riak-admin bucket-type list")
    for line in lines.split("\n") :
        if line.strip() != "" :
            fields = line.split(" ")
            ret.append(fields[0])
    return ret
    
def get_buckets(host, port, bucket_type) :
    ret = []
    connection = riak_utils.Connection(host, port, "/types/%s/buckets?buckets=true" % (bucket_type))
    data = json.loads(connection.get())
    for i in data['buckets'] :
        ret.append((bucket_type, i))
    return ret

def get_keys(host, port, bucket) :
    bucket_type, bucket_name = bucket
    ret = []
    connection = riak_utils.Connection(host, port, "/types/%s/buckets/%s/keys?keys=true" % (bucket_type, bucket_name))
    data = json.loads(connection.get())
    for i in data['keys'] :
        ret.append(i)
    return ret

def get_value(host, port, bucket_type, bucket_name, key) :
    quoted_key = urllib.quote(key.encode('utf8'), safe="")
    connection = riak_utils.Connection(host, port, "/types/%s/buckets/%s/keys/%s" % (bucket_type, bucket_name, quoted_key))
    #print connection.str()
    return connection.get()

def main(argv) :
    (options, args) = optparser.parse_args()
    
    bucket_types = []
    if options.bucket_type == None :
        bucket_types = get_bucket_types()
    else :
        bucket_types = [options.bucket_type]
    #print bucket_types
    
    for bucket_type in bucket_types :
        buckets = []
        if options.bucket_name != None :
            buckets = [(bucket_type, options.bucket_name)]
        else :
            buckets = get_buckets(options.host, options.port, bucket_type)
        #print buckets
        
        for bucket in buckets :
            _type, bucket_name = bucket
            keys = get_keys(options.host, options.port, bucket)
            for key in keys :
                if options.values :
                    print "{{%s}, %s}, \"%s\": %s" % (bucket_type, bucket_name, key, get_value(options.host, options.port, bucket_type, bucket_name, key))
                else :
                    print "{{%s}, %s}, %s" % (bucket_type, bucket_name, key)
                
    
    
    
    return 0

if __name__ == "__main__" :
    import sys
    sys.exit(main(sys.argv))