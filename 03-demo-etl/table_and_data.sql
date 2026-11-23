-- Create the customer table if it doesn't exist
CREATE TABLE IF NOT EXISTS customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    city VARCHAR(100) NOT NULL
);
-- Insert 100 random customer records
DO $$
DECLARE
    i INT;
    cities TEXT[] := ARRAY[
        'New York',
        'Los Angeles',
        'Chicago',
        'London',
        'Singapore',
        'Chennai',
        'Bangalore',
        'Mumbai'
    ];
BEGIN
    FOR i IN 1..100 LOOP
        INSERT INTO customer (name, age, city)
        VALUES (
            'Customer_' || i,
            FLOOR(RANDOM() * 43 + 18)::INT,
            cities[FLOOR(RANDOM() * array_length(cities, 1) + 1)::INT]
        );
    END LOOP;
END $$;

-- Verify the records
SELECT * FROM customer ORDER BY id; 