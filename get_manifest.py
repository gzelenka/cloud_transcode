#!/usr/bin/env python
import os
import os.path
import pyrax
import pyrax.exceptions
import sys

from optparse import OptionParser


pyrax.set_setting("identity_type", "rackspace")
pyrax.set_setting("region", "IAD")
pyrax.set_credential_file("rack_auth")
cf = pyrax.cloudfiles

WORKING_DIR = "/tmp"


def getopts():
    parser = OptionParser()
    parser.add_option("-n", "--name", action='store', dest='name',
                      help='name of the conatainer')
    parser.add_option("-d", "--directory", action='store_true', dest="dir",
                      default=False, help="If target is a directory")
    return parser.parse_args()


def get_files_to_transcode():
    try:
        cont = cf.create_container("NeedTranscode")
    except pyrax.exceptions.NoSuchContainer:
        print "Cannot find need to transcode container, bailing..."
        sys.exit(1)

    manifest = {}
    for o in cont.get_object_names():
        obj = cont.get_object(o)
        print "Getting %s size %d" % (o, obj.total_bytes)
        m, data = obj.get(include_meta=True, chunk_size=1024*4)
        with open(os.path.join(WORKING_DIR, o), 'w') as f:
            for d in data:
                f.write(d)
        manifest[o] = m['x-object-meta-finished-container-name']

    return manifest


if __name__ == '__main__':
    o, a = getopts()
    print o
    print a

    print get_files_to_transcode()
