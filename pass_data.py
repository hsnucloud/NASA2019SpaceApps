import csv
import sys
#import pandas as pd 

path = "/Users/pony/NASA/passData"
fileName = path + "/2018_pass_WestLosAngeles_LosAngeles.csv"
outfile = open( fileName, "w")
outfile.write( "Date\tTime(UT)\tCo\tno2\to3\tpm10\tpm25\n")
r = "/Users/pony/NASA/rawData_WestLosAngeles/2018_WestLosAngeles_LosAngeles.csv"
with open( r , newline='') as csvfile:
    rows = csv.DictReader(csvfile)
    dic = {"Date":"", "Time(UT)":"", "Co":"", "no2":"", "o3":"", "pm10":"", "pm25":""}
    
    n = 0
    for row in rows:
        if n == 0:
# print(row)
            date = row['date'].split("=")[1].split(',')[0]
            Date = date.split('T')[0]
            Time = date.split('T')[1]
            dic['Date'] = Date
            dic['Time(UT)'] = Time.split('Z')[0]
         
            parameter = row['parameter']
            value = row['value']
            unit = row['unit']
            if parameter == "co":
                dic['Co'] = str(value)
            elif parameter == "no2":
                dic['no2'] = str(value)
            elif parameter == "o3":
                dic['o3'] = str(value)
            elif parameter == "pm10":
                dic['pm10'] = str(value)
            elif parameter == "pm25":
                dic['pm25'] = str(value)
            n = n+1
        else:
            parameter = row['parameter']
            value = row['value']
            unit = row['unit']
            if parameter == "co":
                dic['Co'] = str(value)
            elif parameter == "no2":
                dic['no2'] = str(value)
            elif parameter == "o3":
                dic['o3'] = str(value)
            elif parameter == "pm10":
                dic['pm10'] = str(value)
            elif parameter == "pm25":
                dic['pm25'] = str(value)
            n = n+1

        if n > 4:
            n = 0
#            print( dic )
#dic = {"Date":"", "Time(UT)":"", "Co":"", "no2":"", "o3":"", "pm10":"", "pm25":""}
            outfile.write( dic['Date']+"\t"+dic['Time(UT)']+"\t"+dic['Co']+"\t"+dic['no2']+"\t"+dic['o3']+"\t"+dic['pm10']+"\t"+dic['pm25']+"\n")
#           print( dic['Date']+"\t"+dic['Time(UT)']+"\t"+dic['Co']+"\t"+dic['no2']+"\t"+dic['o3']+"\t"+dic['pm10']+"\t"+dic['pm25'])
            


outfile.close()
            
#print(Date)
#       print(time)
        

#print(row['date'], row['parameter'], row['value'], row['unit'] )

