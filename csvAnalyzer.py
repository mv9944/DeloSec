import csv
import json

def analyzer():
    csvData = [['IpClinet', 'ActorIpAddress','ResultStatus','CreationTime']]

    with open(r'C:\Users\nmega\PycharmProjects\untitled\realTimeResults\AuditRecords.csv') as csvfile:
        ff = reader = csv.DictReader(csvfile)
        for row in ff:
            try:
                temp = row['AuditData']
                jsonString = json.loads(temp)
                IpClinet = jsonString.get('ClientIP')
                ActorIpAddress = jsonString.get('ActorIpAddress')
                ResultStatus = jsonString.get('ResultStatus')
                CreationTime = jsonString.get('CreationTime')
                #print (IpClinet,ActorIpAddress,ResultStatus,CreationTime)
                appendix = [IpClinet,ActorIpAddress,ResultStatus,CreationTime]
                csvData.append(appendix)
            except Exception as e:
                print(e)
                continue

    with open(r'C:\Users\nmega\PycharmProjects\untitled\realTimeResults\FirstResults.csv', 'w',newline='',encoding='utf-8') as csvFile:
        try:
         writer = csv.writer(csvFile)
         writer.writerows(csvData)
        except:
         print("error in", csvData)
    csvFile.close()






