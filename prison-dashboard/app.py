from flask import Flask, render_template, jsonify, request
import mysql.connector

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sleepyd2004!",
        database="prison"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def run_query():
    queries = request.json.get('query')
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        results = []
        for query in queries.split(';'):
            q = query.strip()
            if not q:
                continue
            cursor.execute(q)
            if q.lower().startswith("select"):
                results.append(cursor.fetchall())
            else:
                conn.commit()
                results.append(f"{cursor.rowcount} row(s) affected.")

        return jsonify({"success": True, "data": results})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
