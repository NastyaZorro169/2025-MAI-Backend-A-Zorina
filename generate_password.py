from flask import Flask, render_template, request
import random
import string
import os

app = Flask(__name__, template_folder='public')

def generate_strong_password():
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = '#.,!@&^%*'
    
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    remaining_length = random.randint(4, 12)
    all_chars = lowercase + uppercase + digits + special
    password.extend(random.choice(all_chars) for _ in range(remaining_length))
    random.shuffle(password)
    
    return ''.join(password)

@app.route('/', methods=['GET', 'POST'])
def home():
    password = None
    if request.method == 'POST':
        password = generate_strong_password()
    return render_template('password.html', password=password)

if __name__ == '__main__':
    os.makedirs('public', exist_ok=True)
    app.run()