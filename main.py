from flask import Flask
from flask_restful import Api, Resource, reqparse
import mysql.connector
import os


app = Flask(__name__)
api = Api(app)

def mysql_insert(id_mb, timestamp, hostname, mac, ipv4, users):
    
    mydb = mysql.connector.connect(
      host="localhost",
      user="dev",
      passwd="fallout",
      database="audit"
    )
    cursor = mydb.cursor()
    print("SELECT")
    cursor.execute("SELECT * FROM hosts WHERE id_mb=%s", (id_mb,))

    if len( cursor.fetchall() ) == 0:
        try:
            print("INSERT")
            cursor.execute("""INSERT INTO hosts (id_mb, timestamp, hostname, mac, ipv4, users) VALUES (%s, %s, %s, %s, %s, %s)""", ( id_mb, timestamp, hostname, mac, ipv4, users ))
        except mysql.connector.Error as e:
            print("Error: {}".format(e))
    else:
        print("UPDATE")
        cursor.execute ("""
           UPDATE hosts
           SET id_mb=%s, timestamp=%s, hostname=%s, ipv4=%s, mac=%s, users=%s
           WHERE id_mb=%s
           """, ( id_mb, timestamp, hostname, ipv4, mac, users, id_mb ))   

    mydb.commit()

def check_user(users):
    os.system('ipa user-find --all --raw | grep -iE "(uid: *)" | cut -d" " -f4 > ./list_user_freeipa.txt')
    file=open('./list_user_freeipa.txt','r')
    file_freeipa_users=file.read()
    for user_ipa in [ users ]:
        if user_ipa in file_freeipa_users:
            print('Ok')
            return "Ok"
        else:
            print('Kill {}'.format(user_ipa))
            return user_ipa

@app.route('/post', methods=['POST'])
def post():
      parser = reqparse.RequestParser()
      parser.add_argument("timestamp")
      parser.add_argument("id_mb")
      parser.add_argument("hostname")
      parser.add_argument("mac")
      parser.add_argument("ipv4")
      parser.add_argument("users")
      params = parser.parse_args()
 
      host_post = {
          "timestamp": params["timestamp"],
          "id_mb": params["id_mb"],    
          "hostname": params["hostname"],
          "mac": params["mac"],
          "ipv4": params["ipv4"],
          "users": params["users"]
      }

      mysql_insert(params["id_mb"], params["timestamp"], params["hostname"], params["mac"], params["ipv4"], params["users"])
      
      kill_u = check_user(params["users"])
   
      if kill_u == "Ok":
          return "Ok", 200
      else:         
          return kill_u, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
