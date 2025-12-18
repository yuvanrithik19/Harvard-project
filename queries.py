# queries.py

SQL_QUERIES = {
    "1. List all artifacts from the 11th century belonging to Byzantine culture":
        "SELECT * FROM artifacts_metadata WHERE century='11th century' AND culture='Byzantine';",

    "2. What are the unique cultures represented in the artifacts?":
        "SELECT DISTINCT culture FROM artifacts_metadata WHERE culture IS NOT NULL;",

    "3. List all artifacts from the Archaic Period":
        "SELECT * FROM artifacts_metadata WHERE period='Archaic';",

    "4. List artifact titles ordered by accession year in descending order":
        "SELECT title, accessionyear FROM artifacts_metadata ORDER BY accessionyear DESC;",

    "5. How many artifacts are there per department?":
        "SELECT department, COUNT(*) AS total FROM artifacts_metadata GROUP BY department;",

    "6. Oldest 20 artifacts by accession year":
        "SELECT * FROM artifacts_metadata ORDER BY accessionyear ASC LIMIT 20;",

    "7. Which artifacts have more than 1 image?":
        "SELECT am.title, m.mediacount FROM artifacts_media m JOIN artifacts_metadata am ON am.id = m.objectid WHERE m.mediacount > 1;",

    "8. What is the average rank of all artifacts?":
        "SELECT AVG(rank_d) AS avg_rank FROM artifacts_media;",

    "9. Which artifacts have a higher colorcount than mediacount?":
        "SELECT am.title, m.colorcount, m.mediacount FROM artifacts_metadata am JOIN artifacts_media m ON am.id = m.objectid WHERE m.colorcount > m.mediacount;",

    "10. List all artifacts created between 1500 and 1600":
        "SELECT am.title, m.datebegin, m.dateend FROM artifacts_metadata am JOIN artifacts_media m ON am.id = m.objectid WHERE m.datebegin >= 1500 AND m.dateend <= 1600;",

    "11. How many artifacts have no media files?":
        "SELECT COUNT(*) AS no_media FROM artifacts_media WHERE mediacount = 0 OR mediacount IS NULL;",

    "12. Maximum imagecount per classification":
        "SELECT am.classification, MAX(m.imagecount) AS max_images FROM artifacts_media m JOIN artifacts_metadata am ON am.id = m.objectid GROUP BY am.classification;",

    "13. What are all the distinct hues used in the dataset?":
        "SELECT DISTINCT hue FROM artifacts_colors;",

    "14. What are the top 5 most used colors by frequency?":
        "SELECT color, COUNT(*) AS frequency FROM artifacts_colors GROUP BY color ORDER BY frequency DESC LIMIT 5;",

    "15. What is the average coverage percentage for each hue?":
        "SELECT hue, AVG(percent) AS avg_percent FROM artifacts_colors GROUP BY hue;",

    "16. List all colors used for a given artifact ID":
        "SELECT color FROM artifacts_colors WHERE objectid = :id;",

    "17. What is the total number of color entries in the dataset?":
        "SELECT COUNT(*) AS total_colors FROM artifacts_colors;",

    "18. Hue frequency per classification":
        "SELECT am.classification, c.hue, COUNT(*) AS frequency FROM artifacts_colors c JOIN artifacts_metadata am ON c.objectid = am.id GROUP BY am.classification, c.hue ORDER BY am.classification, frequency DESC;",

    "19. List artifact titles and hues for all artifacts belonging to the Byzantine culture":
        "SELECT am.title, ac.color AS hue FROM artifacts_metadata am JOIN artifacts_colors ac ON am.id = ac.objectid WHERE am.culture = 'Byzantine';",

    "20. List each artifact title with its associated hues":
        "SELECT am.title, ac.color AS hue FROM artifacts_metadata am JOIN artifacts_colors ac ON am.id = ac.objectid ORDER BY am.title;",

    "21. Get artifact titles, cultures, and media ranks where the period is not null":
        "SELECT am.title, am.culture, m.rank_d AS media_rank FROM artifacts_metadata am JOIN artifacts_media m ON am.id = m.objectid WHERE am.period IS NOT NULL;",

    "22. Find artifact titles ranked in the top 10 that include the color Grey":
        "SELECT am.title FROM artifacts_metadata am JOIN artifacts_media m ON am.id = m.objectid JOIN artifacts_colors ac ON am.id = ac.objectid WHERE ac.color = 'Grey' ORDER BY m.rank_d LIMIT 10;",

    "23. How many artifacts exist per classification, and what is the average media count for each?":
        "SELECT am.classification, COUNT(*) AS artifact_count, AVG(m.mediacount) AS avg_media_count FROM artifacts_metadata am JOIN artifacts_media m ON am.id = m.objectid GROUP BY am.classification;",

    "24. Count artifacts grouped by century":
        "SELECT century, COUNT(*) AS artifact_count FROM artifacts_metadata GROUP BY century;",

    "25. List all artifact titles along with their culture and each color they have":
        "SELECT am.title, am.medium, m.mediacount FROM artifacts_metadata am JOIN artifacts_media m ON am.id = m.objectid ORDER BY am.title;"
}
