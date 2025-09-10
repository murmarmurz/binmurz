# app.py
from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, request, jsonify
from bin_lookup import lookup_bin

app = Flask(__name__)

@app.route("/api/lookup", methods=["GET"])
def api_lookup():
    binq = request.args.get("bin") or request.args.get("bin6")
    if not binq:
        return jsonify({"error": "Parameter 'bin' diperlukan (6 digit)."}), 400
    res = lookup_bin(binq)
    if "error" in res:
        return jsonify(res), 502
    # build friendly response
    pretty = {
        "bin": res.get("queried_bin"),
        "scheme": res.get("scheme"),
        "type": res.get("type"),
        "brand": res.get("brand"),
        "prepaid": res.get("prepaid"),
        "country": res.get("country"),
        "bank": res.get("bank"),
        "source_cache": res.get("from_cache", False)
    }
    return jsonify(pretty)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)