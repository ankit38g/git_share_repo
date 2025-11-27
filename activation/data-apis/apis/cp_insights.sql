{% cache %}
SELECT 
  customer_id,
  CASE 
    WHEN random() < 0.33 THEN 'High Risk'
    WHEN random() < 0.66 THEN 'Moderate Risk'
    ELSE 'Low Risk'
  END AS customer_segments,
  CASE 
    WHEN random() < 0.33 THEN CASE WHEN random() < 0.5 THEN 'Pair Wine with Meat' ELSE 'Pair Fish with Sweet Products' END
    WHEN random() < 0.66 THEN CASE WHEN random() < 0.5 THEN 'Pair Meat with Fruits' ELSE 'Pair Wine with Fish' END
  ELSE 
      CASE WHEN random() < 0.5 THEN 'Pair Fruits with Sweet Products' ELSE 'Pair Wine with Fruits' END 
  END AS cross_sell_recommendations
FROM cross_sell_cache

{% endcache %}