import configparser, random, requests
from turtle import position
import mysql.connector
from mysql.connector import errorcode

config = configparser.ConfigParser()
config.read('config.ini')

cnxdict = {
    'user' : config['MySQL']['dbuser'],
    'password' : config['MySQL']['dbpassword'],
    'host' : config['MySQL']['dbserver'],
    'database' : config['MySQL']['dbname'],
    'raise_on_warnings' : True
}

def getPersonIdMax():
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "SELECT MAX(Id) FROM Person"
    cursor.execute(query)
    row = cursor.fetchone()
    max = row[0]
    cursor.close()
    cnx.close()
    return max

def getCompanyIdMax():
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "SELECT MAX(Id) FROM Company"
    cursor.execute(query)
    row = cursor.fetchone()
    max = row[0]
    cursor.close()
    cnx.close()
    return max

def randomizeParentCompanies(numParents):
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    cursor.execute("UPDATE Company SET ParentCompany = NULL")
    max = getCompanyIdMax()
    for i in range(numParents):
        query = "UPDATE Company SET ParentCompany = %s WHERE Id = %s"
        cursor.execute(query,(random.randrange(1,max), random.randrange(1,max)))
    cursor.close()
    cnx.commit()
    cnx.close()
    return

def generateReviews(numReviews):
    companyMax = getCompanyIdMax()
    personMax = getPersonIdMax()
    with open('Cities.txt') as f:
        city = f.read().splitlines()
    with open('JobNames.csv') as f:
        job = f.read().splitlines()
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    for i in range(numReviews):
        query = "INSERT INTO Review (PersonId,CompanyId,BranchLocation,YearsOfService,PositionAtCompany,CreateTimestamp)" 
        query += "VALUES (%s, %s, %s, %s, %s, NOW())"
        personId = random.randrange(1, personMax)
        companyId = random.randrange(1, companyMax)
        branch = city[random.randrange(0, len(city))]
        years = random.randrange(1,30)
        position = job[random.randrange(0, len(job))]
        cursor.execute(query, (personId, companyId, branch, years, position))
    cursor.close()
    cnx.commit()
    cnx.close()
    return

def getRandomComment():
    r = requests.get('http://hipsum.co/api/?type=hipster-centric&sentences=3')
    return r.json()[0]

print('Person Max = ', getPersonIdMax())
print('Company = ', getCompanyIdMax())
randomizeParentCompanies(600)
generateReviews(4000)
# for i in range(20):
#    print(getRandomComment())





