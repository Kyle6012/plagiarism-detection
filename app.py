from flask import Flask
from app.routes import bp  # Import the blueprint directly

app = Flask(__name__, template_folder="app/templates/", static_folder="app/static/")
app.config['UPLOAD_FOLDER'] = 'uploads'

# Register the blueprint
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
