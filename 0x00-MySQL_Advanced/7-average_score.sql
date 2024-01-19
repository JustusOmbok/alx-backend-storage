-- Create a stored procedure ComputeAverageScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE total_score INT;
    DECLARE total_projects INT;
    DECLARE average_score FLOAT;

    -- Compute the total score and the total number of projects
    SELECT
        SUM(score), 0) INTO total_score,
        COUNT(DISTINCT project_id), 1) INTO total_projects
    FROM corrections
    WHERE user_id = user_id;

    -- Compute the average score
    SET average_score = total_score / total_projects;

    -- Update the user's average score in the users table
    UPDATE users
    SET average_score = average_score
    WHERE id = user_id;
END //

DELIMITER ;
