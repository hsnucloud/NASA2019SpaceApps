#!/bin/bash
box="/Users/pony/NASA/Dataset/"

i=0;
for line in `awk -F"," '{print$1}' "/Users/pony/NASA/MERRA2/20180502.state.slv.aer.csv" | sort -u`
do 
    address[$i]=$line;
#    echo ${address[$i]};
    i=$(( i+1 )); 
    place=$line;
    echo $place
#    `mkdir $box/$place`
    `touch $box$place"_365time.csv"`
#   echo "location, BCSMASS, yymmdd, hr" >> $box$place".csv"
done 
#echo ${address[0]};

i=0
File="/Users/pony/NASA/MERRA2"
for line in `awk -F"," '{print$1}' "/Users/pony/NASA/MERRA2/20180502.state.slv.aer.csv" | sort -u`
do 
    address[$i]=$line;
#    echo ${address[$i]};
    i=$(( i+1 )); 
    place=$line;
    `touch $box$place".csv"`
    for file in `ls $File/*.csv`
    do 
# echo $file
#tt=`basename $file| cut -d'.' -f1`
#    Time[$i]=$tt;
#    echo ${Time[$i]};
#   i=$(( i+1 ));

        `grep "2018" $file | grep $place |  awk -F',' '{print$1","$17","$24","$25}' >> $box$place".csv"`
    done 
done




#for file in `ls $Data/*.csv`
#do
#   echo $file
#   name=`basename $file| cut -d'.' -f1`
#   newName=$name"_"$Location"_"$DataSource
#   echo $newName 
#   out=$Load"/"$newName
#   echo $out
#   `grep $grep_L $file | sort -n -t$dot -k $sortNum > $out` 
#done
