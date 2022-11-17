from urllib import request
r = request.Request('http://publications.europa.eu/resource/dataset/planned-availability')
resp = request.urlopen(r)
resp.readlines()
resp.fp.read(100)
