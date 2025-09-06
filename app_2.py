from flask import Flask, request, jsonify, render_template_string
import numpy as np

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Suma con Flask + NumPy</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
  <style>
    :root{
      --bg:#0f172a;
      --card:#0b1320;
      --accent:#7c3aed;
      --muted:#94a3b8;
      --glass: rgba(255,255,255,0.04);
    }
    *{box-sizing:border-box;font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial;}
    body{margin:0;background:linear-gradient(180deg,#071029 0%, var(--bg) 100%);color:#e6eef8;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;}
    .card{background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));backdrop-filter:blur(6px);border-radius:12px;padding:28px;width:100%;max-width:640px;box-shadow:0 8px 30px rgba(2,6,23,0.6);border:1px solid rgba(255,255,255,0.03)}
    h1{margin:0 0 8px;font-size:20px}
    p.lead{margin:0 0 20px;color:var(--muted);font-size:14px}
    .row{display:flex;gap:12px;flex-wrap:wrap}
    .input{
      flex:1 1 160px;
      display:flex;flex-direction:column;
    }
    label{font-size:12px;color:var(--muted);margin-bottom:6px}
    input[type="number"]{
      padding:10px 12px;border-radius:8px;border:1px solid rgba(255,255,255,0.04);background:var(--glass);color:inherit;font-size:16px;outline:none;
      transition:box-shadow .15s, transform .06s;
    }
    input[type="number"]:focus{box-shadow:0 6px 18px rgba(124,58,237,0.12);transform:translateY(-1px)}
    .actions{display:flex;gap:12px;margin-top:18px}
    button{
      border:0;padding:10px 14px;border-radius:10px;font-weight:600;cursor:pointer;
      background:linear-gradient(90deg,var(--accent),#5b21b6);color:white;
      box-shadow:0 6px 18px rgba(124,58,237,0.18);
    }
    button.ghost{background:transparent;border:1px solid rgba(255,255,255,0.06);color:var(--muted);box-shadow:none}
    .result{
      margin-top:18px;padding:14px;border-radius:10px;background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border:1px solid rgba(255,255,255,0.03);
      display:flex;justify-content:space-between;align-items:center;
    }
    .r-left{color:var(--muted);font-size:13px}
    .r-right{font-weight:700;font-size:18px}
    .error{color:#ff7b7b;margin-top:12px;font-size:13px}
    footer{margin-top:16px;color:var(--muted);font-size:12px;text-align:right}
    @media (max-width:520px){.row{flex-direction:column}.actions{flex-direction:column}}
  </style>
</head>
<body>
  <div class="card" role="main" aria-labelledby="title">
    <h1 id="title">Calculadora de suma — Flask + NumPy</h1>
    <p class="lead">Introduce dos números y presiona <strong>Sumar</strong>. El cálculo se hace en el servidor usando <code>NumPy</code>.</p>

    <div class="row" role="form" aria-label="Formulario de suma">
      <div class="input">
        <label for="a">Número A</label>
        <input id="a" type="number" step="any" placeholder="Ej. 12.5" />
      </div>

      <div class="input">
        <label for="b">Número B</label>
        <input id="b" type="number" step="any" placeholder="Ej. 3.14" />
      </div>
    </div>

    <div class="actions">
      <button id="sumBtn" aria-live="polite">Sumar</button>
      <button id="clearBtn" class="ghost" type="button">Limpiar</button>
    </div>

    <div id="result" class="result" hidden>
      <div class="r-left">Resultado</div>
      <div class="r-right" id="resValue">0</div>
    </div>

    <div id="error" class="error" role="status" aria-atomic="true" hidden></div>

    <footer>Servidor: Flask · Librería de cálculo: NumPy</footer>
  </div>

<script>
  const sumBtn = document.getElementById('sumBtn');
  const clearBtn = document.getElementById('clearBtn');
  const aInput = document.getElementById('a');
  const bInput = document.getElementById('b');
  const resultBox = document.getElementById('result');
  const resValue = document.getElementById('resValue');
  const errorBox = document.getElementById('error');

  function showError(msg){
    errorBox.textContent = msg;
    errorBox.hidden = false;
  }
  function clearError(){
    errorBox.hidden = true;
    errorBox.textContent = '';
  }

  sumBtn.addEventListener('click', async () => {
    clearError();
    const a = aInput.value.trim();
    const b = bInput.value.trim();

    if(a === '' || b === ''){
      showError('Por favor ingresa ambos números.');
      return;
    }

    // Construimos un JSON y lo enviamos al servidor (POST)
    try {
      sumBtn.disabled = true;
      sumBtn.textContent = 'Calculando...';
      const resp = await fetch('/sumar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ a, b })
      });

      const data = await resp.json();
      if(!resp.ok){
        showError(data.error || 'Error en el servidor');
      } else {
        resValue.textContent = data.resultado;
        resultBox.hidden = false;
      }
    } catch (err) {
      showError('Error de conexión: ' + err.message);
    } finally {
      sumBtn.disabled = false;
      sumBtn.textContent = 'Sumar';
    }
  });

  clearBtn.addEventListener('click', () => {
    aInput.value = '';
    bInput.value = '';
    resultBox.hidden = true;
    clearError();
    aInput.focus();
  });

  // Soporta Enter en los inputs
  [aInput, bInput].forEach(inp => {
    inp.addEventListener('keydown', (e) => {
      if(e.key === 'Enter') sumBtn.click();
    });
  });
</script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(TEMPLATE)

@app.route("/sumar", methods=["POST"])
def sumar():
    """Espera JSON { "a": "...", "b": "..." } o números.
       Usa numpy.add para realizar la suma y devuelve JSON.
    """
    try:
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"error": "Se esperaba JSON en el cuerpo de la petición."}), 400

        # Convertimos a float (acepta valores numéricos en strings también)
        a = float(payload.get("a", 0))
        b = float(payload.get("b", 0))

        # Aquí usamos NumPy
        resultado = np.add(a, b)

        # np.add puede devolver tipos numpy; convertimos a Python nativo para JSON
        resultado_py = float(resultado)

        return jsonify({"a": a, "b": b, "resultado": resultado_py})
    except ValueError:
        return jsonify({"error": "Los valores proporcionados no son números válidos."}), 400
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    # Para desarrollo local
    app.run(host="0.0.0.0", port=5000, debug=True)
