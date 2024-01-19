-- Drop the procedure if it exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Create the procedure
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    -- Calculate the total weighted score and total weight
    SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
    INTO total_weighted_score, total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Update the average_score for the user
    UPDATE users
    SET users.average_score = IFNULL(total_weighted_score / NULLIF(total_weight, 0), 0)
    WHERE users.id = user_id;
END $$

DELIMITER ;
