-----------FUNCTIONS FOR REVENUE DISPLAYMENT------------
CREATE OR REPLACE FUNCTION get_monthly_revenue()
RETURNS TABLE(value NUMERIC(12,2),month TEXT,status order_status)
LANGUAGE SQL
AS $$
	SELECT SUM(i.unit_price*i.quantity) AS value,
	SUBSTRING(o.order_date::TEXT,1,7) AS month,o.status
	FROM orderitems i JOIN orders o
	ON o.id=i.order_id
	GROUP BY SUBSTRING(o.order_date::TEXT,1,7),o.status;
$$;

CREATE OR REPLACE FUNCTION get_total_revenue()
RETURNS TABLE(value NUMERIC(12,2),status order_status)
LANGUAGE SQL
AS $$
	SELECT SUM(i.unit_price*i.quantity) AS value,o.status
	FROM orderitems i JOIN orders o
	ON o.id=i.order_id
	GROUP BY o.status;
$$;


-----------TRIGGER FUNCTION FOR CUSTOMER NAME NORMALISATION------------
CREATE OR REPLACE FUNCTION normalize_data()
RETURNS TRIGGER
LANGUAGE PLPGSQL
AS $$
BEGIN
	NEW.name:=INITCAP(TRIM(NEW.name));
	RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS data_normalization ON customers;
CREATE TRIGGER data_normalization
BEFORE INSERT ON customers
EXECUTE FUNCTION normalize_data();


-----------Monthly Category Sales Performance------------
CREATE OR REPLACE FUNCTION sales_performance()
RETURNS TABLE(name TEXT,status order_status,revenue NUMERIC(12,2),month TEXT)
LANGUAGE SQL
AS $$
SELECT c.name,o.status,SUM(i.quantity*i.unit_price) AS revenue,
SUBSTRING(o.order_date::TEXT,1,7) AS month
FROM orderitems i JOIN orders o
ON i.order_id=o.id
JOIN products p
ON i.product_id=p.id
JOIN categories c
ON c.id=p.category_id
GROUP BY c.name,o.status,SUBSTRING(o.order_date::TEXT,1,7)
ORDER BY month DESC,name;
$$;

------------New vs. Returning Customer Analysis------------
CREATE OR REPLACE FUNCTION customer_retention(start_date DATE, end_date DATE)
RETURNS TABLE(month DATE,"returned customers" INT, "new customers" INT)
LANGUAGE SQL
AS $$
	SELECT DATE_TRUNC('month',o1.order_date),
	COUNT( DISTINCT
		CASE
		WHEN o2.order_date IS NOT NULL THEN o1.customer_id
		END
	) AS "return customers",
	COUNT( DISTINCT
		CASE
		WHEN o2.order_date IS NULL THEN o1.customer_id
		END
	) AS "new customers"
	FROM orders o1 LEFT JOIN orders o2 
	on o1.customer_id=o2.customer_id AND 
	o2.order_date<o1.order_date
	WHERE o1.order_date BETWEEN start_date AND end_date
	GROUP BY DATE_TRUNC('month',o1.order_date);
$$;

----------------Rating customers----------------
CREATE OR REPLACE FUNCTION customer_analisis(
start_date DATE,end_date DATE
)
RETURNS TABLE(
"customer id" INT,"money spent" NUMERIC(12,2),
"orders number" INT,"money returned" NUMERIC(12,2),
"returned orders number" INT,
"net revenue" NUMERIC(12,2)
)
LANGUAGE SQL
AS $$
	WITH revenue AS 
	(
		SELECT o.customer_id,SUM(i.quantity*i.unit_price) AS money_spent,
		COUNT(DISTINCT i.order_id) AS number_bought
		FROM orders o JOIN orderitems i
		ON o.id=i.order_id
		WHERE o.order_date BETWEEN start_date AND end_date
		GROUP BY o.customer_id
	),
	returned AS
	(
		SELECT o.customer_id,SUM(i.quantity*i.unit_price) AS money_returned,
		COUNT(*) AS number_returned
		FROM returns r JOIN orders o
		ON o.id=r.order_id
		JOIN orderitems i
		ON i.order_id=r.order_id AND r.product_id=i.product_id
		WHERE o.order_date BETWEEN start_date AND end_date AND
		r.return_date BETWEEN start_date AND end_date
		GROUP BY o.customer_id
	)
	SELECT rev.customer_id AS "customer id",
	rev.money_spent AS "money spent",
	rev.number_bought AS "orders number",
	COALESCE(ret.money_returned,0) AS "money returned",
	COALESCE(ret.number_returned,0) AS "returned orders number",
	(rev.money_spent-COALESCE(ret.money_returned,0)) AS "net revenue"
	FROM revenue rev LEFT JOIN returned ret
	ON rev.customer_id=ret.customer_id
	ORDER BY "net revenue" DESC;
$$;

