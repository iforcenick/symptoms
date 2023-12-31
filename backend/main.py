from flask import Flask, request
from flask_cors import CORS
from mysql.connector import connect, Error
import json
from cred import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

app = Flask(__name__)
CORS(app)

connection = connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
cursor = connection.cursor()

@app.route('/hpo', methods=['GET'])
def get_hpo():
    cursor.execute('''SELECT * FROM hpo_table''')
    hpos = cursor.fetchall()
    unique_names = set()
    unique_hpos = []
    for item in hpos:
        if item[2] in unique_names:
            continue
        unique_names.add(item[2])
        unique_hpos.append({"id": item[0], "legal_id": item[1], "name": item[2]})
    return json.dumps(unique_hpos)

@app.route('/rare_conditions', methods=['GET'])
def get_rare_conditions():
    hpos_str = request.args.get('hpos')
    selected_hpos = [ int(item) for item in hpos_str.split(",") ]

    global cursor
    cursor.execute('''SELECT * FROM symptom_table WHERE ''' + ' OR '.join([f'hpo_id = {id}' for id in selected_hpos]))
    symptoms = cursor.fetchall()
    symptom_map = {}
    for symptom in symptoms:
        if symptom[0] not in symptom_map:
            symptom_map[symptom[0]] = []
        symptom_map[symptom[0]].append([ symptom[1], symptom[2], symptom[3] ])


    cursor.execute('''SELECT * FROM hpo_table''')
    hpos = cursor.fetchall()
    hpo_map = {}
    for hpo in hpos:
        hpo_map[hpo[0]] = hpo

    cursor.execute('''SELECT * FROM disorder_table''')
    disorders = cursor.fetchall()
    disorders_with_freq = []
    for disorder in disorders:
        if disorder[0] not in symptom_map:
            continue
        hpo_list = symptom_map[disorder[0]]
        freq = 1
        for hpo_item in hpo_list:
            avg_freq = (hpo_item[1] + hpo_item[2]) / 2 / 100
            if hpo_item[0] in selected_hpos:
                freq *= avg_freq
            else:
                freq *= (1.0 - avg_freq)
        disorder_l = list(disorder)
        disorder_l.append(freq)
        disorders_with_freq.append(disorder_l)
    
    disorders_with_freq = sorted(disorders_with_freq, key=lambda x: x[4])

    response = [ {"id": item[0], "orpha_code": item[1], "name": item[2], "expert_link": item[3], "freq": item[4]} for item in disorders_with_freq if item[4] > 0.00001 ]
    
    return json.dumps(response)

print("Listening to 5000 port")
app.run(host='0.0.0.0', port='5000', debug=True)