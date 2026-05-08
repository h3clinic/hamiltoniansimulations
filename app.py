from flask import Flask, render_template_string, request
from itertools import combinations, permutations

app = Flask(__name__)


def generate_configurations(n):
    particles = [f"p{i}" for i in range(1, n + 1)]
    energy_levels = [f"E{i}" for i in range(n)]
    configurations = []

    for k in range(1, n + 1):
        for chosen_particles in combinations(particles, k):
            for chosen_levels in combinations(energy_levels, k):
                for assigned_levels in permutations(chosen_levels):
                    configuration = tuple(zip(chosen_particles, assigned_levels))
                    configurations.append(configuration)

    return configurations


def format_configuration(configuration):
    pairs = ", ".join(f"({particle}, {energy})" for particle, energy in configuration)
    return "{" + pairs + "}"


HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>configurations</title>
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

  {% if configurations %}
  <p>{{ total }} configurations for n = {{ n }}</p>
  <ol>
    {% for i, configuration in configurations %}
    <li>{{ configuration }}</li>
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
    configurations = generate_configurations(n)
    formatted = [format_configuration(configuration) for configuration in configurations]

    return render_template_string(
        HTML,
        n=n,
        configurations=list(enumerate(formatted, start=1)),
        total=len(configurations),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5050)
