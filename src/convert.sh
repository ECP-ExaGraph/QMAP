#!/bin/bash

dataFolder=/home/khan242/quantum/nwchem/QA/chem_library_tests/
#dataFolder=/home/khan242/quantum/nwchem/QA/chem_library_tests/


for i in `ls -1 $dataFolder`
do
	echo $dataFolder$i
	python nwchem_parser.py $dataFolder$i/
done
