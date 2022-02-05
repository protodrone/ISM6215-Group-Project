/*
  Company Star Review Histogram
*/

SELECT
	c.Name,
    q.QuestionText,
    CONCAT(sa.Answer, ' Stars') AS Stars,
    COUNT(sa.Answer) AS Total
FROM 
	StarAnswers sa
    INNER JOIN Answers a ON sa.AnswerId = a.Id
    INNER JOIN Review r on a.ReviewId = r.Id
    INNER JOIN Company c on r.CompanyId = c.Id
    INNER JOIN ReviewQuestions q on a.QId = q.Id
GROUP BY
	c.Name, q.QuestionText, sa.Answer
ORDER BY
	c.Name ASC, q.QuestionText ASC, sa.Answer DESC
;

/*
  Cities with Company Branches with > 1 Review
*/
SELECT 
	r.BranchLocation,
    c.Name,
    COUNT(r.Id) AS TotalReviews
FROM 
	Review r
    INNER JOIN Company c on r.CompanyId = c.Id
GROUP BY
	r.BranchLocation, c.Name
HAVING
	TotalReviews > 1
ORDER BY
	TotalReviews DESC, r.BranchLocation ASC, c.Name ASC
    ;

/*
 Sample data summary.
*/
SELECT
	(SELECT COUNT(Id) FROM Person) AS People,
    (SELECT COUNT(Id) FROM Company) AS Companies,
    (SELECT COUNT(Id) FROM ReviewQuestions) AS Questions,
    (SELECT COUNT(Id) FROM Review) AS Reviews,
    (SELECT COUNT(Id) FROM Answers) AS Answers,
    (SELECT COUNT(Id) FROM StarAnswers) AS StarAnswers,
    (SELECT COUNT(Id) FROM CommentAnswers) AS CommentAnswers
;

/*
 Top 10 Reviewers by Review Quantity
*/
SELECT DISTINCT
	CONCAT(p.Lname, ', ', p.FirstName) AS Person,
    (SELECT COUNT(DISTINCT CompanyId) FROM Review WHERE PersonId = p.Id) AS CompaniesReviewed
FROM 
	Person p
    INNER JOIN Review r on p.Id = r.PersonId
    INNER JOIN Company c on r.CompanyId = c.Id
ORDER BY
	CompaniesReviewed DESC
LIMIT 10
;

/*
 Companies with a Parent Company
*/
SELECT
	c.Name AS CompanyName,
    (SELECT Name from Company where Id = c.ParentCompany) AS ParentCompany
FROM
	Company c
WHERE 
	c.ParentCompany IS NOT NULL
;

/*
	Top 10 Companies by direct subsidiary quantity, depth of 1
    It is important to note that this query only caluculates the Company Tree to a depth of 1,
    as SQL is limited to fixed iteration and lacks dynamic recursion. This is an artifact of being
    a query languge and not a turing complete programming language. 
*/
SELECT
	c.Name AS CompanyName,
    (SELECT COUNT(Id) FROM COMPANY WHERE ParentCompany = c.Id) AS Subsidiaries
FROM 
	Company c
ORDER BY
	Subsidiaries DESC
LIMIT 10
;