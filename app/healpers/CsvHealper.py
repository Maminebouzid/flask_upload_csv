import csv
from ..enums.FileEnum import InputEnums, OutputEnum
import datetime
import pycountry
from io import StringIO

def allowed_file(filename):
    """
    check file extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == "csv"


def read_file_content(file):
    """
    read Csv file content
    """
    lines = file.read().decode("utf-8")
    csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(lines.splitlines(), skipinitialspace=True)]
    
    return csv_dicts

def check_header(content):
    """
    check the header of the csv file
    """
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
    """
    convert country code to country name using pycountry
    """
    country=  pycountry.countries.get(alpha_3=country_code)
    return country.name


def compute_output_data(data):
    """
    generate list of python dicts containing the required data for the csv  
    """
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
    """
    generate the desired data for the output
    """
    data = []
    for line in content:
    
        data.append(get_line_content(line))
    #order the lines by date
    data.sort(key=lambda item:item[InputEnums.REALEASE_DATE.value])
    
    output_data = compute_output_data(data)
  
    return output_data
 
def parse_user_file(file):
        '''
        handle the user file
        '''
        content = read_file_content(file)
        
        valid_header = check_header(content)
        if valid_header  :
            
            data = generate_output_data(content)
            return data
        return "wrong header"

def generate_file(data):
    """
    generate the csv file from the list of dicts
    """
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
