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
  <title>State Generator</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: monospace; background: #f9f9f9; color: #111; padding: 40px; }
    h1 { font-size: 1.4rem; margin-bottom: 24px; font-weight: 600; }

    form { display: flex; align-items: center; gap: 12px; margin-bottom: 32px; }
    label { font-size: 0.9rem; }
    input[type=number] {
      width: 60px; padding: 6px 10px; border: 1px solid #ccc;
      border-radius: 4px; font-family: monospace; font-size: 1rem;
    }
    button {
      padding: 7px 18px; background: #111; color: #fff;
      border: none; border-radius: 4px; cursor: pointer;
      font-family: monospace; font-size: 0.9rem;
    }
    button:hover { background: #333; }

    .meta { font-size: 0.85rem; color: #555; margin-bottom: 20px; }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
      gap: 8px;
    }
    .state {
      background: white; border: 1px solid #e0e0e0;
      border-radius: 6px; padding: 10px 12px;
      font-size: 0.8rem; line-height: 1.6;
    }
    .state .idx { color: #aaa; font-size: 0.72rem; margin-bottom: 2px; }
    .pair { display: inline-block; margin-right: 4px; }
    .pair span.p { color: #1a6ef5; }
    .pair span.e { color: #e07b00; }
  </style>
</head>
<body>
  <h1>State Generator</h1>

  <form method="get">
    <label>n =</label>
    <input type="number" name="n" value="{{ n }}" min="1" max="6">
    <button type="submit">Generate</button>
  </form>

  {% if states %}
  <div class="meta">
    Formula: &Sigma; C(n,k)&sup2; &middot; k! &nbsp;|&nbsp;
    n = {{ n }} &nbsp;&rarr;&nbsp; <strong>{{ total }} states</strong>
  </div>
  <div class="grid">
    {% for i, state in states %}
    <div class="state">
      <div class="idx">{{ i }}</div>
      {% for p, e in state %}
      <span class="pair">(<span class="p">{{ p }}</span>,<span class="e">{{ e }}</span>)</span>
      {% endfor %}
    </div>
    {% endfor %}
  </div>
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
