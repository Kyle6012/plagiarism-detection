from flask import Flask
from app.routes import bp
from dashboard import create_dashboard

app = Flask(__name__, template_folder="app/templates/", static_folder="app/static/")
app.config['UPLOAD_FOLDER'] = 'uploads'

# Register the blueprint
app.register_blueprint(bp)

# Create the Dash app
dash_app = create_dashboard(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
