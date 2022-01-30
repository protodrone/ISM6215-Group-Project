import configparser, random, requests
from platform import node
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
    """returns the highest/last PersonId"""
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
    """returns the highest/last CompanyId"""
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
    """generates numParents random parent company associations.
    The total number of children may not match numParents because the same
    parentId may be randomly repeatedly. This problem is exagerated in smaller
    data sets.
    """
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
    """generate numReviews number of random reviews"""
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
    """retrieves a 3 sentence random comment from the Hipster Ipsum API"""
    r = requests.get('http://hipsum.co/api/?type=hipster-centric&sentences=3')
    return r.json()[0]

def nodeHasChild(nodeId):
    """returns boolean if the Company node has children"""
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "SELECT COUNT(Id) FROM Company WHERE ParentCompany = %s"
    cursor.execute(query, (nodeId,))
    row = cursor.fetchone()
    cursor.close()
    cnx.close()
    return row[0] > 0

def printChildren(nodeId, numTabs):
    """recursively print the Company tree from a starting nodeId"""
    tabs = ""
    for i in range(numTabs):
        tabs += "\t"
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "SELECT Id,Name FROM Company WHERE ParentCompany = %s"
    cursor.execute(query, (nodeId,))
    for row in cursor.fetchall():
        print("{}--> {}".format(tabs,row[1]))
        if nodeHasChild(row[0]):
            printChildren(row[0],numTabs+1)
    cursor.close()
    cnx.close()
    return

def printCompanyTree():
    """recursively print the Company tree from root"""
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "SELECT Id FROM Company WHERE ParentCompany IS NULL"
    cursor.execute(query)
    for row in cursor.fetchall():
        printChildren(row[0], 0)
    cursor.close()
    cnx.close()
    return

print('Person Max = ', getPersonIdMax())
print('Company = ', getCompanyIdMax())

# Uncomment to randomize the parent companies
# randomizeParentCompanies(600)

# Uncomment to generate reviews
# generateReviews(4000)

# Uncomment to print random comments.
# for i in range(20):
#    print(getRandomComment())

# Uncomment to print the Company Tree
# printCompanyTree()




