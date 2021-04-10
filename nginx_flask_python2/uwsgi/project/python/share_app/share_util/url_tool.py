import urllib,urllib2,urlparse

def get(url,query):
	"access by GET"
	req = urllib2.Request(url+'?'+urllib.urlencode(query))
	return urllib2.urlopen(req).read()

def post(url,data):
	"access by POST"
	req = urllib2.Request(url, urllib.urlencode(data))
	return urllib2.urlopen(req).read()

def make(url_o,pathname):
	"make url from a url_o based on pathname"
	return urlparse.urlunparse((url_o['scheme'],url_o['domain'],\
		url_o['path'][pathname],'','',''))
