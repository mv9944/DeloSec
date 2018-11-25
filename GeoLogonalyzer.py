import csv
import json

def geoLogonAnalyer():
    csvData = [['creationTime','user','ip']]

    with open(r'C:\Users\nmega\PycharmProjects\untitled\realTimeResults\AuditRecords.csv') as csvfile:
        ff = reader = csv.DictReader(csvfile)
        for row in ff:
            try:
                temp = row['AuditData']
                jsonString = json.loads(temp)
                ip = jsonString.get('ClientIP')
                creationTime = str(jsonString.get('CreationTime')).replace("T"," ")
                user = jsonString.get('UserId')
               # print ("->" ,creationTime,user,ip)
                appendix = [creationTime,user,ip]
                csvData.append(appendix)
            except Exception as e:
                print(e)
                continue

    with open(r'C:\Users\nmega\PycharmProjects\untitled\realTimeResults\GeoLogonFirstResults.csv', 'w',newline='',encoding='utf-8') as csvFile:
        try:
         writer = csv.writer(csvFile)
         writer.writerows(csvData)
        except:
         print("error in", csvData)
    csvFile.close()






