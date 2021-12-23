SELECT f.id, s.id FROM song f
    INNER JOIN song s ON f.id != s.id
EXCEPT
    SELECT firstId, secondId FROM correlation
EXCEPT
    SELECT secondId, firstId FROM correlation;
