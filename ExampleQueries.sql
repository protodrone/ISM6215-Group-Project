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