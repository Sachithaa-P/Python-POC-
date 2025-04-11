import mysql.connector
import os
from poc2exception import (
    InvalidFileNameException,
    RestrictedSQLCommandException,
    DuplicateEntryException,
    DataTypeMismatchException
)  # Importing custom exceptions

# Establish database connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="my_database"
)
cursor = connection.cursor()
print("Connected to the database.")

# Default folder path
DEFAULT_FOLDER = r"C:\Users\s.paranidharan\OneDrive - Perficient, Inc\internship\POC1"  # Change this to your desired folder path

# Function to create a table
def create_table(json_data):
    try:
        table_name = json_data['table_name']
        columns = json_data['columns']
        column_definitions = ", ".join([f"{col['name']} {col['type']}" for col in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});"
        cursor.execute(query)
        connection.commit()
        print(f"Table '{table_name}' created successfully.")
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")

# Function to run multiple SQL queries and save output
def run_query_with_exceptions(query, file_name):
    error_occurred = False  # Flag to track errors

    try:
        # Custom Exception Handling
        if not file_name.strip() or any(c in file_name for c in r'\/:*?"<>|@!'):
            raise InvalidFileNameException("Invalid file name. Please enter a valid file name without special characters.")

        if "drop" in query.lower() or "truncate" in query.lower():
            raise RestrictedSQLCommandException("DROP and TRUNCATE commands are not allowed for security reasons.")

        os.makedirs(DEFAULT_FOLDER, exist_ok=True)
        file_path = os.path.join(DEFAULT_FOLDER, file_name)
        error_file_path = os.path.join(DEFAULT_FOLDER, "error.txt")

        queries = [q.strip() for q in query.split(";") if q.strip()]

        for q in queries:
            try:
                cursor.execute(q)
                if q.lower().startswith("select"):
                    results = cursor.fetchall()
                    with open(file_path, "a") as file:
                        if results:
                            for row in results:
                                file.write(", ".join(map(str, row)) + "\n")
                        else:
                            file.write(f"No results found for query: {q}\n")
                else:
                    connection.commit()
                    with open(file_path, "a") as file:
                        file.write(f"Query executed successfully: {q}\n")

            except mysql.connector.Error as query_error:
                error_occurred = True

                if "Duplicate entry" in str(query_error):
                    raise DuplicateEntryException(f"Error: Duplicate entry detected. {query_error}")

                if "Incorrect" in str(query_error) and "value" in str(query_error):
                    raise DataTypeMismatchException(f"Error: Data type mismatch. {query_error}")

                with open(error_file_path, "a") as error_file:
                    error_file.write(f"Error: {query_error}\nInvalid SQL Command: {q}\n\n")
                print(f"An error occurred. Check {error_file_path}.")
                break  # Stop execution on first error

        if error_occurred:
            if os.path.exists(file_path):  # Delete user-specified file if created
                os.remove(file_path)
        else:
            print(f"All queries executed. Results saved to: {file_path}")

    except (InvalidFileNameException, RestrictedSQLCommandException,
            DuplicateEntryException, DataTypeMismatchException) as e:
        print(str(e))
    except Exception as e:
        error_file_path = os.path.join(DEFAULT_FOLDER, "error.txt")
        with open(error_file_path, "a") as error_file:
            error_file.write(f"Error: {e}\nInvalid SQL Command: {query}\n\n")
        print(f"An unexpected error occurred. Details saved in: {error_file_path}")

# Example usage
table_json = {
    "table_name": "students",
    "columns": [
        {"name": "id", "type": "INT PRIMARY KEY AUTO_INCREMENT"},
        {"name": "name", "type": "VARCHAR(100)"},
        {"name": "age", "type": "INT"},
        {"name": "grade", "type": "VARCHAR(10)"}
    ]
}

# Create a table
create_table(table_json)

# Perform CRUD operations
# Create
run_query_with_exceptions(
    "INSERT INTO students (name, age, grade) VALUES ('SACH', 20, 'A');"
    "INSERT INTO students (name, age, grade) VALUES ('Messi', 26, 'B');"
    "INSERT INTO students (name, age, grade) VALUES ('Ney', 22, 'C');",
    "insert_output.txt"
)
# Read
run_query_with_exceptions("SELECT * FROM students;", "select_output.txt")
# Update
run_query_with_exceptions("UPDATE students SET grade = 'A+' WHERE name = 'SACH';", "update_output.txt")
# Delete
run_query_with_exceptions("DELETE FROM students WHERE name = 'Ney';", "delete_output.txt")

# Main loop for console-based interaction
def console_input():
    while True:
        query = input("Enter SQL Query (or type 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            print("Exiting the program.")
            break

        file_name = input("Enter the output file name (e.g., result.txt): ").strip()

        if not file_name:
            print("Error: Please provide an output file name.")
            continue

        run_query_with_exceptions(query, file_name)

# Start the console input loop
console_input()

# Close the cursor and connection after closing the program
cursor.close()
connection.close()
print("Connection closed.")
