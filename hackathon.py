from bs4 import BeautifulSoup
import urllib
import json

perf_file = urllib.request.urlopen("https://www.blackrock.com/tools/hackathon/performance?&identifiers=ticker%3AIVV&graph=resultMap.RETURNS.latestPerf")
data = json.loads(perf_file.read().decode('utf-8'))
perf_file.close()

from pprint import pprint

return str(data["resultMap"]["RETURNS"][0]["latestPerf"]["sixMonth"])
