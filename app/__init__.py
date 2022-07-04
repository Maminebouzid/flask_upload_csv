from crypt import methods
from flask import Flask , render_template, request, flash, redirect, make_response, url_for
from werkzeug.utils import secure_filename
import csv
from .enums.FileEnum import InputEnums, OutputEnum
import datetime
import pycountry
from io import StringIO
from werkzeug.wrappers import Response
import os
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == "csv"

def read_file_content(file):
    lines = file.read().decode("utf-8")
    csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(lines.splitlines(), skipinitialspace=True)]
    
    return csv_dicts

def check_header(content):
    if len(content) >1:
        keys = list (content[0].keys())
        expected_header =  InputEnums.enum_to_list()
      
        return keys == expected_header
    
    return False

def get_line_content(line):
    """
    read each line content from csv and check for errors

    """
    content = {}
    date_format = '%Y/%m/%d'
    content[InputEnums.ID.value]=  line[InputEnums.ID.value]

    try:
        content[InputEnums.REALEASE_DATE.value] = datetime.datetime.strptime(line[InputEnums.REALEASE_DATE.value], date_format)
        
    except ValueError:
        return 'date error'
    
    content[InputEnums.GAME_NAME.value] = line[InputEnums.GAME_NAME.value]

    country_code = line[InputEnums.COUNTRY_CODE.value]
    if len(country_code) != 3:
        return 'country format error'
    content[InputEnums.COUNTRY_CODE.value] = country_code
    content[InputEnums.NBR_COPY.value] = int(line[InputEnums.NBR_COPY.value])

    content[InputEnums.PRICE.value] = float(line[InputEnums.PRICE.value])

    return content

def get_country_name(country_code):
    country=  pycountry.countries.get(alpha_3=country_code)
    return country.name


def get_output_data(data):
    output_data = []
    date_format = '%d.%m.%Y'
    
    for line in data:
        content = {}
        content[OutputEnum.ID.value]=  line[InputEnums.ID.value]
        content[OutputEnum.REALEASE_DATE.value]  = line[InputEnums.REALEASE_DATE.value].strftime(date_format) 
        content[OutputEnum.GAME_NAME.value] = line[InputEnums.GAME_NAME.value].capitalize()       
        content[OutputEnum.COUNTRY.value] = get_country_name(line[InputEnums.COUNTRY_CODE.value]) 
      
        nbr_copy = int(line[InputEnums.NBR_COPY.value])
        price = float(line[InputEnums.PRICE.value])
        revenue = nbr_copy * price
        
        content[OutputEnum.NBR_COPY.value]  = nbr_copy
        content[OutputEnum.PRICE.value] =str(price ) +" USD"
        content[OutputEnum.REVENUE.value] = str (round(revenue)) +" USD"
        output_data.append(content)
    
    return output_data



def generate_output_data(content):
    data = []
    for line in content:
    
        data.append(get_line_content(line))
    #order the lines by date
    data.sort(key=lambda item:item[InputEnums.REALEASE_DATE.value])
    
    output_data = get_output_data(data)
  
    return output_data
 
def parse_user_file(file):
        content = read_file_content(file)
        
        valid_header = check_header(content)
        if valid_header  :
            
            data = generate_output_data(content)
            return data
        return valid_header

def generate_file(data):
    buffer = StringIO()
    writer = csv.writer(buffer)
    # write header
    writer.writerow(data[0].keys())
    yield buffer.getvalue()
    buffer.seek(0)
    buffer.truncate(0)
    for line in data:
         
        writer.writerow((
            line[OutputEnum.ID.value], line[OutputEnum.REALEASE_DATE.value], line[OutputEnum.GAME_NAME.value], line[OutputEnum.COUNTRY.value],
             line[OutputEnum.NBR_COPY.value], line[OutputEnum.PRICE.value], line[OutputEnum.REVENUE.value])
        )
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate(0)

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