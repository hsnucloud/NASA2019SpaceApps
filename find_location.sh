#!/bin/bash
Data_L="/Users/pony/NASA/LosAngeles.csv"
Data="/Users/pony/NASA/MERRA2"
Location="WestLosAngeles"
grep_L="West Los Angeles"
DataSource="MERRA2"
sortNum="25"
dot=","
'''
for file in `ls $Data/*.csv`
do
    echo $file
    name=`basename $file| cut -d'.' -f1`
    newName=$name"_"$Location"_"$DataSource
    echo $newName 
    out=$Load"/"$newName
    echo $out
    `grep $grep_L $file | sort -n -t$dot -k $sortNum > $out` 
done
'''

Load="/Users/pony/NASA/rawData_WestLosAngeles"
`grep "2018"  $Data_L | grep "West Los Angeles" >  $Load"/2018_"$Location"_LosAngeles.csv"` 

