from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # Needed for session

jokes = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? Because it had too many problems.",
    "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I'm reading a book on anti-gravity. It's impossible to put down!"
]

colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'teal']

base_template = '''
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Fun Flask App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
    <style>
      body {
        padding-top: 70px;
        transition: background-color 0.3s, color 0.3s;
      }
      [data-theme="dark"] {
        background-color: #121212;
        color: #e0e0e0;
      }
      [data-theme="dark"] .navbar {
        background-color: #1f1f1f !important;
      }
      .btn-copy {
        cursor: pointer;
      }
      footer {
        margin-top: 3rem;
        padding: 1rem 0;
        text-align: center;
        font-size: 0.9rem;
        color: #666;
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
      <ul class="navbar-nav me-auto">
        <li class="nav-item"><a class="nav-link {% if active == 'jokes' %}active{% endif %}" href="/">Jokes</a></li>
        <li class="nav-item"><a class="nav-link {% if active == 'magic' %}active{% endif %}" href="/magic">Magic Number</a></li>
        <li class="nav-item"><a class="nav-link {% if active == 'color' %}active{% endif %}" href="/color">Color Text</a></li>
        <li class="nav-item"><a class="nav-link {% if active == 'reverse' %}active{% endif %}" href="/reverse">Reverse Text</a></li>
      </ul>
      <button id="dark-toggle" class="btn btn-outline-light btn-sm">Toggle Dark Mode</button>
    </div>
  </div>
</nav>
<div class="container">
  {{ content|safe }}
</div>
<footer>
  &copy; 2025 Fun Flask App — Crafted with ❤️
</footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
  // Dark mode toggle and persistence
  const toggleBtn = document.getElementById('dark-toggle');
  const htmlEl = document.documentElement;

  function setTheme(theme) {
    htmlEl.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }

  toggleBtn.addEventListener('click', () => {
    const current = htmlEl.getAttribute('data-theme');
    if(current === 'light') {
      setTheme('dark');
    } else {
      setTheme('light');
    }
  });

  // Load saved theme
  const savedTheme = localStorage.getItem('theme') || 'light';
  setTheme(savedTheme);
</script>
</body>
</html>
'''

@app.route('/')
def home():
    # Initially show first joke
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
        fetch('/api/joke?index=' + currentIndex)
          .then(response => response.json())
          .then(data => {{
            document.getElementById('joke-text').textContent = data.joke;
          }});
    }});
    </script>
    '''
    return render_template_string(base_template, content=page_content, active='jokes')

@app.route('/api/joke')
def api_joke():
    idx = request.args.get('index', default=0, type=int)
    joke = jokes[idx % len(jokes)]
    return jsonify({'joke': joke})

@app.route('/magic')
def magic():
    magic_number = random.randint(1, 1000)
    # Store magic number history in session (keep last 5)
    history = session.get('magic_history', [])
    history.insert(0, magic_number)
    session['magic_history'] = history[:5]

    page_content = f'''
    <h1>Your magic number is: <span id="magic-number">{magic_number}</span></h1>
    <p>This number will refresh in <span id="countdown">10</span> seconds.</p>
    <h5>Last 5 magic numbers:</h5>
    <ul id="history-list" class="list-group mb-3">
      {''.join(f'<li class="list-group-item">{num}</li>' for num in session['magic_history'])}
    </ul>
    <p><a href="/">Back Home</a></p>
    <script>
    let countdown = 10;
    const countdownEl = document.getElementById('countdown');
    const magicNumberEl = document.getElementById('magic-number');
    const historyList = document.getElementById('history-list');

    function refreshNumber() {{
        fetch('/api/magic')
            .then(response => response.json())
            .then(data => {{
                magicNumberEl.textContent = data.magic_number;
                countdown = 10;
                updateHistory(data.magic_history);
            }});
    }}

    function updateHistory(history) {{
      historyList.innerHTML = '';
      history.forEach(num => {{
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.textContent = num;
        historyList.appendChild(li);
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
    return render_template_string(base_template, content=page_content, active='magic')

@app.route('/api/magic')
def api_magic():
    magic_number = random.randint(1, 1000)
    history = session.get('magic_history', [])
    history.insert(0, magic_number)
    session['magic_history'] = history[:5]
    return jsonify({'magic_number': magic_number, 'magic_history': session['magic_history']})

@app.route('/color')
def color():
    page_content = f'''
    <h1 id="color-text">This text changes color!</h1>
    <button id="toggle-color" class="btn btn-secondary mb-3">Pause Color Cycle</button>
    <p><a href="/">Back Home</a></p>
    <script>
    const colors = {colors};
    let index = 0;
    let cycling = true;
    const textEl = document.getElementById('color-text');
    const toggleBtn = document.getElementById('toggle-color');

    function cycleColor() {{
        if (!cycling) return;
        textEl.style.color = colors[index];
        index = (index + 1) % colors.length;
    }}

    toggleBtn.addEventListener('click', () => {{
      cycling = !cycling;
      toggleBtn.textContent = cycling ? 'Pause Color Cycle' : 'Resume Color Cycle';
      if (cycling) cycleColor();
    }});

    cycleColor();
    setInterval(cycleColor, 1000);
    </script>
    '''
    return render_template_string(base_template, content=page_content, active='color')

@app.route('/reverse', methods=['GET'])
def reverse():
    page_content = '''
    <h1>Reverse Text</h1>
    <form id="reverse-form" method="post" onsubmit="return false;">
        <div class="mb-3">
            <label for="text" class="form-label">Enter text:</label>
            <input type="text" id="text" name="text" class="form-control" autocomplete="off" />
        </div>
    </form>
    <h3>Reversed: <span id="reversed-text"></span> <button id="copy-btn" class="btn btn-sm btn-outline-primary btn-copy">Copy</button></h3>
    <p><a href="/">Back Home</a></p>
    <script>
    const input = document.getElementById('text');
    const output = document.getElementById('reversed-text');
    const copyBtn = document.getElementById('copy-btn');

    input.addEventListener('input', () => {{
        const val = input.value;
        output.textContent = val.split('').reverse().join('');
    }});

    copyBtn.addEventListener('click', () => {{
      if(output.textContent.length === 0) return;
      navigator.clipboard.writeText(output.textContent)
        .then(() => {{
          copyBtn.textContent = 'Copied!';
          setTimeout(() => copyBtn.textContent = 'Copy', 1500);
        }});
    }});
    </script>
    '''
    return render_template_string(base_template, content=page_content, active='reverse')

@app.errorhandler(404)
def page_not_found(e):
    page_content = '''
    <div class="text-center mt-5">
      <h1>404 - Page Not Found</h1>
      <p>Oops! The page you are looking for does not exist.</p>
      <a href="/" class="btn btn-primary">Go Home</a>
    </div>
    '''
    return render_template_string(base_template, content=page_content, active=''), 404

if __name__ == '__main__':
    app.run(debug=True)
