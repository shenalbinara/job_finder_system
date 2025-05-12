from flask import Flask, render_template, request
from scraper import scrape_linkedin
import mysql.connector
from config import  get_db_connection

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_type = request.form.get('job_type')
        location = request.form.get('location')
        remote_status = request.form.get('remote_status')  # Get remote/physical status from form

        if not remote_status:
            remote_status = "Physical"  # Default value if not provided

        # Clear old results before inserting new ones
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM job_finder_table02")  # Deletes all previous records
        conn.commit()
        cursor.close()
        conn.close()

        scrape_linkedin(job_type, location, remote_status)  # Ensure 3 arguments are passed

    return render_template('index.html')


@app.route("/dashboard")
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM job_finder_table02")
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("dashboard.html", jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True)
