CREATE TYPE IF NOT EXISTS Order_status AS ENUM
(
  'pending',
  'processing',
  'shipped',
  'delivered',
  'cancelled'
);

CREATE TABLE IF NOT EXISTS Customers
(
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	email TEXT,
	signup_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS Categories
(
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Products
(
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	category_id INT NOT NULL 
		REFERENCES Categories(id)
		ON DELETE RESTRICT,
	price NUMERIC(10,2) NOT NULL
		CHECK (price>=0)
);

CREATE TABLE IF NOT EXISTS Orders 
(
	id SERIAL PRIMARY KEY, 
	customer_id INT NOT NULL 
		REFERENCES Customers(id)
		ON DELETE RESTRICT,
	order_date DATE NOT NULL, 
	status Order_status NOT NULL 
		DEFAULT  'pending'
);

CREATE TABLE IF NOT EXISTS OrderItems
(
	order_id INT NOT NULL 
		REFERENCES Orders(id)
		ON DELETE CASCADE,

	product_id INT NOT NULL 
		REFERENCES Products(id)
		ON DELETE RESTRICT,
	quantity INT NOT NULL
		CHECK (quantity>=0), 
	unit_price NUMERIC(10,2) NOT NULL,
	PRIMARY KEY(order_id,product_id)
);

CREATE TABLE IF NOT EXISTS "Returns"
(
	order_id INT NOT NULL,
	product_id INT NOT NULL,
	return_date DATE NOT NULL DEFAULT CURRENT_DATE,
	reason TEXT,
	CONSTRAINT fk_order_product_id
		FOREIGN KEY (order_id,product_id)
		REFERENCES OrderItems(order_id,product_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
	PRIMARY KEY(order_id,product_id)
);
