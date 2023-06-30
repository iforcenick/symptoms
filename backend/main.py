from flask import Flask, request
from mysql.connector import connect, Error
import json

app = Flask(__name__)

connection = connect(
    host="localhost",
    user="root",
    password="rootroot",
    database="symptom_db"
)
cursor = connection.cursor()

@app.route('/hpo', methods=['GET'])
def get_hpo():
    cursor.execute('''SELECT * FROM hpo_table''')
    hpos = cursor.fetchall()
    return json.dumps(hpos)

@app.route('/rare_conditions', methods=['GET'])
def get_rare_conditions():
    hpos_str = request.args.get('hpos')
    selected_hpos = [ int(item) for item in hpos_str.split(",") ]

    global cursor
    cursor.execute('''SELECT * FROM symptom_table WHERE ''' + ' OR '.join([f'hpo_id = {id}' for id in selected_hpos]))
    symptoms = cursor.fetchall()
    symptom_map = {}
    for symptom in symptoms:
        print(symptom[0])
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