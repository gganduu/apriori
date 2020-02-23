# apriori
This is an implementation of Apriori algorithm in Python

There are two example data uploaded.

Command example: python apriori.py -s 0.5 -c 0.9 -f bank_user_background.data
Results:
Namespace(input_file='bank_user_background.data', min_conf=0.9, min_sup=0.5)
**2-frequent pattern**
frozenset({'country=United-States', 'sex=Male'})-->0.5983170222349617
frozenset({'race=White', 'sex=Male'})-->0.5883256213914254
frozenset({'country=United-States', 'workclass=Private'})-->0.6171942180909873
frozenset({'race=White', 'workclass=Private'})-->0.5942426600057328
frozenset({'salary<=50K', 'workclass=Private'})-->0.5429548339543835
frozenset({'country=United-States', 'salary<=50K'})-->0.6784734449858728
frozenset({'salary<=50K', 'race=White'})-->0.6378731419679784
frozenset({'country=United-States', 'race=White'})-->0.7881126898980386
frozenset({'country=United-States', 'hours=full-time'})-->0.5179558576634864

**3-frequent pattern**
frozenset({'country=United-States', 'race=White', 'sex=Male'})-->0.5415421153924901
frozenset({'country=United-States', 'race=White', 'workclass=Private'})-->0.5433847917775685
frozenset({'country=United-States', 'salary<=50K', 'race=White'})-->0.5835346627902215

**1-frequent pattern**
frozenset({'hours=full-time'})-->0.5850907006265099
frozenset({'country=United-States'})-->0.8974243478973015
frozenset({'race=White'})-->0.855042791040498
frozenset({'salary<=50K'})-->0.7607182343065395
frozenset({'workclass=Private'})-->0.6941976168052086
frozenset({'sex=Male'})-->0.6684820441423365

Rules:
("frozenset({'race=White'})-->frozenset({'country=United-States'})", 0.9217230975527992)
("frozenset({'race=White', 'sex=Male'})-->frozenset({'country=United-States'})", 0.9204802505655124)
("frozenset({'country=United-States', 'sex=Male'})-->frozenset({'race=White'})", 0.9051089894945762)
("frozenset({'race=White', 'workclass=Private'})-->frozenset({'country=United-States'})", 0.9144156560088202)
("frozenset({'salary<=50K', 'race=White'})-->frozenset({'country=United-States'})", 0.9148130316161128)

