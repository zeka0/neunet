from ether import *

debug = True
filePath = r'E:\VirtualDesktop\nnet\csv\reddit-comments-2015-08.csv'
model_fname = 'nltk-rnn'

csv_reader = neoCsvReader(filePath)
db = fullPool(csv_reader.read_all(), True)
ff = nltkFilter()
db = filterPool(db, ff)

x = db.read_instances(1)
print 'OK'