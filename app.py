from flask import Flask, render_template_string
from itertools import combinations, permutations
from math import comb, factorial

app = Flask(__name__)

def generate_states(n):
    particles = list(range(1, n + 1))
    energy_levels = list(range(n))
    states = []
    for size in range(1, n + 1):
        for chosen_particles in combinations(particles, size):
            for chosen_levels in combinations(energy_levels, size):
                for level_order in permutations(chosen_levels):
                    state = tuple(zip(chosen_particles, level_order))
                    states.append(state)
    return states

def expected_count(n):
    return sum(comb(n, k) ** 2 * factorial(k) for k in range(1, n + 1))

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>states</title>
  <style>
    body { font-family: monospace; padding: 40px; background: white; color: #111; }
    form { margin-bottom: 24px; }
    input[type=number] { width: 50px; font-family: monospace; font-size: 1rem; border: 1px solid #ccc; padding: 4px 6px; }
    button { font-family: monospace; padding: 4px 12px; cursor: pointer; }
    p { color: #888; margin-bottom: 16px; font-size: 0.85rem; }
    ol { padding-left: 1.4rem; line-height: 2; }
  </style>
</head>
<body>
  <form method="get">
    n = <input type="number" name="n" value="{{ n }}" min="1" max="6">
    <button type="submit">generate</button>
  </form>

  {% if states %}
  <p>{{ total }} states for n = {{ n }}</p>
  <ol>
    {% for i, state in states %}
    <li>{{ state }}</li>
    {% endfor %}
  </ol>
  {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    from flask import request
    n = int(request.args.get("n", 2))
    n = max(1, min(n, 6))
    states = generate_states(n)
    return render_template_string(HTML,
        n=n,
        states=list(enumerate(states, start=1)),
        total=len(states)
    )

if __name__ == "__main__":
    app.run(debug=True, port=5050)
