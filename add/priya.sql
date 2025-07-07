SELECT 
    a.id,
    a.name,
    b.order_date,
    b.amount
FROM 
    customers a
LEFT JOIN 
    orders b
ON 
    a.id = b.customer_id;
