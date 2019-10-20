import csv
import os
#import pandas as pd 
path = "/Users/pony/NASA/dataset_MERRA2/"
files= os.listdir(path)
#out = "/Users/pony/NASA/passData/"+city+"_MERRA2.csv"
#outfile = open( out,'w')
#Table = []
for file in files:
    out = open( ("/Users/pony/NASA/dataset_MERRA2_average"+file),'w')
    p = path + file
    fp = open( p, 'r' )
#print(fp)
    a = 1
    dict = { 'Date': "", 'Average':0.0 }
    average = 0
    Table = []
    for line in fp.readlines():
        UTC_DATE =  line.split(',')[2]
        average = float(line.split(',')[1]) 
        if a == 1:
            dict['Date'] = UTC_DATE
            dict['Average'] = format(average,'.2f')
        else:
            update = float(dict['Average']) + average
            dict['Average'] = format(update,'.2f')

        a = a+1
        if a > 24:
            Table.append( dict ) 
            a = 1
            dict['Average'] = format( float(dict['Average'])/24 , '.2f')
            dict = { 'Date': "", 'Average':0.0 }
     
    num = len(Table)
    out.write( "Date, AVERAGE_FORDAY" )
    for l in range(num):
        out.write( str(Table[l]['Date'])+","+str(Table[l]['Average']) + "\n" )
        #print(Table[l]['data'])
     
    print( "Finish !!")

#print(Table)
#print(Table[0]['data'])
#outfile.write( "YY-MM-DD, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5\n")
#for l in range(num):
#   outfile.write( str(Table[l]['Date'])+"," )
#   for r in range( len( Table[l]['data'] ) ):
#       if r == (len( Table[l]['data'] ) -1 ):
#           outfile.write( str(Table[l]['data'][r] ) + "\n" )
#       else:
#           outfile.write( str(Table[l]['data'][r] )+"," )

# print(Table[l]['data'])
#print( Table[l]['Date'] + "\t" + Table[l]['data'] + "\n" )

#print(Table)

