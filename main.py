import powershellRunner
import csvAnalyzer
import Tester
import GeoLogonalyzer

# username = "eyal@delisos.onmicrosoft.com"
# password = "poolwhite1#"
#
# print("Analyzing Process stage 1: Connecting to Office365 Api ")
# powershellRunner.t1(username,password)
# print("Analyzing Process stage 2: Extracts IP addresses ")
# csvAnalyzer.analyzer()
# print("Analyzing Process stage 3: Ip Analyzing -  Finding Ips GeoLocation etc")
# Tester.ipAnalyzer()
# print("Analyzing Process stage 4: Ip Analyzing -  Checking all the Outlooks Accounts - Extracting rules ")
# powershellRunner.t2(username,password)
# print("Done")

username = "eyal@delisos.onmicrosoft.com"
password = "poolwhite1#"

print("Analyzing Process stage 1: Connecting to Office365 Api                       [START]")
powershellRunner.t1(username,password)
print("Analyzing Process stage 1                                             [OK - NO ERROR]")
print("Analyzing Process stage 2: Extracts IP addresses                              [START]")
csvAnalyzer.analyzer()
print("Analyzing Process stage 2:                                            [OK - NO ERROR]")
print("Analyzing Process stage 3: Ip Analyzing -  Finding Ips GeoLocation etc        [START]")
Tester.ipAnalyzer()
print("Analyzing Process stage 3                                             [OK - NO ERROR]")
print("Analyzing Process stage 4: Ip Analyzing -  Extracting rules                   [START]")
powershellRunner.t2(username,password)
print("Analyzing Process stage 4:                                            [OK - NO ERROR]")
print("Analyzing Process stage 5: Logon Analyzing                                    [START]")
GeoLogonalyzer.geoLogonAnalyer()
powershellRunner.t3()
print("Analyzing Process stage 5:                                            [OK - NO ERROR]")
print("                                  [Done]                                             ")