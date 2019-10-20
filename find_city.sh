#!/bin/bash
#Azusa#
#Compton#
#CostaMesa#
#Glendora#
#LAX_Hastings#
#LaHabra#
#Lancaster#
#LongBeach#
#LosAngeles#
#MissionViejo#
#Pasadena#
#PicoRivera#
#Pomona#
#Reseda#
#SantaClarita#
#SouthLongBeach#
#GREP_L=(#Azusa# #Compton# #Costa Mesa - Mesa Ve# #Glendora - Laurel# #LAX-Hastings# #La Habra# #Lancaster-Division# #Long Beach - Hudson# #Los Angeles - N. Mai# #Mission Viejo# #Pasadena# #Pico Rivera# #Pomona# #Reseda# #Santa Clarita# #South Long Beach# #West Los Angeles - V#)
    

Data_L="/Users/pony/NASA/LosAngeles.csv"


Location="CostaMesa"
Load="/Users/pony/NASA/rawData_CostaMesa"
`grep "2018"  $Data_L | grep "Costa Mesa" >  $Load"/2018_"$Location"_LosAngeles.csv"` 

Location="Compton"
Load="/Users/pony/NASA/rawData_Compton"
`grep "2018"  $Data_L | grep "Compton" >  $Load"/2018_"$Location"_LosAngeles.csv"` 
