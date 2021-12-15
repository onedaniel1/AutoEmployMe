import pandas as pd
import random
from datetime import datetime
import re
from dateutil.relativedelta import relativedelta

#returns firstName, lastName, birthdate, phoneNumber, ssNumber
class Person():

    def __init__(self):
        #get name in firstName and lastName strings
        firstNameList = pd.read_csv(r'.\new-top-firstNames.csv')
        lastNameList = pd.read_csv(r'.\new-top-surnames.csv')
        self.firstName = firstNameList.name.sample().values[0]
        self.lastName = lastNameList.name.sample().values[0].capitalize()
        del firstNameList
        del lastNameList

        #get birthdate in date format
        birthYear = str(random.randrange(1970,2003))
        birthMonth = str(random.randrange(1,12))
        if len(birthMonth) <2:
            birthMonth = "0" + birthMonth
        birthDay = str(random.randrange(1,28))
        if len(birthDay) <2:
            birthDay = "0" + birthDay
        self.birthdate = datetime.fromisoformat("" + birthYear + "-" + birthMonth + "-" + birthDay)
        del birthYear
        del birthMonth
        del birthDay

        #get phone numbers from shitheads in congress
        congressList = pd.read_csv(r'.\legislators-current.csv')
        congressList = congressList.loc[congressList['party'] == "Republican"]
        self.phoneNumber = congressList.phone.sample().values[0]
        del congressList

        #get social security number
        i = 0
        while i < 1:
            ssNumber = random.randrange(100000000,999999999)
            if "00" in str(ssNumber):
                i = 0
            else:
                i = 1
        self.ssNumber = ssNumber

        #get street address
        lst = ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eigth', 'Ninth', 'Park', 'Main', 'Oak', 'Pine', 'Maple', 'Cedar', 'Elm', 'View', 'Washington', 'Lake', 'Hill']
        lstsuf = ['Street', 'Lane', 'Road', "Avenue"]
        self.address = str(random.randint(500,30000)) + " " + random.choice(lst) + " " + random.choice(lstsuf)
        del lst
        del lstsuf

        #get city, state, and zip from https://simplemaps.com/data/us-cities
        cityList = pd.read_csv(r'.\uscities.csv')
        city = cityList.sample()
        self.city = city.city.values[0]
        self.state_id = city.state_id.values[0]
        self.state_name = city.state_name
        zip = str(city.zips.values[0]).split()
        self.zip = random.choice(zip)
        del city
        del cityList
        del zip

        #Get email
        x = random.randint(1,3)
        if x == 1:
            email = self.firstName + "." + self.lastName
        elif x == 2:
            email = self.firstName[0] + self.lastName
        else:
            email = self.firstName + self.lastName[0] + str(random.randint(0,999))
        emailSites = ["@live.com", "@outlook.com", "@gmail.com", "@yahoo.com"]
        self.email = email + random.choice(emailSites)
        del email


class Job():
    def __init__(self, startDate, endDate):
        self.startDate = datetime(datetime.today().year, datetime.today().month, random.randint(1,28)) - relativedelta(months = startDate)
        self.endDate = datetime(datetime.today().year, datetime.today().month, random.randint(1,28)) - relativedelta(months = endDate)
        if self.endDate > datetime.today():
            self.endDate = datetime.today()
        companies = pd.read_excel(r'.\USA_Database_Sample.xlsx')
        companies = companies.sample()
        self.name = companies.BUSINESSNAME.values[0]
        self.address = companies.ADDRESS.values[0]
        self.city = companies.CITY.values[0]
        self.state = companies.STATE.values[0]
        self.zip = companies.ZIP.values[0]
        self.phone = companies.PHONE.values[0]
        positionList = pd.read_csv(r'.\job-phrase-list.csv')
        self.position = " ".join([word.capitalize() for word in positionList.sample().values[0][0].split(" ")])
        boss = Person()
        self.bossFirst = boss.firstName
        self.bossLast = boss.lastName
        self.bossPhone = boss.phoneNumber
        self.bossPosition = " ".join([word.capitalize() for word in positionList.sample().values[0][0].split(" ")])

        del companies
        del boss
        del positionList

class School():
    def __init__(self, years):
        self.years = int(years)
        self.date = datetime(datetime.today().year, datetime.today().month, random.randint(1,28)) - relativedelta(months = random.randint(12,50))
        colleges = pd.read_csv(r'.\InstitutionCampus.csv')
        colleges = colleges.loc[colleges['LocationType'] == "Institution"]
        colleges = colleges.sample()
        self.college = colleges.LocationName.values[0]
        self.address = colleges.Address.values[0]
        if int(years) < 12:
            self.degree = "General Educational Development Certificate"
            self.college = ""
            self.address = ""
        elif int(years) >= 12 and int(years) < 14:
            del colleges
            colleges = pd.read_csv(r'.\highSchools.csv', encoding_errors='ignore')
            colleges = colleges.loc[colleges['LEVEL'] == "High"]
            colleges = colleges.sample()
            self.degree = "High school Graduate"
            self.college = colleges.SCH_NAME.values[0]
            self.address = colleges.LCITY.values[0] + ', '+ colleges.LSTATE.values[0] + ' ' + str(colleges.LZIP.values[0])
        elif int(years) >=14 and int(years) < 16:
            self.degree = "Associate's Degree"
        elif int(years) >= 16 and int(years) < 18:
            self.degree = "Bachelor's Degree"
        elif int(years) >=18:
            self.degree = "Master's Degree"
        del colleges


#Create job history for last 10 years, change months to a different number to make it longer or shorter
months = 120
i = 0
start = 0
jobs = []
while months > 0:
    
    jobLength = random.randint(1, months)
    start = months
    months = months - jobLength
    end = months
    jobs.append(Job(start, end))

#Create skills list
skillsList = pd.read_csv(r'.\Skills.csv', encoding_errors='ignore')
i = random.randint(5,15)
skills = skillsList.Skills.sample(i).values

#show resume
joe = Person()
print(joe.firstName, joe.lastName)
print(joe.email)
print(joe.phoneNumber)
print("\n\n\n                                           Skills")
print("___________________________________________________________________________________________________________________")
for i in skills:
    print (i)
print("\n\n\n                                           Education")
print("___________________________________________________________________________________________________________________")
mySchool = School(random.randint(10,19))
print (mySchool.degree + "       " + mySchool.date.strftime('%x'))
print(mySchool.college)
print(mySchool.address)
print("\n\n\n                                           Job History")
print("___________________________________________________________________________________________________________________")#

for i in jobs:
    print ("Name:       " + i.name)
    print ("Position:   " + i.position)
    print ("Start Date: " + i.startDate.strftime('%x') + "     End Date:   " + i.endDate.strftime('%x'))
    print ("Address:    " + str(i.address))
    print ("            " + i.city + ", " + i.state + " " + str(i.zip))
    print ("Supervisor: " + i.bossFirst + " " + i.bossLast)
    print ("Phone:      " + i.phone)
    print ("\n")