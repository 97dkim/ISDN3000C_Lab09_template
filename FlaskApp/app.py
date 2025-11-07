import sqlite3
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

# ------------------------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
# ------------------------------------------------------------------

@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        message = request.form.get('message', '').strip()

        if not name:
            flash('Name is required.', 'error')
        elif not message:
            flash('Message is required.', 'error')
        elif len(message) > 140:
            flash('Message must be 140 characters or fewer.', 'error')
        else:
            conn.execute(
                'INSERT INTO messages (name, message) VALUES (?, ?)',
                (name, message)
            )
            conn.commit()
            flash(f'Thanks, {name}! Your message was posted.', 'success')

        conn.close()
        return redirect(url_for('index'))

    messages = conn.execute(
        'SELECT * FROM messages ORDER BY created_at DESC'
    ).fetchall()
    conn.close()

    return render_template(
        'index.html',
        page_title='Guestbook Home',
        messages=messages
    )

# ------------------------------------------------------------------
# NEW: JSON API Endpoint
@app.route('/api/messages', methods=['POST'])
def add_message_api():
    # Ensure request is JSON
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'Request must be JSON'
        }), 400

    data = request.get_json()
    name = data.get('name')
    message = data.get('message')

    # Validation
    if not name or not name.strip():
        return jsonify({
            'status': 'error',
            'message': 'Name is required.'
        }), 400

    if not message or not message.strip():
        return jsonify({
            'status': 'error',
            'message': 'Message is required.'
        }), 400

    if len(message.strip()) > 140:
        return jsonify({
            'status': 'error',
            'message': 'Message must be 140 characters or fewer.'
        }), 400

    # Insert into DB
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO messages (name, message) VALUES (?, ?)',
            (name.strip(), message.strip())
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({
            'status': 'error',
            'message': 'Database error.'
        }), 500
    finally:
        conn.close()

    return jsonify({
        'status': 'success',
        'message': 'Message added!'
    }), 201
# ------------------------------------------------------------------

@app.route('/health')
def health_check():
    return 'Server is running!', 200

@app.route('/about')
def about():
    return 'This is a simple Flask guestbook application.'

if __name__ == '__main__':
    app.run(debug=True)