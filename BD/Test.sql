SELECT *
FROM Nationalities

SELECT *
FROM Federations

SELECT *
FROM Events

SELECT *
FROM HasOrganisedEvent

SELECT *
FROM Wrestlers

SELECT EventID, EventName, EventCagematchRating
FROM Events
ORDER BY EventCagematchRating DESC

SELECT MAX(EventID) FROM Events