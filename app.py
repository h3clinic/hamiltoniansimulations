from flask import Flask, render_template_string, request

from states import format_basis_state, generate_basis_states

app = Flask(__name__)


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
    max vibration = <input type="number" name="v" value="{{ max_vibration }}" min="0" max="20">
    <button type="submit">generate</button>
  </form>

  {% if basis_states %}
  <p>{{ total }} basis states for n = {{ n }}; max vibration = {{ max_vibration }}</p>
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
    max_vibration = int(request.args.get("v", n - 1))
    max_vibration = max(0, min(max_vibration, 20))
    basis_states = generate_basis_states(n, max_vibration)
    formatted = [format_basis_state(basis_state) for basis_state in basis_states]

    return render_template_string(
        HTML,
        n=n,
        max_vibration=max_vibration,
        basis_states=list(enumerate(formatted, start=1)),
        total=len(basis_states),
    )


if __name__ == "__main__":
    app.run(debug=False, port=5050)
