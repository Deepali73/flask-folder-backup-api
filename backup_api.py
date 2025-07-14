from flask import Flask, request, jsonify
import shutil, os
from datetime import datetime

app = Flask(__name__)

# Create a base backup directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

# ✅ NEW: Root route to confirm server is running
@app.route("/", methods=["GET"])
def home():
    return (
        "<h2>✅ Flask Backup API is running</h2>"
        "<p>Use <code>POST /backup</code> with a JSON body like:<br>"
        "<code>{ \"folder\": \"C:/Users/ASUS/Documents/message/testfolder\" }</code></p>"
    )

# Main backup route (POST only)
@app.route("/backup", methods=["POST"])
def backup():
    data = request.get_json()
    folder = data.get("folder")

    if not folder or not os.path.exists(folder):
        return jsonify({"error": "Folder not found"}), 400

    name = os.path.basename(folder.rstrip("/\\"))
    time = datetime.now().strftime("%Y%m%d_%H%M")
    zip_path = os.path.join(BACKUP_DIR, f"{name}_{time}.zip")

    # Create zip archive
    shutil.make_archive(zip_path.replace(".zip", ""), "zip", folder)

    return jsonify({
        "message": "✅ Backup successful",
        "backup_file": zip_path
    }), 200

# Entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
