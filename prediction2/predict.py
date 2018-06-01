import json
from sklearn.externals import joblib
import csv
from data_input import data_input
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
import numpy as np
from itertools import izip

def LoadData(filePath):
	reader = csv.reader(open(filePath))
	jobList = []
	for i,row in enumerate(reader):
		if i > 0:
			jobList.append(data_input(row))
	return jobList

def TokenizingTestData(data,start,end,vect,vect2):
	targets = []
	desTests = []
	titleTests = []
	for i in xrange(start,end):
		job = data[i].data
		desTests.append(job['organization'] + ' ' + job['joblocation'] + ' ' + job['education'] + ' ' + 
		job['experience'] + ' ' + job['employmentType'] + ' ' + job['industry'] + ' ' + job['jobfunction'])
		titleTests.append(job['title'])
	des = vect.transform(desTests)
	title = vect2.transform(titleTests)
	tests = hstack((des,title))
	return tests

def getTestData(data,start,end,vect,vect2,vect3,vect4,vect5,vect6,vect7,vect8):
	targets = []
	desTests = []
	titleTests = []
	levelTests = []
	orgTests = []
	loTests = []
	eduTests = []
	expTests = []
	indTests = []	
	jobfuncTests = []
	for i in xrange(start,end):
		job = data[i].data
		titleTests.append(job['title'])
		levelTests.append(job['level'])
		orgTests.append(job['organization'])
		loTests.append(job['joblocation'])
		eduTests.append(job['education'])
		expTests.append(job['experience'])
		indTests.append(job['industry'])
		jobfuncTests.append(job['jobfunction'])
		#desTests.append(job['level'] + ' ' + job['organization'] + ' ' + job['joblocation'] + ' ' + job['education'] + ' ' + 
		#job['experience'] + ' ' + job['employmentType'] + ' ' + job['industry'] + ' ' + job['jobfunction'])		
	title = vect1.transform(titleTests)
	level = vect2.transform(levelTests)
	org = vect3.transform(orgTests)
	lo = vect4.transform(loTests)
	edu = vect5.transform(eduTests)
	exp = vect6.transform(expTests)
	ind = vect7.transform(indTests)
	jobfunc = vect8.transform(jobfuncTests)
	#des = vect2.transform(desTests)
	tests = hstack((title,level,org,lo,edu,exp,ind,jobfunc))
	return tests

paths = json.load(open('/home/onani/Desktop/SeniorProject_WebApplication/prediction/SETTINGS.json','rb'))
#print 'Loading models'
model = joblib.load('/home/onani/Desktop/SeniorProject_WebApplication/prediction/model.p')
vect1 = joblib.load('/home/onani/Desktop/SeniorProject_WebApplication/prediction/vect1.p')
vect2 = joblib.load('/home/onani/Desktop/SeniorProject_WebApplication/prediction/vect2.p')
vect3 = joblib.load('/home/onani/Desktop/SeniorProject_WebApplication/prediction/vect3.p')
vect4 = joblib.load('/home/onani/Desktop/SeniorProject_WebApplication/prediction/vect4.p')
vect5 = joblib.load('/home/onani/Desktop/SeniorProject_WebApplication/prediction/vect5.p')
vect6 = joblib.load('/home/onani/Desktop/SeniorProject_WebApplication/prediction/vect6.p')
vect7 = joblib.load('/home/onani/Desktop/SeniorProject_WebApplication/prediction/vect7.p')
vect8 = joblib.load('/home/onani/Desktop/SeniorProject_WebApplication/prediction/vect8.p')

#print 'loading testing data',paths['TEST_DATA_PATH']
validData = LoadData('/home/onani/Desktop/SeniorProject_WebApplication/prediction/test.csv')
titles = [validData[i].data['title'] for i in xrange(len(validData))]
#validSalary = [validData[i].data['SalaryMid'] for i in xrange(len(validData))]
validTests = getTestData(validData,0,len(validData),vect1,vect2,vect3,vect4,vect5,vect6,vect7,vect8)

#print 'predicting'
predictions = np.exp(model.predict(validTests))

#print 'writing to csv'
#with open(paths['SUBMISSION_PATH'],'wb') as fOut:
#    out = csv.writer(fOut)
#    for row in izip(titles,validSalary,predictions):
#        out.writerow(row)

print predictions[0]
