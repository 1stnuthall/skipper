'''
OSM Cache Handler.
'''
import os, json, time

from collections import namedtuple
from types import SimpleNamespace

cache = "__osm__"
if not os.path.isdir(cache):
    os.mkdir(cache)

def write_cache(object, content):
    path = "/".join([cache, f"{object}.json"])
    with open(path, "w") as cachefile:
        cachefile.write(json.dumps(content))
    
def cache_decoder(input):
    return namedtuple('X', input.keys())(*input.values())

def get_cache(object):
    path = "/".join([cache, f"{object}.json"])
    if os.path.exists(path):
        mod = os.stat(path).st_mtime
        if mod <= time.time() + 1:
            return json.load(open(path,"r"))
        else:
            os.remmove(path)
            return False
