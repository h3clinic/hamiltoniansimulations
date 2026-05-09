from flask import Flask, render_template_string, request

from states import generate_basis_states, count_basis_states

app = Flask(__name__)

DISPLAY_LIMIT = 5000
PREVIEW_COUNT = 100

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>basis states</title>
  <style>
    body { font-family: monospace; padding: 40px; background: white; color: #111; }
    form { margin-bottom: 24px; display: flex; gap: 16px; align-items: flex-end; flex-wrap: wrap; }
    label { display: flex; flex-direction: column; gap: 4px; font-size: 0.9rem; }
    input[type=number] { width: 60px; font-family: monospace; font-size: 1rem; border: 1px solid #ccc; padding: 4px 6px; }
    button { font-family: monospace; padding: 6px 14px; cursor: pointer; }
    .info { color: #888; margin-bottom: 8px; font-size: 0.85rem; }
    .formula { color: #555; margin-bottom: 8px; font-size: 0.85rem; }
    .truncated { color: #c00; margin-bottom: 8px; font-size: 0.8rem; }
    ol { padding-left: 1.4rem; line-height: 2; }
  </style>
</head>
<body>
  <form method="get">
    <label>Number of modes (n)
      <input type="number" name="n" value="{{ n }}" min="1" max="10">
    </label>
    <label>Max vibration per mode (v)
      <input type="number" name="v" value="{{ v }}" min="0" max="20">
    </label>
    <button type="submit">generate</button>
  </form>

  {% if total is not none %}
  <p class="info">{{ total }} basis states &nbsp;|&nbsp; n = {{ n }}, v = {{ v }}</p>
  <p class="formula">Formula: ({{ v }}+1)<sup>{{ n }}</sup> = {{ total }} &nbsp;&nbsp; each mode: v&#x1D62; &isin; {0, &hellip;, {{ v }}}</p>
  {% if truncated %}
  <p class="truncated">Showing first {{ preview }} of {{ total }} states. Reduce n or v to see all.</p>
  {% endif %}
  {% if basis_states %}
  <ol>
    {% for i, basis_state in basis_states %}
    <li>{{ basis_state|safe }}</li>
    {% endfor %}
  </ol>
  {% endif %}
  {% endif %}
</body>
</html>
"""


@app.route("/")
def index():
    n = int(request.args.get("n", 3))
    n = max(1, min(n, 10))
    v = int(request.args.get("v", 2))
    v = max(0, min(v, 20))

    total = count_basis_states(n, v)

    if total <= DISPLAY_LIMIT:
        basis_states = generate_basis_states(n, v)
        truncated = False
        preview = total
    else:
        basis_states = generate_basis_states(n, v)[:PREVIEW_COUNT]
        truncated = True
        preview = PREVIEW_COUNT

    return render_template_string(
        HTML,
        n=n,
        v=v,
        basis_states=list(enumerate(basis_states, start=1)),
        total=total,
        truncated=truncated,
        preview=preview,
    )


if __name__ == "__main__":
    app.run(debug=False, port=5050)
