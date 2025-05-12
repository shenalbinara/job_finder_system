import mysql.connector


def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="cloudslt@123",
            database="job_finder_database"  # Make sure this is your actual database name
        )
        if conn.is_connected():
            print("Database connection successful!")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def insert_job(job_title, location, remote_status, contact, job_type):
    # Ensure job_type does not exceed 100 characters
    if len(job_type) > 100:
        job_type = job_type[:100]  # Truncate to fit in the database

    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database. Job not inserted.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO job_finder_table02 (job_title, location, remote_status, contact, job_type) VALUES (%s, %s, %s, %s, %s)",
            (job_title, location, remote_status, contact, job_type))
        conn.commit()
        print("Job inserted successfully!")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        cursor.close()
        conn.close()


# Test connection
if __name__ == "__main__":
    get_db_connection()
