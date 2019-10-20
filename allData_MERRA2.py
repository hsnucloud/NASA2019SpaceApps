import csv
import os
#import pandas as pd 

box = "/Users/pony/NASA/MERRA2"
files= os.listdir(path)

    
#out = "/Users/pony/NASA/passData/"+city+"_MERRA2.csv"
#outfile = open( out,'w')
Table = []
for file in files:
    with open( file , newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        dict = {"Station":"", "UTC_DATE":"", "BCSMASS":""}
        for row in rows:
            if dict["Station"] == "":
                dict["Station"] = row['Station']
            
            if dict["UTC_DATE"] == "":
                dict["UTC_DATE"] = row['UTC_DATE']

            if dict["BCSMASS"] == "":
                dict["BCSMASS"] = row['BCSMASS']

            if dict["Station"] == row['Station'] and dict["UTC_DATE"] == row['UTC_DATE']:
                
                
            
        
        p = path + "/"+ file
#        print(p)
        fp = open( p, 'r' )
        a = 0 
        dict = { 'Date': "", 'data' : [] }
        line = fp.readline()
        for line in fp.readlines():
            UTC_DATE =  line.split(',')[23]
            UTC_TIME =  line.split(',')[24]
            DUSMASS25 = line.split(',')[17]
            SSSMASS25 = line.split(',')[21]
            total = float(DUSMASS25)+ float(SSSMASS25)
            if a == 0:
                dict['Date'] = UTC_DATE
                dict['data'].append(format(total,'.2f'))
            else:
                dict['data'].append(format(total,'.2f'))
            a = a+1
            # print( line)i
        Table.append( dict ) 
        
        print( "Finish !!")

num = len(Table)
#print(Table[0]['data'])
outfile.write( "YY-MM-DD, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5\n")
for l in range(num):
    outfile.write( str(Table[l]['Date'])+"," )
    for r in range( len( Table[l]['data'] ) ):
        if r == (len( Table[l]['data'] ) -1 ):
            outfile.write( str(Table[l]['data'][r] ) + "\n" )
        else:
            outfile.write( str(Table[l]['data'][r] )+"," )

# print(Table[l]['data'])
#print( Table[l]['Date'] + "\t" + Table[l]['data'] + "\n" )

#print(Table)

