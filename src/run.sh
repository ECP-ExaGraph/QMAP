dataFolder=/Users/khan242/PNNL/QCAT/results


for i in `ls ../layout|grep edges`
do
>out.csv
python3 QMap.py All 1 ../layout/$i
mv out.csv hipc20_1_$i.csv
done
