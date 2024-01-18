-- List all bands with Glam rock as their main style, ranked by longevity
-- Assumes the metal_bands table is already imported

SELECT
    band_name,
    CASE
        WHEN split IS NULL THEN 0
        ELSE 2022 - formed
    END AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC, band_name;
