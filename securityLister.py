import csv
with open('security-universe_20171014.csv', newline='') as csvfile:
	securityList = csv.reader(csvfile, delimiter=',',quotechar='|')
	for row in securityList:
		
