import psycopg2
import csv

conn_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

def connect():
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
                next(reader)
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

def insert_from_console():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            first_name = input("Enter first name: ")
            last_name = input("Enter last name (optional, press Enter to skip): ")
            phone = input("Enter phone number: ")
            cur.execute(
                "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s) ON CONFLICT (phone) DO NOTHING",
                (first_name, last_name or None, phone)
            )
            conn.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error inserting from console: {e}")
        finally:
            cur.close()
            conn.close()

def update_data():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            phone = input("Enter phone number to update: ")
            cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
            if cur.fetchone():
                field = input("What to update? (first_name/phone): ").lower()
                if field == "first_name":
                    new_value = input("Enter new first name: ")
                    cur.execute("UPDATE phonebook SET first_name = %s WHERE phone = %s", (new_value, phone))
                elif field == "phone":
                    new_value = input("Enter new phone number: ")
                    cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (new_value, phone))
                else:
                    print("Invalid field.")
                    return
                conn.commit()
                print("Data updated successfully.")
            else:
                print("Phone number not found.")
        except Exception as e:
            print(f"Error updating data: {e}")
        finally:
            cur.close()
            conn.close()

def query_data():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            print("Query options: 1) All contacts, 2) By first name, 3) By phone")
            choice = input("Choose option (1-3): ")
            if choice == "1":
                cur.execute("SELECT * FROM phonebook ORDER BY first_name")
            elif choice == "2":
                first_name = input("Enter first name to search: ")
                cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"%{first_name}%",))
            elif choice == "3":
                phone = input("Enter phone number to search: ")
                cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
            else:
                print("Invalid choice.")
                return
            rows = cur.fetchall()
            if rows:
                for row in rows:
                    print(f"ID: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Phone: {row[3]}")
            else:
                print("No results found.")
        except Exception as e:
            print(f"Error querying data: {e}")
        finally:
            cur.close()
            conn.close()

def delete_data():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            field = input("Delete by (username/phone): ").lower()
            if field == "username":
                first_name = input("Enter first name: ")
                cur.execute("DELETE FROM phonebook WHERE first_name = %s", (first_name,))
            elif field == "phone":
                phone = input("Enter phone number: ")
                cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
            else:
                print("Invalid field.")
                return
            if cur.rowcount > 0:
                conn.commit()
                print("Data deleted successfully.")
            else:
                print("No matching records found.")
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
        print("2. Insert from console")
        print("3. Update data")
        print("4. Query data")
        print("5. Delete data")
        print("6. Exit")
        choice = input("Choose an option (1-6): ")
        if choice == "1":
            file_path = input("Enter CSV file path: ")
            insert_from_csv(file_path)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_data()
        elif choice == "4":
            query_data()
        elif choice == "5":
            delete_data()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()