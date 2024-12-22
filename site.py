import psycopg2
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


DB_HOST = ''
DB_NAME = ''
DB_USER = ''
DB_PASS = ''


def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)



@app.route("/")
def index():
    user_id = request.args.get('user_id', type=int)
    print(user_id)
    if user_id is None:
        return "User ID is required", 400
    click_count = 0
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT \"score\" FROM \"score\" WHERE \"ID_user\" = %s", (user_id,))
            result = cursor.fetchone()

            if result is None:
                cursor.execute("INSERT INTO \"score\" (\"ID_user\", \"score\") VALUES (%s, %s)", (user_id, 1))
                click_count = 1
            else:
                click_count = result[0]
    return render_template("index.html", click_count=click_count)

@app.route('/clicker', methods=['post'])
def clicker():
    update = None
    context = None
    user_id = request.args.get('user_id', type=int)
    #click_count = request.form.get('score')
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT \"score\" FROM \"score\" WHERE \"ID_user\" = %s", (user_id,))
            result = cursor.fetchone()

            if result is None:
                cursor.execute("INSERT INTO \"score\" (\"ID_user\", \"score\") VALUES (%s, %s)", (user_id, 1))
                click_count = 1
            else:
                click_count = result[0] + 1
                cursor.execute("UPDATE score SET \"score\" = %s WHERE \"ID_user\" = %s", (click_count, user_id))

            conn.commit()
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True, port=5001)