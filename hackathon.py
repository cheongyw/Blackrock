from bs4 import BeautifulSoup
import urllib2
import json

perf_file = urllib2.urlopen("https://www.blackrock.com/tools/hackathon/performance?&identifiers=ticker%3AIVV&graph=resultMap.RETURNS.latestPerf")
data = json.loads(perf_file.read())
perf_file.close()

from pprint import pprint

pprint(data["resultMap"]["RETURNS"][0]["latestPerf"]["sixMonth"])
