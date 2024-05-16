import pandas as pd
import re
import os

# Load the CSV files as text
print("Loading CSV files...")
with open('test_for_richard1.csv', 'r') as file1, open('test_for_richard2.csv', 'r') as file2:
    content1 = file1.read()
    content2 = file2.read()
print("CSV files loaded.")

# Combine the content of the two files
print("Combining CSV files...")
combined_content = content1 + '\n' + content2
print("CSV files combined.")

print("Saving combined CSV to file...")
with open('combined_csv.csv', 'w') as f:
    f.write(combined_content)
print("Combined CSV saved to 'combined_csv.csv'.")

# Split content into lines
lines = combined_content.split('\n')

# Process multi-line content and extract relevant lines
def process_multiline_entries(lines):
    combined_lines = []
    current_feature = None
    current_increment = None
    current_lines = []
    
    for line in lines:
        if 'FEATURE' in line:
            if current_feature or current_increment:
                combined_lines.append([current_feature, current_increment, '\n'.join(current_lines)])
            current_feature = line
            current_increment = None
            current_lines = []
        elif 'INCREMENT' in line:
            if current_feature or current_increment:
                combined_lines.append([current_feature, current_increment, '\n'.join(current_lines)])
            current_increment = line
            current_feature = None
            current_lines = []
        else:
            current_lines.append(line)
    
    # Add the last set
    if current_feature or current_increment:
        combined_lines.append([current_feature, current_increment, '\n'.join(current_lines)])
    
    return pd.DataFrame(combined_lines, columns=['FEATURE', 'INCREMENT', 'DETAILS'])

df_processed = process_multiline_entries(lines)

# Define a function to extract the expiration dates from the DETAILS column
def extract_expiration_dates(details):
    if pd.isna(details):
        return None
    details = str(details)  # Convert content to string
    matches = re.findall(r'ISSUED\s*=\s*(\d{2}-[a-zA-Z]{3}-\d{4})', details)
    return matches if matches else None

# Apply the function to each row in the dataframe
print("Applying function to each row...")
df_processed['EXPIRATION_DATE'] = df_processed.apply(lambda row: extract_expiration_dates(row['DETAILS']) if pd.notna(row['FEATURE']) else None, axis=1)
df_processed['INCREMENT_EXPIRATION_DATE'] = df_processed.apply(lambda row: extract_expiration_dates(row['DETAILS']) if pd.notna(row['INCREMENT']) else None, axis=1)
print("Function applied to each row.")

# Forward fill the 'FEATURE' and 'INCREMENT' columns
print("Forward filling 'FEATURE' and 'INCREMENT' columns...")
df_processed['FEATURE'] = df_processed['FEATURE'].fillna(method='ffill')
df_processed['INCREMENT'] = df_processed['INCREMENT'].fillna(method='ffill')

# Only drop rows where both 'FEATURE' and 'INCREMENT' are NaN
print("Cleaning dataframe...")
df_processed = df_processed.dropna(subset=['FEATURE', 'INCREMENT'], how='all')
print("Dataframe cleaned.")

# Save the dataframe to a CSV file
print("Saving dataframe to CSV file...")
df_processed.to_csv('output.csv', index=False)
print("Dataframe saved to CSV file.")

# Save the cleaned dataframe to a new CSV file
print("Saving cleaned dataframe to a new CSV file...")
df_processed[['FEATURE', 'EXPIRATION_DATE', 'INCREMENT', 'INCREMENT_EXPIRATION_DATE']].to_csv('FINAL.csv', index=False)
print("Dataframe saved to 'FINAL.csv' file.")

# Display the desired columns
print("Displaying desired columns...")
print(df_processed[['FEATURE', 'EXPIRATION_DATE', 'INCREMENT', 'INCREMENT_EXPIRATION_DATE']])

# Load the FINAL.csv file
df = pd.read_csv('FINAL.csv')

# Function to clean the FEATURE and INCREMENT columns
def clean_column(entry):
    if pd.isna(entry):
        return None
    parts = entry.split()
    return parts[1] if len(parts) > 1 else None

# Apply the function to FEATURE and INCREMENT columns
df['FEATURE'] = df['FEATURE'].apply(clean_column)
df['INCREMENT'] = df['INCREMENT'].apply(clean_column)

# Remove empty rows
df.dropna(how='all', inplace=True)

# Shift all non-empty values up within each column to fill gaps
df = df.apply(lambda x: pd.Series(x.dropna().values))

# Reset the index after shifting values
df.reset_index(drop=True, inplace=True)

# Save the cleaned dataframe to a new CSV file
cleaned_file_path = 'CLEANED_FINAL.csv'
df.to_csv(cleaned_file_path, index=False)

# Remove the 'output.csv' file
if os.path.exists('output.csv'):
    os.remove('output.csv')
    print("Removed 'output.csv' file.")

# Remove the 'FINAL.csv' file
if os.path.exists('FINAL.csv'):
    os.remove('FINAL.csv')
    print("Removed 'FINAL.csv' file.")

# Remove the 'combined_csv.csv' file
if os.path.exists('combined_csv.csv'):
    os.remove('combined_csv.csv')
    print("Removed 'combined_csv.csv' file.")

# Display the cleaned dataframe
print(df.head(10))
print("Cleaned dataframe saved to 'CLEANED_FINAL.csv' file.")


#---------------------------------------------------------------------

import pandas as pd
from datetime import datetime

# Load the cleaned CSV file
df = pd.read_csv('CLEANED_FINAL.csv')

# Function to convert date format from DD-MMM-YYYY to YYYY-MM-DD
def convert_date_format(date_str):
    if pd.isna(date_str):
        return None
    try:
        return datetime.strptime(date_str, '%d-%b-%Y').strftime('%Y-%m-%d')
    except ValueError:
        return None

# Apply the conversion function to the date columns, handling NaN values
df['EXPIRATION_DATE'] = df['EXPIRATION_DATE'].apply(lambda x: convert_date_format(str(x).strip("[]").replace("'", "")) if pd.notna(x) else None)
df['INCREMENT_EXPIRATION_DATE'] = df['INCREMENT_EXPIRATION_DATE'].apply(lambda x: convert_date_format(str(x).strip("[]").replace("'", "")) if pd.notna(x) else None)

# Define a function to generate SQL insert statements without specifying the primary key
def generate_sql_insert(df):
    sql_queries = []
    for index, row in df.iterrows():
        expiration_date = f"'{row['EXPIRATION_DATE']}'" if row['EXPIRATION_DATE'] else 'NULL'
        sql_query = f"""
        INSERT INTO ramt_license_usage (
            retrieval_time, user_name, host_name, licenses_used_by_user,
            is_reservation, licenses_total, licenses_total_in_use, feature_name, feature_version,
            daemon_name, server_master_port, server_master_host, server_port, server_host,
            expiration_date
        ) VALUES (
            NOW(), 'user_{index}', 'host_{index}', '{row['FEATURE']}',
            'NO', '10', '5', '{row['INCREMENT']}', '1.0',
            'daemon_{index}', '1234', 'master_host_{index}', '5678', 'host_{index}',
            {expiration_date}
        );
        """
        sql_queries.append(sql_query)
    return sql_queries

# Generate the SQL queries
sql_queries = generate_sql_insert(df)

# Write the SQL queries to a file
with open('insert_queries.sql', 'w') as f:
    for query in sql_queries:
        f.write(query + '\n')

print("SQL insert queries have been saved to 'insert_queries.sql'")