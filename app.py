import os
import tempfile
import shutil
import stat

from flask import Flask, request, jsonify
from git import Repo
from analysis_service import analyze_repo_dir

# NEW: Import CORS
from flask_cors import CORS

app = Flask(__name__)

# NEW: Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Load API KEY from environment
API_KEY = os.getenv("API_KEY")


def remove_readonly(func, path, excinfo):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass


@app.before_request
def verify_api_key():
    if request.method == "POST":
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401


@app.route("/")
def home():
    return "AI Code Intelligence Backend is running 🚀"


@app.route("/analyze", methods=["POST"])
def analyze_repo():
    print("🔥 /analyze called")

    data = request.get_json()
    repo_url = data.get("repo_url")

    if not repo_url:
        return {"error": "repo_url required"}, 400

    print("🔥 Repo URL:", repo_url)

    temp = tempfile.mkdtemp()
    repo_dir = os.path.join(temp, "repo")

    try:
        print("🔥 Cloning repository...")
        Repo.clone_from(repo_url, repo_dir)
        print("🔥 Clone completed")
    except Exception as e:
        print("❌ Clone failed:", e)
        shutil.rmtree(temp, ignore_errors=True)
        return {"error": str(e)}, 500

    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    print("🔥 Repo Name:", repo_name)

    try:
        print("🔥 Starting analysis...")
        result = analyze_repo_dir(repo_dir, repo_name)
        print("🔥 Analysis done")
    except Exception as e:
        print("❌ Analysis failed:", e)
        shutil.rmtree(temp, ignore_errors=True)
        return {"error": str(e)}, 500

    print("🧹 Cleaning temporary files...")
    try:
        shutil.rmtree(temp, onerror=remove_readonly)
        print("🧹 Cleanup successful")
    except Exception as e:
        print("⚠ Cleanup warning:", e)

    return jsonify(result)


if __name__ == "__main__":
    print("🚀 Starting backend...")
    app.run(debug=True)
