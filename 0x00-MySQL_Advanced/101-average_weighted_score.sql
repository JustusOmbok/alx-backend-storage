-- Drop the procedure if it exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Create the procedure
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done BOOLEAN DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;

    -- Declare cursor for user ids
    DECLARE users_cursor CURSOR FOR SELECT id FROM users;
    -- Declare continue handler for not found
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN users_cursor;

    -- Loop over user ids
    user_loop: LOOP
        FETCH users_cursor INTO user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Initialize variables for each user
        SET total_weighted_score = 0;
        SET total_weight = 0;

        -- Calculate the total weighted score and total weight for the user
        SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
        INTO total_weighted_score, total_weight
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Update the average_score for the user
        UPDATE users
        SET users.average_score = IFNULL(total_weighted_score / NULLIF(total_weight, 0), 0)
        WHERE users.id = user_id;
    END LOOP;

    -- Close the cursor
    CLOSE users_cursor;
END $$

DELIMITER ;
