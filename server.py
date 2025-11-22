from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__, static_folder="static")

# Excel path (same folder)
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "QT Scholarship Results.xlsx")

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/search")
def search():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        df = pd.read_excel(EXCEL_PATH, dtype=str, keep_default_na=False)
    except Exception as e:
        return jsonify({"error": f"Error reading Excel: {str(e)}"}), 500

    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    col_order = list(df.columns)

    matches = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False)).any(axis=1)]

    if matches.empty:
        return jsonify({"found": False, "data": [], "columns": col_order})

    return jsonify({
        "found": True,
        "columns": col_order,
        "data": matches.to_dict(orient="records")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
