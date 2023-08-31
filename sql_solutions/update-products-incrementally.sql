-- Update the products table based on products_raw
-- Update only when new records are present based on changes in the product price
UPDATE products prd
SET
    productprice = new_price.productprice,
    updatedat = new_price.updatedat
    FROM (SELECT
          lat_raw_prd.id,
          lat_raw_prd.productprice,
          lat_raw_prd.updatedat
      FROM (SELECT
                id,
                productname,
                productprice,
                updatedat,
                -- Get the latest product data from the products_raw table
                row_number()
                OVER (PARTITION BY id ORDER BY updatedat DESC) AS prd_rank
            FROM products_raw
           ) lat_raw_prd
          JOIN products prd
               ON prd.id = lat_raw_prd.id
          -- Filters the data to the latest data for a product
      WHERE lat_raw_prd.prd_rank = 1
        -- Only get the product where the price changes
        -- It can also happen there is a decrease in product so get all price changes
        AND prd.productprice <> lat_raw_prd.productprice
     ) new_price
WHERE prd.id = new_price.id;