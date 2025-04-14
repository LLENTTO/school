import psycopg2
import csv

# Database connection configuration
conn_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "your_password",  # Replace with your PostgreSQL password
    "host": "localhost",
    "port": "5432"
}

def connect():
    """Connect to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**conn_params)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50),
                    phone VARCHAR(15) NOT NULL UNIQUE
                );
            """)
            conn.commit()
            print("Table created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            cur.close()
            conn.close()

def insert_from_csv(file_path):
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    cur.execute(
                        "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s) ON CONFLICT (phone) DO NOTHING",
                        (row[0], row[1] if row[1] else None, row[2])
                    )
            conn.commit()
            print("Data inserted from CSV successfully.")
        except Exception as e:
            print(f"Error inserting from CSV: {e}")
        finally:
            cur.close()
            conn.close()

def insert_or_update_user():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            first_name = input("Enter first name: ")
            phone = input("Enter phone number: ")
            cur.execute("CALL insert_or_update_user(%s, %s)", (first_name, phone))
            conn.commit()
            print("User inserted or updated successfully.")
        except Exception as e:
            print(f"Error inserting/updating user: {e}")
        finally:
            cur.close()
            conn.close()

def insert_multiple_users():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            print("Enter names and phones (e.g., 'John,1234567890;Jane,0987654321')")
            input_str = input("Input: ")
            pairs = input_str.split(";")
            names = []
            phones = []
            for pair in pairs:
                if pair:
                    name, phone = pair.split(",")
                    names.append(name.strip())
                    phones.append(phone.strip())
            
            cur.execute("CALL insert_multiple_users(%s, %s, NULL)", (names, phones))
            invalid_data = cur.fetchone()[0] if cur.rowcount > 0 else []
            conn.commit()
            print("Users processed.")
            if invalid_data:
                print("Invalid data:", invalid_data)
            else:
                print("All data valid.")
        except Exception as e:
            print(f"Error inserting multiple users: {e}")
        finally:
            cur.close()
            conn.close()

def search_by_pattern():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            pattern = input("Enter search pattern (part of name or phone): ")
            cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
            rows = cur.fetchall()
            if rows:
                for row in rows:
                    print(f"ID: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Phone: {row[3]}")
            else:
                print("No results found.")
        except Exception as e:
            print(f"Error searching data: {e}")
        finally:
            cur.close()
            conn.close()

def query_paginated():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            limit = int(input("Enter number of records per page: "))
            page = int(input("Enter page number (1-based): "))
            offset = (page - 1) * limit
            cur.execute("SELECT * FROM get_phonebook_paginated(%s, %s)", (limit, offset))
            rows = cur.fetchall()
            if rows:
                for row in rows:
                    print(f"ID: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Phone: {row[3]}")
            else:
                print("No results found.")
        except Exception as e:
            print(f"Error querying paginated data: {e}")
        finally:
            cur.close()
            conn.close()

def delete_data():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            field = input("Delete by (username/phone): ").lower()
            if field not in ["username", "phone"]:
                print("Invalid field.")
                return
            value = input(f"Enter {field}: ")
            cur.execute("CALL delete_phonebook_entry(%s, %s)", (field, value))
            conn.commit()
            print("Data deleted successfully (or no matching records found).")
        except Exception as e:
            print(f"Error deleting data: {e}")
        finally:
            cur.close()
            conn.close()

def main():
    create_table()
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from CSV")
        print("2. Insert or update user")
        print("3. Insert multiple users")
        print("4. Search by pattern")
        print("5. Query paginated")
        print("6. Delete data")
        print("7. Exit")
        choice = input("Choose an option (1-7): ")
        if choice == "1":
            file_path = input("Enter CSV file path: ")
            insert_from_csv(file_path)
        elif choice == "2":
            insert_or_update_user()
        elif choice == "3":
            insert_multiple_users()
        elif choice == "4":
            search_by_pattern()
        elif choice == "5":
            query_paginated()
        elif choice == "6":
            delete_data()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()