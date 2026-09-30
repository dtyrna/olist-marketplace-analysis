# Silver-Layer Data Cleaning

## Tables and Columns

### `order_payments`

- `order_id`: Unique identifier of the order
- `payment_sequential`: Payment sequence within an order when multiple payment methods are used
- `payment_type`: Payment method used by the customer
- `payment_installments`: Number of selected payment installments
- `payment_value`: Value of the respective payment

### `products`

- `product_id`: Unique identifier of the product
- `product_category_name`: Product category in Portuguese
- `product_name_lenght`: Number of characters in the product name
- `product_description_lenght`: Number of characters in the product description
- `product_photos_qty`: Number of published product photos
- `product_weight_g`: Product weight in grams
- `product_length_cm`: Product length in centimeters
- `product_height_cm`: Product height in centimeters
- `product_width_cm`: Product width in centimeters

### `sellers`

- `seller_id`: Unique identifier of the seller
- `seller_zip_code_prefix`: Five-digit postal code prefix of the seller location
- `seller_city`: City of the seller location
- `seller_state`: Two-character code of the Brazilian state

## Data Source and Target Layer

- Load Pickle tables locally for testing purposes in the Jupyter Notebook only
- Load Bronze tables from an AWS S3 bucket in the final Python script
- Process the tables from the Bronze Layer into the Silver Layer
- Use DataFrames to process the individual tables
- Export the cleaned tables for further processing in the data warehouse

## General Cleaning Conventions

- Define numeric and string columns explicitly before processing
- Convert numeric columns with `pd.to_numeric(..., errors="raise")`
- Raise an error and stop processing when numeric values cannot be converted
- Convert string columns with `astype(str)`
- Print conversion errors and stop the script when type conversion fails
- Make each transformation traceable through status messages or validation checks
- Include the affected table and column in every error message
- Check null values at column or row level before deciding to remove records
- Do not remove records automatically because individual attributes are missing
- Remove rows without usable data
- Check business keys for missing values and duplicates
- Stop processing when duplicate business keys are detected
- Create technical keys only after all row-removing cleaning steps are complete
- Sort columns alphabetically after all transformations

## Standard Cleaning for Multiple Tables

### Standardize Data Types

- `order_payments`: Convert `payment_sequential`, `payment_installments` and `payment_value` to numeric types
- `order_payments`: Convert `order_id` and `payment_type` to strings
- `products`: Convert lengths, quantities, weight and dimensions to numeric types
- `products`: Convert `product_id` and `product_category_name` to strings
- `sellers`: Convert `seller_id`, `seller_zip_code_prefix`, `seller_city` and `seller_state` to strings

### Validate Business Keys

- `products`: Check that every row contains a `product_id`
- `products`: Check that `product_id` is unique
- `sellers`: Check that every row contains a `seller_id`
- `sellers`: Check that `seller_id` is unique
- Print affected records when business keys are missing or duplicated
- Stop the script after printing invalid key values
- Use `order_id` as the business reference to the order in `order_payments`

### Handle Empty Records

- Check all non-key columns for completely missing values
- Remove rows without usable data
- Keep rows with an existing key and partially missing attributes
- Print the number of detected and removed fully empty rows
- Print the columns used for the empty-row check
- `products`: Remove a record that contained only a `product_id`
- `sellers`: No fully empty records were detected

### Create Technical Keys

- `order_payments`: Create `id_order_payments`
- `products`: Create `id_products`
- `sellers`: Create `id_sellers`
- Start each technical key at `1`
- Create technical keys only after all row-removing cleaning steps
- Validate the minimum and maximum value of each generated key
- Validate that the number of key values matches the number of DataFrame rows

## Specific Cleaning of `order_payments`

- Determine the available values in `payment_type`
- Print payment-type frequencies before cleaning
- Remove rows with `payment_type = "not_defined"`
- Print the number of removed rows with an undefined payment type
- Check that `not_defined` no longer exists after cleaning
- Validate the values in `payment_value`
- Remove rows with `payment_value = 0.0`
- Print the number of removed rows without a positive payment value
- Check that no further `0.0` values remain after cleaning
- Create `id_order_payments` only after these cleaning steps

## Specific Cleaning of `products`

- Check `product_id` before removing empty records
- Check whether multiple categories are combined in `product_category_name`
- Check the separators defined in the script
- Print affected product IDs when multiple categories are detected
- No multiple categories were detected in `product_category_name`
- Determine null values in `product_category_name`, `product_description_lenght` and `product_photos_qty`
- Keep products with a missing category, description length or photo count when other product data is available
- Check null values in `product_weight_g`, `product_length_cm`, `product_height_cm` and `product_width_cm`
- Keep products with partially missing size or weight data
- Identify products without values in any size attribute separately
- Do not remove a product automatically only because size attributes are missing
- Create `id_products` after all validations and row-removing steps

## Specific Cleaning of `sellers`

### Standardize City Names

- Use `unidecode` to remove diacritical marks
- Print city names containing special characters before standardization
- Convert city names to a simplified Latin-character representation
- Check whether non-standard characters remain after conversion
- Check for additional location or regional information in `seller_city`
- For comma-separated values, keep the text before the first comma
- For other defined separators, keep the text before the respective separator
- Remove leading and trailing whitespace after splitting values
- Print affected city names before cleaning
- Check city names for remaining separators after cleaning

### Standardize State Codes

- Determine all unique values in `seller_state`
- Check every state code for exactly two characters
- Check for leading or trailing whitespace
- Check capitalization
- Print every state code that does not follow the expected format
- Convert state codes to lowercase
- Remove whitespace before format validation
- Check that only two-character codes remain after correction
- Store state codes, for example, as `sp`, `rj` or `mg`

### Validate Postal Code Prefixes

- Analyze frequencies of `seller_zip_code_prefix`
- Print the minimum and maximum number of sellers per postal code prefix
- Keep `seller_zip_code_prefix` as a string
- Prevent loss of leading zeros through numeric conversion
- Validate the minimum and maximum length of postal code prefixes

## Controls for Athena Tables

- Determine the data type of every final column after cleaning
- Determine the minimum and maximum value of every numeric column
- Determine the minimum and maximum character length of every string column
- Store these metrics as the basis for defining Athena columns
- Use the maximum observed character length to restrict the allowed string length in Athena
- Use the observed value ranges to validate numeric Athena columns
- Check that Athena data types match the final Pandas data types
- Check that Athena string lengths can accommodate all cleaned values
- Print the table, column, data type, minimum value and maximum value for troubleshooting
- Print the table, column, minimum string length and maximum string length for troubleshooting
- Use these controls to investigate errors during Athena table creation or CSV loading

## Final Validation and Troubleshooting

- Print the name of the table before each cleaning step
- Include the name of the affected column in conversion errors
- Print row counts before and after every row-removing step
- Print the number of removed records for each removal reason
- Check whether an expected cleaning rule actually changed the data
- Check whether invalid values remain after cleaning
- Print final column names and data types for each table
- Print the final row count for each table
- Print the generated technical keys for each table
- Export data only after all data-quality checks have completed successfully
- Use distinct error messages for the table, column, validation rule and affected value

The local Pickle files are used exclusively as test input in the Notebook. The production process must load the Bronze tables from the AWS S3 bucket. The data types, value ranges and string lengths determined during the Notebook-based validation also provide the basis for the subsequent Athena table definitions.
