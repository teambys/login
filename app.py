from flask import Flask, request, render_template_string, redirect, url_for, flash, send_file
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random key for session management

# Directory to store responses
RESPONSES_DIR = 'responses'
os.makedirs(RESPONSES_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract data from the form
        user_email = request.form.get('user_email')
        user_pass = request.form.get('user_pass')

        # URL to send the request to
        url = 'https://golperjhuri.com/login.php'
        
        # Data to be sent in the POST request
        data = {
            'user_email': user_email,
            'user_pass': user_pass,
            'remamber': 'on'
        }

        # Sending the POST request
        response = requests.post(url, data=data)

        # Save the response
        response_file = os.path.join(RESPONSES_DIR, f'response_{user_email}.html')
        with open(response_file, 'w', encoding='utf-8') as file:
            file.write(response.text)

        flash('Login successful! Response saved.')
        return redirect(url_for('view_responses'))

    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; }
        h1 { color: #333; }
        form { max-width: 400px; margin: 0 auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        label { display: block; margin-bottom: 8px; margin-top: 12px; }
        input[type="email"], input[type="password"] { width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 4px; }
        button { background-color: #5cb85c; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #4cae4c; }
        a { display: block; text-align: center; margin-top: 20px; color: #5cb85c; text-decoration: none; }
    </style>
</head>
<body>
    <h1>Login</h1>
    <form method="post">
        <label for="user_email">Email:</label>
        <input type="email" id="user_email" name="user_email" required>
        <label for="user_pass">Password:</label>
        <input type="password" id="user_pass" name="user_pass" required>
        <button type="submit">Submit</button>
    </form>
    <a href="{{ url_for('view_responses') }}">View Saved Responses</a>
</body>
</html>''')

@app.route('/responses')
def view_responses():
    # List files in the responses directory
    response_files = os.listdir(RESPONSES_DIR)
    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Saved Responses</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; }
        h1 { color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { background: #fff; margin: 10px 0; padding: 15px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        a { color: #5cb85c; text-decoration: none; }
    </style>
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
</html>''', files=response_files)

@app.route('/responses/<filename>')
def view_response_file(filename):
    # Serve the HTML content of the selected file directly
    file_path = os.path.join(RESPONSES_DIR, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

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
