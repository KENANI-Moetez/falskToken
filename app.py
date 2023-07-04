from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulated user database (replace with your own user retrieval logic)
users = {'user1': {'password': 'password1'},
         'user2': {'password': 'password2'}}


@app.route('/')
def home():
    return 'Welcome to the home page!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and password == users[username]['password']:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password'

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    return 'Welcome to the dashboard!'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
