-- List all bands with Glam rock as their main style, ranked by longevity
-- Assumes the metal_bands table is already imported

SELECT band_name, (IFNULL(split, '2022') - formed) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY lifespan DESC, band_name;
