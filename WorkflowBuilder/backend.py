from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask import Flask, request, jsonify, session, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import os
import importlib.util
import importlib
import sys
from time import sleep
import importlib.util
import sys
import os
import traceback
import re
#import apsw 

AUTH_TOKEN = "SECRETKEY"

# Add a relative path (e.g., "../myfolder" or "./subdir") to sys.path
relative_path = "./detexa"
absolute_path = os.path.abspath(relative_path)

if absolute_path not in sys.path:
    sys.path.append(absolute_path)
from detexa import yesql
from detexa.yesql import functions
app = Flask(__name__)
CORS(app)
app.secret_key = 'SECRETKEY'


def summarize_exception(e):
    tb_lines = traceback.format_exception(type(e), e, e.__traceback__)
    tb_text = ''.join(tb_lines)
    print('lala: ', tb_text)
    sqlerror = 0
    for ll, line in enumerate(tb_lines):
        print(ll, ': ', line)
        if 'udfs.py' in line:
            match = re.search(r'File ".*udfs\.py", line (\d+), in <*(\w+)>*', line)
            if match:
                line_number, func_name = match.groups()
                myline = line.split('\n')
                filtered_list = list(filter(None, myline))
                return f"Error in function '{func_name}' in Python UDF code, at line {line_number}: {filtered_list[-1]}"
        elif 'SQLError' in line:
            sqlerror = 1
    if sqlerror:
        return str(e)
    # Fallback: Generic traceback
    return f"Unhandled Error: {str(e)}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        token = request.form.get('token')
        if token == AUTH_TOKEN:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid token")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
    
    
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def index():
    return render_template('llm_extract.html')




def load_udfs_module():
    module_name = "udfs.udfs"
    module_path = os.path.abspath(os.path.join("udfs", "udfs.py"))

    if module_name in sys.modules:
        del sys.modules[module_name]

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise ImportError(f"Could not load spec for {module_name} at {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        raise ImportError(f"Failed to load module {module_name}: {e}")

# === Call it unconditionally, always try to register udfs from it ===
try:
    mod = load_udfs_module()
    conn = yesql.functions.Connection('data.db')
    if hasattr(mod, 'udfs'):
        functions.register_ops(mod.udfs, conn)
    else:
        functions.register_ops(mod, conn)
except Exception as e:
    print(f"[WARNING] Failed to load/register udfs module: {e}")

def get_datasets():
    # Connect to your SQLite database
    conn = yesql.functions.Connection('data.db')
    cursor = conn.cursor()
    
    # Query the list of all tables (each representing a dataset)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]

@app.route('/api/datasets')
@login_required
def datasets():
    try:
        datasets = get_datasets()  # Function to fetch datasets
        return jsonify({"datasets": datasets})
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Handle any potential error

@app.route('/api/execute', methods=['POST'])
@login_required
def execute_query():
  try:
    data = request.get_json()
    dataset = data.get('dataset')
    query = data.get('query')
    udfs, query = split_udfs_and_query(query)
    print("UDFs:\n\n", udfs)
    print(f"Executing query on {dataset}: {query}")
    udfpath = write_string_to_file_and_get_path(udfs)
    load_udfs_module()
    conn = yesql.functions.Connection('data.db')
    yesql.functions.register(connection=conn, externalpath=udfpath)
    cursor = conn.cursor()
    
    # Example: table 'datasets' with columns 'id', 'name'
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)
    print(f"Executing query on {dataset}: {query}")
    

    #headers = ["doi", "class", "token", "textsnippet", "confidence"]
    headers = [desc[0] for desc in cursor.description]
    html = list_to_html_table(results, headers)
    return jsonify({"status": "ok", "message": html})
  except Exception as e:
    message = summarize_exception(e)
    html = f"""
    <table class="pretty-table" style="color: red; border: 1px solid #ccc; width: 100%; margin-top: 10px;">
        <tr><td>{message}</td></tr>
    </table>
    """
    return jsonify({"status": "ok", "message": html})

def list_to_html_table(data, headers=None):
    html = """
    <style>
      table.pretty-table {
        border-collapse: collapse;
        width: 100%;
        font-family: Arial, sans-serif;
        margin: 0;
      }
      .pretty-table th, .pretty-table td {
        border: 1px solid #ccc;
        padding: 8px 12px;
        text-align: left;
      }
      .pretty-table th {
        background-color: #f2f2f2;
        font-weight: bold;
      }
      .pretty-table tr:nth-child(even) {
        background-color: #f9f9f9;
      }
    </style>
    <table class="pretty-table">
    """
    
    if headers:
        html += "  <thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead>\n"

    html += "  <tbody>\n"
    for row in data:
        html += "    <tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>\n"
    html += "  </tbody>\n</table>"

    return html


_last_loaded_udf_content = None  # cache last content

def write_string_to_file_and_get_path(content, file_name="udfs/udfs.py", directory='udfs'):
    global _last_loaded_udf_content

    os.makedirs(directory, exist_ok=True)

    # Write content to the file
    with open(file_name, "w") as file:
        file.write(content)
        file.flush()

    module_path = os.path.abspath(file_name)
    module_name = "udfs"

    # Reload only if content changed
    if module_name in sys.modules and _last_loaded_udf_content == content:
        # Nothing changed, no reload needed
        return os.path.abspath(directory)

    # Remove old version (if any)
    if module_name in sys.modules:
        del sys.modules[module_name]

    # Load new version
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot create spec for module at {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # Save latest content to detect changes
    _last_loaded_udf_content = content

    return os.path.abspath(directory)



def split_udfs_and_query(code: str):
    lines = code.strip().splitlines()
    udfs = []
    query = []
    in_query = False

    for line in lines:
        if line.strip().startswith("-- YeSQL Query"):
            in_query = True
        if in_query:
            query.append(line)
        else:
            udfs.append(line)

    return "\n".join(udfs), "\n".join(query)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)


