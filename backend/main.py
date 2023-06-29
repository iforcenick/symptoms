from flask import Flask, request
from mysql.connector import connect, Error

app = Flask(__name__)

connection = connect(
    host="localhost",
    user="root",
    password="rootroot",
    database="symptom_db"
)
cursor = connection.cursor()

@app.route('/rare_conditions', methods=['GET'])
def get_rare_conditions():
    global cursor
    cursor.execute('''SELECT * from disorder_table''')
    disorders = cursor.fetchall()
    print(disorders[0])
    for disorder in disorders:
        disorder_xml = BeautifulSoup(disorder[1], "xml")
        asscs = disorder_xml.find_all('HPODisorderAssociation')
        for hpo in asscs:
            hpo_id_element = hpo.HPOId
            hpo_id = hpo_id_element.get_text()
            freq_element = hpo.HPOFrequency.Name
            freq = freq_element.get_text()
            matches = re.search('\\((.*?)(\\d+)-(\\d+)(.*?)\\)', freq)
            min_freq = max_freq = 0
            if matches is not None:
                min_freq = int(matches[3])
                max_freq = int(matches[2])
            
    hpos_str = request.args.get('hpos')
    hpos = hpos_str.split(",")
    
    return ' '.join(hpos)