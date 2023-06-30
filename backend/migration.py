from bs4 import BeautifulSoup
import re
from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user="root",
        password="rootroot",
    ) as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE DATABASE IF NOT EXISTS symptom_db;''')
        cursor.execute('''USE symptom_db;''')

        #Executing SQL Statements
        cursor.execute('''CREATE TABLE IF NOT EXISTS symptom_table(disorder_id int, hpo_id int, min_freq int, max_freq int)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS disorder_table(id int, orpha_code int, name varchar(255), expert_link varchar(512))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS hpo_table(id int, legal_id varchar(255), term varchar(255))''')
        
        # #Saving the Actions performed on the DB
        connection.commit()

        with open('symptoms.xml', 'r', encoding='ISO-8859-1') as f:
            data = f.read()
            print("File reading completed")
            # Passing the stored data inside
            # the beautifulsoup parser, storing
            # the returned object
            hpo_data = BeautifulSoup(data, "xml")
            print("XML parse completed.")
            disorders = hpo_data.find_all('Disorder')

            used_hpo_ids = {}

            for disorder in disorders:
                disorder_id = int(disorder['id'])
                orpha_code = int(disorder.OrphaCode.get_text())
                disorder_name = disorder.Name.get_text()
                expert_link = disorder.ExpertLink.get_text()
                cursor.execute('''INSERT INTO disorder_table VALUES(%s,%s,%s,%s)''',(disorder_id, orpha_code, disorder_name, expert_link))
                asscs = disorder.find_all('HPODisorderAssociation')
                for hpo in asscs:
                    hpo_id_num = int(hpo.HPO['id'])
                    legal_id = hpo.HPOId.get_text()
                    hpo_term = hpo.HPOTerm.get_text()
                    freq = hpo.HPOFrequency.Name.get_text()
                    matches = re.search('\\((.*?)(\\d+)-(\\d+)(.*?)\\)', freq)
                    min_freq = max_freq = 0
                    if matches is not None:
                        min_freq = int(matches[3])
                        max_freq = int(matches[2])
                    print(disorder_id, hpo_id_num, freq, min_freq, max_freq)
                    cursor.execute('''INSERT INTO symptom_table VALUES(%s,%s,%s,%s)''',(disorder_id, hpo_id_num, min_freq, max_freq))
                    if hpo_id_num not in used_hpo_ids:
                        used_hpo_ids[hpo_id_num] = True
                        cursor.execute('''INSERT INTO hpo_table VALUES(%s,%s,%s)''',(hpo_id_num, legal_id, hpo_term))
        
        connection.commit()
        # #Closing the cursor
        cursor.close()
except Error as e:
    print(e)
