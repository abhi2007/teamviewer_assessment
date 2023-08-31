CREATE TABLE products_history (
    id           INTEGER       NOT NULL,
    productprice NUMERIC(4, 2) NOT NULL,
    from_day_id  INTEGER       NOT NULL,
    to_day_id    INTEGER       NOT NULL
);

INSERT INTO products_history

SELECT
    hst.id,
    hst.productprice,
    -- make the updated day as the product day
    hst.updated_day_id                             AS from_day_id,
    -- generate a to_day field upto which the price of the product is valid
    coalesce(lead(hst.updated_day_id)
             OVER (PARTITION BY hst.id), 99991231) AS to_day_id
FROM (SELECT
          id,
          productprice,
          coalesce(lag(productprice)
                   OVER (PARTITION BY id ORDER BY updatedat), 0) AS previous_price,
          -- cast it to integer to generate a day_id attribute
          to_char(updatedat, 'YYYYMMDD') :: INTEGER              AS updated_day_id
      FROM products_raw
     ) hst
    -- check for existing history
    LEFT JOIN products_history hst_data
              ON hst_data.id = hst.id
                  AND hst_data.from_day_id = hst.updated_day_id
    -- INSERT into history only when the current price is different from the previous price
WHERE hst.productprice <> hst.previous_price
  -- Insert only when history is not present
  AND hst_data.id IS NULL;


-- Add indexes
CREATE UNIQUE INDEX products_history__id_from_day__unique ON products_history(id, productprice,from_day_id);
ANALYZE products_history;