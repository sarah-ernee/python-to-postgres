import random
import string

# Function to generate mock data for different data types
def generate_mock_data(data_type):
    if data_type == 'integer':
        return str(random.randint(1, 100))
    elif data_type == 'text':
        return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
    elif data_type == 'date':
        return f"'{random.randint(2000, 2022)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'"
    # Add more data types as needed

# Define table schema and columns
table_name = 'example_table'
columns = {
    'id': 'SERIAL PRIMARY KEY',
    'name': 'TEXT',
    'age': 'INTEGER',
    'birthdate': 'DATE'
    # Add more columns with their data types
}

# Generate SQL query to create table
create_table_query = f'CREATE TABLE {table_name} ('
for column, data_type in columns.items():
    create_table_query += f'{column} {data_type}, '
create_table_query = create_table_query[:-2] + ');'

print("SQL Query to Create Table:")
print(create_table_query)

# Generate SQL queries to insert mock data
insert_queries = []
num_records_to_insert = 10
for _ in range(num_records_to_insert):
    insert_query = f"INSERT INTO {table_name} ("
    for column in columns.keys():
        insert_query += f"{column}, "
    insert_query = insert_query[:-2] + ") VALUES ("
    for data_type in columns.values():
        insert_query += f"{generate_mock_data(data_type)}, "
    insert_query = insert_query[:-2] + ");"
    insert_queries.append(insert_query)

print("\nSQL Queries to Insert Mock Data:")
for query in insert_queries:
    print(query)



'''
DO $$ 
DECLARE 
    user_name TEXT;
    table_rec RECORD;
    users TEXT[] := ARRAY['sarah', 'marcus', 'hanfai'];
BEGIN 
    FOREACH user_name IN ARRAY users
    LOOP
        FOR table_rec IN 
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        LOOP 
            EXECUTE 'GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER, ALTER ON TABLE ' || quote_ident(table_rec.table_name) || ' TO ' || quote_ident(user_name);
            EXECUTE 'GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO ' || quote_ident(user_name);
        END LOOP; 
    END LOOP; 
END $$;
'''