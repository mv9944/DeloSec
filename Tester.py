import csv
from geolite2 import geolite2
from ipwhois.net import Net
from ipwhois.asn import IPASN

def ipAnalyzer():
    csvData = [['Ip', 'Country_code', 'Country', 'City', 'Time_zone', 'Longitude', 'Latitude','asn','asn_description']]


    # with open('FinalResults.csv', 'w') as csvFile:
    #     writer = csv.writer(csvFile)
    #     writer.writerows(csvData)
    # csvFile.close()

    with open(r'C:\Users\nmega\PycharmProjects\untitled\realTimeResults\FirstResults.csv') as csvfile:

        ff = reader = csv.DictReader(csvfile)
        for row in ff:
            try:
             ip = row['IpClinet']
             net = Net(ip)
             obj = IPASN(net)
             results = obj.lookup()
             reader = geolite2.reader()
             temp = reader.get(ip)
             #print(temp)
             country = temp.get('registered_country').get('names').get('en')
             country_iso_code = temp.get('registered_country').get('iso_code')
             city = temp.get('city').get('names').get('en')
             time_zone = temp.get('location').get('time_zone')
             lon = temp.get('location').get('longitude')
             lat = temp.get('location').get('latitude')
             asn = results.get('asn')
             asn_description = results.get('asn_description')
             appendix = [ip,country_iso_code,country,city,time_zone,lon,lat,asn,asn_description]
             #print(appendix)
             #print(ip," ",country_iso_code," ",country," ",city," ",time_zone," ",lon," ",lat)
             csvData.append(appendix)
            except Exception as e:
                try:
                 country = temp.get('country').get('names').get('en')
                 country_iso_code = temp.get('country').get('iso_code')
                 city = 'No Data'
                 time_zone = 'No Data'
                 lon = temp.get('location').get('longitude')
                 lat = temp.get('location').get('latitude')
                 appendix = [ip,country_iso_code,country,city,time_zone,lon,lat,asn,asn_description]
                 csvData.append(appendix)
                except:
                 continue
            continue
    #print(appendix[0])

    with open(r'C:\Users\nmega\PycharmProjects\untitled\realTimeResults\FinalResults.csv', 'w',newline='',encoding='utf-8') as csvFile:
        try:
         writer = csv.writer(csvFile)
         writer.writerows(csvData)
        except:
         print("error in", csvData)

    csvFile.close()
