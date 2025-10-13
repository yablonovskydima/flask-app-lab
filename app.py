from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def aboutme():
    return render_template('aboutme.html', title="About Me")

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Контакти")

@app.route('/services')
def services():
    return render_template('services.html', title="Контакти")

@app.route('/projects')
def projects():
    return render_template('projects.html', title="Контакти")

if __name__ == '__main__':
    app.run(debug=True)
