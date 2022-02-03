import configparser, random, requests
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
    print("Getting Person Ids.")
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
    print("Getting Company Id Max")
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "SELECT MAX(Id) FROM Company"
    cursor.execute(query)
    row = cursor.fetchone()
    max = row[0]
    cursor.close()
    cnx.close()
    return max

def getSentenceIdMax():
    """returns the highest/last sentences Id"""
    print("Getting sentences Id Max")
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "SELECT MAX(Id) FROM sentences"
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
    print("Randomizing Parent Companies")
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
    print("Generating Reviews")
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

def generateQuestionTypes():
    """insert default question types of star and comment"""
    print("Generating default question types of Star and Comment.")
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "INSERT INTO QuestionType (Type) VALUES ('Star'),('Comment')"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()
    return

def generateQuestions():
    """insert default sample questions"""
    print("Generate default sample Star and Comment questions 1-5.")
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "INSERT INTO ReviewQuestions (QTypeId, QuestionText) VALUES"
    query += " (1, 'Star Question 1'),"
    query += " (1, 'Star Question 2'),"
    query += " (1, 'Star Question 3'),"
    query += " (1, 'Star Question 4'),"
    query += " (1, 'Star Question 5'),"
    query += " (2, 'Comment Question 1'),"
    query += " (2, 'Comment Question 2'),"
    query += " (2, 'Comment Question 3'),"
    query += " (2, 'Comment Question 4'),"
    query += " (2, 'Comment Question 5')"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()
    return

def getReviewIds():
    """returns a list of current Review Ids"""
    print("Getting Review Ids")
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "SELECT Id FROM Review"
    cursor.execute(query)
    reviewIds = cursor.fetchall()
    cursor.close()
    cnx.close()
    return reviewIds

def getQuestionIds():
    """returns a list of current Question Ids"""
    print("Getting Question Ids")
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "SELECT Id FROM ReviewQuestions"
    cursor.execute(query)
    ReviewQuestionIds = cursor.fetchall()
    cursor.close()
    cnx.close()
    return ReviewQuestionIds

def insertAnswer(QId, ReviewId):
    """Inserts a single answer."""
    print("Inserting Answer")
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "INSERT INTO Answers (QId, ReviewId) VALUES (%s, %s)"
    cursor.execute(query, (QId, ReviewId))
    cnx.commit()
    cursor.close()
    cnx.close()
    return

def insertManyAnswers(answers):
    """Inserts a list of answers."""
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "INSERT INTO Answers (QId, ReviewId) VALUES (%s, %s)"
    cursor.executemany(query, answers)
    cnx.commit()
    cursor.close()
    cnx.close()
    return
    return

def generateAnswers():
    """generates an answer for each question for each review"""
    questionIds = getQuestionIds()
    answers = []
    for id in getReviewIds():
        for qid in questionIds:
            answers.append((qid[0],id[0]))
    insertManyAnswers(answers)
    return

def getAnswerIds():
    """returns a list of current Answers Ids"""
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "SELECT Id FROM Answers"
    cursor.execute(query)
    AnswerIds = cursor.fetchall()
    cursor.close()
    cnx.close()
    return AnswerIds

def insertManyCommentAnswers(commentAnswers):
    """Inserting Comment Answer List"""
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "INSERT INTO CommentAnswers (AnswerId, Comment) VALUES (%s, %s)"
    cursor.executemany(query, commentAnswers)
    cnx.commit()
    cursor.close()
    cnx.close()
    return

def getCommentAnswerIds():
    """returns a list of current Comment Answers Ids"""
    print("Getting Comment Answer Ids.")
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "select a.Id from Answers a inner join ReviewQuestions q on a.QId = q.Id"
    query += " inner join QuestionType qt on q.QTypeId = qt.Id where qt.Type = 'Comment'"
    cursor.execute(query)
    CommentAnswerIds = cursor.fetchall()
    cursor.close()
    cnx.close()
    return CommentAnswerIds

def getSentence(Id):
    """returns a specific sentence"""
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "SELECT sentence FROM sentences WHERE id = %s"
    cursor.execute(query,(Id,))
    row = cursor.fetchone()
    max = row[0]
    cursor.close()
    cnx.close()
    return max

def getAllSentences():
    """returns the list of sentences"""
    print("Getting sentences")
    cnx = mysql.connector.connect(**cnxdict)
    cursor = cnx.cursor()
    query = "SELECT sentence FROM sentences"
    cursor.execute(query)
    sentences = cursor.fetchall()
    cursor.close()
    cnx.close()
    return sentences

def generateCommentAnswers():
    """Generating Comment Answers."""
    print("Generating Comment Answers.")
    max = getSentenceIdMax()
    commentAnswers = []
    commentAnswerIds = getCommentAnswerIds()
    sentences = getAllSentences()
    print("Found {} Comment Answer Ids".format(len(commentAnswerIds)))
    for a in commentAnswerIds:
        commentAnswers.append((a[0],sentences[random.randrange(0,max)][0]))
    #print(commentAnswers[0:4])
    insertManyCommentAnswers(commentAnswers)
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
# generateQuestionTypes()
# generateQuestions()
# generateAnswers()
# generateCommentAnswers()




