{% cache %}

 with random_cat as(select customer_id,   CASE
      WHEN random() < 0.2 THEN 'Wines'
      WHEN random() < 0.4 THEN 'Meats'
      WHEN random() < 0.6 THEN 'Fish'
      WHEN random() < 0.8 THEN 'Sweet Products'
      ELSE 'Fruits'
    END AS product_category from affinity_cache) 
  SELECT 
    cp1.product_category AS category_1,
    cp2.product_category AS category_2,
    COUNT(DISTINCT cp1.customer_id)*4/10.0 AS product_affinity_score
  FROM random_cat cp1
    INNER JOIN random_cat cp2 
  ON cp1.customer_id = cp2.customer_id AND cp1.product_category <> cp2.product_category 
  group by 1,2
{% endcache %}