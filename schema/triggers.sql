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

-----------TRIGGER FUNCTION FOR CHECKING RETURN DATE (less than 30 days)------------
CREATE OR REPLACE FUNCTION is_return_valid()
RETURNS TRIGGER
LANGUAGE PLPGSQL
AS $$
DECLARE
buy_date DATE;
deadline DATE;
BEGIN
	buy_date:=(
		SELECT order_date 
		FROM orders
		WHERE id=NEW.order_id
	);
	deadline:=buy_date+INTERVAL'30 day';
	IF deadline<NEW.return_date
	THEN
		RAISE EXCEPTION 
		'Return period expired on %(more than 30 days)!',deadline;
	ELSIF (NEW.order_id,NEW.product_id) IN 
	(SELECT order_id,product_id FROM orderitems) THEN
		RAISE EXCEPTION 
		'There is no such product in order!';
	ELSE 
		RETURN NEW;
	END IF;
END;
$$;

CREATE OR REPLACE TRIGGER enforce_return_window
BEFORE INSERT OR UPDATE ON returns
FOR EACH ROW
EXECUTE FUNCTION is_return_valid();