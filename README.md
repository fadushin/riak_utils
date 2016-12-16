# riak_utils

## `riak-util`

The `riak-util` command provides a command-liney way to riak.

The `riak-util` command is in the `bin` directory:

    prompt$ bin/riak-util 
    Syntax: bin/riak-util <cmd> [--help] <args>
    Commands: 
	
    delete get list put

All commands support `--help`

    prompt$ bin/riak-util get --help
    Usage: get-command.py [options]
    
    Options:
      -h, --help            show this help message and exit
      --host=HOST           Riak host (localhost)
      --port=PORT           Riak port (8098)
      -t BUCKET_TYPE, --bucket_type=BUCKET_TYPE
                            Riak Bucket Type
      -n BUCKET_NAME, --bucket_name=BUCKET_NAME
                            Riak Bucket Name
      -k KEY, --key=KEY     Riak Key
      --r=R                 r value (default: quorum)
      --pr=PR               pr value (default: 0)
      --notfound_ok=NOTFOUND_OK
                            notfound_ok value (default: true)
      --verbose             Print the results verbosely

### Examples

> Note: The `-t` (or `--bucket_type`) flag requires an existing and activated bucket type, e.g., via `riak-admin`:

    prompt$ riak-admin bucket-type create test
    prompt$ riak-admin bucket-type activate test

Create an object against a rel running on localhost:

    prompt$ bin/riak-util put -t test -n test -k test -v test

Get the value back:

    prompt$ bin/riak-util get -t test -n test -k test
    b'test'

Get a verbose listing of the contents:

    prompt$ bin/riak-util get -t test -n test -k test --verbose
    Status: 200
    Headers:
        Last-Modified: Fri, 16 Dec 2016 20:48:29 GMT
        Link: </buckets/test>; rel="up"
        Vary: Accept-Encoding
        ETag: "21TvE2scPWup8VvNCHXv1V"
        Server: MochiWeb/1.1 WebMachine/1.10.9 (cafe not found)
        Content-Length: 4
        X-Riak-Vclock: a85hYGBgzGDKBVI8R4M2ctum1/UyMHDoZjAlMuaxMsieP3GRLwsA
        Content-Type: text/plain
        Date: Fri, 16 Dec 2016 20:49:43 GMT
    Body: b'test'

Update an object (performs a get before put to get the vclock):

    prompt$ bin/riak-util put -t test -n test -k test -v a-different-value
    prompt$ bin/riak-util get -t test -n test -k test
    b'a-different-value'

Update an object, but generate siblings:

    prompt$ bin/riak-util put -t test -n test -k test -v somethingelse --force
    prompt$ bin/riak-util get -t test -n test -k test --verbose
    Status: 300
    Headers:
        Content-Type: text/plain
        ETag: "6MNV4PgPJy436u0qOkGqbV"
        Server: MochiWeb/1.1 WebMachine/1.10.9 (cafe not found)
        Vary: Accept, Accept-Encoding
        Date: Fri, 16 Dec 2016 20:51:10 GMT
        X-Riak-Vclock: a85hYGBgzGDKBVI8R4M2ctum1/UyMHDoZjAlMuWxMqw6f+IiXxYA
        Last-Modified: Fri, 16 Dec 2016 20:50:50 GMT
        Content-Length: 56
    Body: b'Siblings:\n7BhPkRsuu8YFa3OEg6bPUA\n21TvE2scPWup8VvNCHXv1V\n'

Update again, to resolve siblings:

    prompt$ bin/riak-util put -t test -n test -k test -v athirdthing
    prompt$ bin/riak-util get -t test -n test -k test
    b'athirdthing'

Add another entry under a different bucket

    prompt$ bin/riak-util put -t test -n another-bucket -k another-key -v athing

Or even in the default bucket type (by not specifying one):

    prompt$ bin/riak-util put -n naked-bucket -k some-key -v something

List everything:

    prompt$ bin/riak-util list
    test, test, test
    test, another-bucket, another-key
    default, naked-bucket, some-key

List with values:

    prompt$ bin/riak-util list --values
    test, test, test: "athirdthing"
    test, another-bucket, another-key: "athing"
    default, naked-bucket, some-key: "something"

List all keys under a bucket type, or bucket:

    prompt$ bin/riak-util list -t test --values
    test, another-bucket, another-key: "athing"
    test, test, test: "athirdthing"
    prompt$ bin/riak-util list -t test -n another-bucket --values
    test, another-bucket, another-key: "athing"

Delete all keys in a bucket

    prompt$ bin/riak-util delete -t test -n another-bucket
    deleted test another-bucket another-key
    prompt$ bin/riak-util list -t test -n another-bucket
    prompt$ 

Delete all buckets of a given bucket type:

    prompt$ bin/riak-util delete -t test
    deleted test test test

Delete all keys in all buckets of all bucket types:

    prompt$ bin/riak-util delete
    deleted default naked-bucket some-key
