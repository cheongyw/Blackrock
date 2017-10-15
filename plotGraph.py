import pandas as pd
import numpy as np
from ggplot import *

urlAddress = "https://www.blackrock.com/tools/hackathon/performance?&identifiers=ticker:APL&graph=resultMap.RETURNS.latestPerf"
perf_file = urllib.request.urlopen(urlAddress)
data = json.loads(perf_file.read())
perf_file.close()

df = pd.DataFrame({
    "three": data["resultMap"]["RETURNS"][0]["latestPerf"]["threeMonth"],
    "six": data["resultMap"]["RETURNS"][0]["latestPerf"]["sixMonth"],
    "nine": data["resultMap"]["RETURNS"][0]["latestPerf"]["nineMonth"]
})
df = pd.melt(df)

ggplot(aes(x='period', y='performance'), data=df) +\
    geom_histogram()
