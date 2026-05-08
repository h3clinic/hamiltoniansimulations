from flask import Flask, render_template_string, request
from itertools import combinations, permutations

app = Flask(__name__)


def generate_basis_states(n):
    particles = list(range(1, n + 1))
    energy_levels = list(range(n))
    basis_states = []

    for k in range(1, n + 1):
        for chosen_particles in combinations(particles, k):
            for chosen_levels in combinations(energy_levels, k):
                for assigned_levels in permutations(chosen_levels):
                    basis_state = tuple(zip(chosen_particles, assigned_levels))
                    basis_states.append(basis_state)

    return basis_states


def format_basis_state(basis_state):
    ordered_pairs = sorted(basis_state, key=lambda pair: pair[1]) if len(basis_state) > 1 else basis_state
    entries = []

    for index, (particle, level) in enumerate(ordered_pairs):
        particle_label = f"{particle}'" if index > 0 else str(particle)
        entries.append(f"{particle_label},{level}")

    return "|" + ";".join(entries) + "⟩"


HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>basis states</title>
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

  {% if basis_states %}
  <p>{{ total }} basis states for n = {{ n }}</p>
  <ol>
    {% for i, basis_state in basis_states %}
    <li>{{ basis_state|safe }}</li>
    {% endfor %}
  </ol>
  {% endif %}
</body>
</html>
"""


@app.route("/")
def index():
    n = int(request.args.get("n", 2))
    n = max(1, min(n, 6))
    basis_states = generate_basis_states(n)
    formatted = [format_basis_state(basis_state) for basis_state in basis_states]

    return render_template_string(
        HTML,
        n=n,
        basis_states=list(enumerate(formatted, start=1)),
        total=len(basis_states),
    )


if __name__ == "__main__":
  app.run(debug=False, port=5050)
