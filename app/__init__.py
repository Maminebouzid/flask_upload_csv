from crypt import methods
from flask import Flask , render_template, request,  make_response
from werkzeug.wrappers import Response
import os
from .healpers.CsvHealper import allowed_file, parse_user_file, generate_file


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ["Secret"]
    return app

app = create_app()

@app.route("/")
def hello_world():
    '''
    index page
    '''
    return render_template("index.html")


@app.route("/upload", methods=['post'])
def handlecsv():
    try:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                
                return make_response({'message': 'No file part'},405)
             
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                return make_response({'message': 'No selected file'},405)
            
            if file and allowed_file(file.filename):
                                
                data = parse_user_file(file)
                if type(data) ==list:
                               
                    # stream the response as the data is generated
                    response = Response(generate_file(data), mimetype='text/csv')
                    
                    # add a filename
                    response.headers.set("Content-Disposition", "attachment", filename=f"{file.filename}-transformed.csv")
                    return response

                    
                else:
                    return make_response({'message': data},405)
            else:
                return make_response({'message': 'format not supported'},405)
    except Exception as e:
        return make_response({'message': f'error {e}'},500)