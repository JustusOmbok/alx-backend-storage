-- Rank country origins of bands by the number of non-unique fans
-- Assumes the metal_bands table is already imported

SELECT origin, SUM(fans) as nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
