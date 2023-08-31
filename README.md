# teamviewer_assessment
Technical assessment for team viewer

The solutions are as below:

1. SQL incremental updates. This is present inside sql_solutions directory.
Description:
    * The update works based on changes in the product price
    * It compares the price in products_raw table with the products table
    * Only in case of the change the products table is updated.
    * The historical table products_history is created. The columns required are added in the Create statement.
    * The history table maintains all the pricing history of the products.
    * At any point of time we can see the valid price of a product with from_day_id and to_day_id as valid period
    * The latest entry or the current price of the product will have an infinite to_day_id of 99991231
    * I have removed the product name from the history table to remove redundancy.
    * Suggestion: It can also be removed from the products table too. There can be a product details table with this information.

2. Data Ingestion. This is included inside the freshdesk directory.
Description:
    * The ingestion from the Freshdesk API can be done using Python.
    * The code to perform the task has been segregated into config, download and util sections.
    * The config part serves as the part to segregate the sensitive information from the main application.
    * Any change to the API key or credentials will not trigger any changes to the application.
    * Any further API integrations can also use the config or even other Freshdesk integrations can utilise the same config.
    * There is a util functionality provided to write file to a destination file path and check if it exists or not.
    * The util also serves as a central tool which can be utilised by other applications.
    * The download part is split in 2 parts: one is requesting the API based on the credentials from config and the other is downloading the report or the ticket information.
    * The download that writes the csv files also zips the file and also adds a date to segregate all the files.
    * The download is called with a main function and it can also include other micro apps.
    * The entire process can be triggered using Airflow at a defined interval.
    * The downloaded csv can be integrated into the data warehouse with Python writing into Postgres.

3. SQL Debugging : Issue with the edition values
Description: 
    * The 2nd and 3rd CASE statements both considers similar attributes ('Remote Management', 'Pilot'). So, if there is a overlap in a.item_group_id and a.nal_category then there will wrong values
    * The 4th CASE statement has a Boolean filter (A.is_main_item) but its value True or False is not specified. This can also give wrong results.
    * There are again overlaps in the next CASE statements so if the oal_product_group is present in other criteria then also it will be wrong here.
    * THE CTE SQL with window_product will not give correct results as it operates max(oal_product_group). The max function on a VARCHAR column will not give correct data.
    * The same issue is with the CTE SQL for window_product_two and window_product_three. The max(oal_product_group) will give wrong results.
    * The CTE SQL with contract_core_product the max(product_order) has no affect on the outcome. If not needed it can be removed.
    * To fix the issues, the CTE SQL needs to be re-written to get the latest data and not using max on a VARCHAR column. Rather it should use a date or an integer column to get the latest product group.
    * The overlapping cases can be improved by writing a subquery that considers all conditions and not ignores the overlapping values.

