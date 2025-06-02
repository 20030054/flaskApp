from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

jokes = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? Because it had too many problems.",
    "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet."
]

colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'teal']

base_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Fun Flask App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
    <style>
      body {
        padding-top: 70px;
      }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
  <div class="container">
    <a class="navbar-brand" href="/">Fun Flask</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
      aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item"><a class="nav-link" href="/">Jokes</a></li>
        <li class="nav-item"><a class="nav-link" href="/magic">Magic Number</a></li>
        <li class="nav-item"><a class="nav-link" href="/color">Color Text</a></li>
        <li class="nav-item"><a class="nav-link" href="/reverse">Reverse Text</a></li>
      </ul>
    </div>
  </div>
</nav>
<div class="container">
  {{ content|safe }}
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/')
def home():
    joke = random.choice(jokes)
    page_content = f'''
    <h1 class="mb-4">Welcome to the Fun Flask App!</h1>
    <div class="card mb-3">
      <div class="card-body">
        <h5 class="card-title">Random Joke</h5>
        <p id="joke-text" class="card-text">{joke}</p>
        <button id="next-joke" class="btn btn-primary">Next Joke</button>
      </div>
    </div>
    <script>
    const jokes = {jokes};
    let currentIndex = jokes.indexOf("{joke}");

    document.getElementById('next-joke').addEventListener('click', () => {{
        currentIndex = (currentIndex + 1) % jokes.length;
        document.getElementById('joke-text').textContent = jokes[currentIndex];
    }});
    </script>
    '''
    return render_template_string(base_template, content=page_content)

@app.route('/magic')
def magic():
    magic_number = random.randint(1, 1000)
    page_content = f'''
    <h1>Your magic number is: <span id="magic-number">{magic_number}</span></h1>
    <p>This number will refresh in <span id="countdown">10</span> seconds.</p>
    <p><a href="/">Back Home</a></p>
    <script>
    let countdown = 10;
    const countdownEl = document.getElementById('countdown');
    const magicNumberEl = document.getElementById('magic-number');

    function refreshNumber() {{
        fetch('/api/magic')
            .then(response => response.json())
            .then(data => {{
                magicNumberEl.textContent = data.magic_number;
                countdown = 10;
            }});
    }}

    setInterval(() => {{
        countdown--;
        countdownEl.textContent = countdown;
        if (countdown <= 0) {{
            refreshNumber();
        }}
    }}, 1000);
    </script>
    '''
    return render_template_string(base_template, content=page_content)

@app.route('/api/magic')
def api_magic():
    return jsonify({'magic_number': random.randint(1, 1000)})

@app.route('/color')
def color():
    page_content = f'''
    <h1 id="color-text">This text changes color!</h1>
    <p><a href="/">Back Home</a></p>
    <script>
    const colors = {colors};
    let index = 0;
    const textEl = document.getElementById('color-text');

    function cycleColor() {{
        textEl.style.color = colors[index];
        index = (index + 1) % colors.length;
    }}

    cycleColor();
    setInterval(cycleColor, 1000);
    </script>
    '''
    return render_template_string(base_template, content=page_content)

@app.route('/reverse', methods=['GET', 'POST'])
def reverse():
    page_content = '''
    <h1>Reverse Text</h1>
    <form id="reverse-form" method="post" onsubmit="return false;">
        <div class="mb-3">
            <label for="text" class="form-label">Enter text:</label>
            <input type="text" id="text" name="text" class="form-control" required autocomplete="off" />
        </div>
    </form>
    <h3>Reversed: <span id="reversed-text"></span></h3>
    <p><a href="/">Back Home</a></p>
    <script>
    const input = document.getElementById('text');
    const output = document.getElementById('reversed-text');

    input.addEventListener('input', () => {{
        const val = input.value;
        output.textContent = val.split('').reverse().join('');
    }});
    </script>
    '''
    return render_template_string(base_template, content=page_content)

if __name__ == '__main__':
    app.run(debug=True)
