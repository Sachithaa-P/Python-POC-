import csv
import random
import string
import os


# Function to generate random data
def generate_random_value(data_type, length):
    if data_type == "INT":
        return random.randint(1, 10 ** length - 1)
    elif data_type == "VARCHAR":
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    elif data_type == "DATE":
        year = random.randint(2000, 2025)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # To keep it simple
        return f"{year}-{month:02d}-{day:02d}"
    else:
        return "Unknown"


# Function to read the metadata CSV file and generate random data
def generate_random_data(metadata_file, num_records, output_file):
    # Reading the metadata CSV file
    fields = []
    with open(metadata_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            fields.append(row)

    # Generating random data based on metadata
    data = []
    for _ in range(num_records):
        record = {}
        for field in fields:
            field_name = field["FieldName"]
            data_type = field["DataType"]
            length = int(field["Length"])
            record[field_name] = generate_random_value(data_type, length)
        data.append(record)

    # Writing the generated data to the output file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[field["FieldName"] for field in fields])
        writer.writeheader()
        writer.writerows(data)

    print(f"Generated {num_records} records and saved to {output_file}")


# Main function to interact with the user
def main():
    # user to upload a metadata CSV file
    metadata_file = input("Enter the path to your metadata CSV file: ")
    if not os.path.exists(metadata_file):
        print("File not found. Please check the file path.")
        return

    #user how many records they want
    try:
        num_records = int(input("How many records do you want to generate? "))
        if num_records <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a valid number for the records.")
        return

    # Default folder path to store the generated file
    DEFAULT_FOLDER = r"C:\Users\s.paranidharan\OneDrive - Perficient, Inc\internship\poc3\generated_data"
    os.makedirs(DEFAULT_FOLDER, exist_ok=True)

    # Define the output file path
    output_file = os.path.join(DEFAULT_FOLDER, "generated_data.csv")

    # Generate random data and save to the file
    generate_random_data(metadata_file, num_records, output_file)


if __name__ == "__main__":
    main()
