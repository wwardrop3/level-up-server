SELECT
    e.id,
    e.description,
    e.game_id,
    e.organizer_id,
    o.bio,
    g.title
FROM levelupapi_event e
JOIN levelupapi_gamer o
ON e.organizer_id = o.id
JOIN levelupapi_game g
ON e.game_id = g.id



SELECT
    e.id,
    e.date,
    e.description,
    e.organizer_id,
    e.game_id,
    o.bio

FROM levelupapi_event e
JOIN levelupapi_gamer o

Drop Table 

SELECT * FROM Gamer