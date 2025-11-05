from flask import request, jsonify, render_template
from src.application.use_cases import UploadBinaryCase
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository

def register_routes(app):


    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/upload", methods=["POST"])
    def upload_file():


        # Request file input y environment variables 
        file = request.files['files']
        environment = request.form.get('environment', 'dev')

        # Invoque  "Upload Binary Use case" with current context
        use_case = UploadBinaryCase(FileRepository(), JsonRepository)
        binary = use_case.execute(file, environment)

        # Return current use cases 
        return jsonify({'id': binary.id, 'status': binary.status})

