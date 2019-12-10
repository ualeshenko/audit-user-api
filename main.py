from flask import Flask
from flask_restful import Api, Resource, reqparse
import mysql.connector
import json

app = Flask(__name__)
api = Api(app)

def mysql_insert(id_mb, timestamp, hostname, ipv4, users):
    
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
            cursor.execute("""INSERT INTO hosts (id_mb, timestamp, hostname, ipv4, users) VALUES (%s, %s, %s, %s, %s)""", ( id_mb, timestamp, hostname, ipv4, users ))
        except mydb.Error as error:
            print("Error: {}".format(error))
    else:
        print("UPDATE")
        cursor.execute ("""
           UPDATE hosts
           SET id_mb=%s, timestamp=%s, hostname=%s, ipv4=%s, users=%s
           WHERE id_mb=%s
           """, ( id_mb, timestamp, hostname, ipv4, users, id_mb ))   

    mydb.commit()

@app.route('/post', methods=['POST'])
def post():
      parser = reqparse.RequestParser()
      parser.add_argument("timestamp")
      parser.add_argument("id_mb")
      parser.add_argument("hostname")
      parser.add_argument("ipv4")
      parser.add_argument("users")
      params = parser.parse_args()
 
      host_post = {
          "timestamp": params["timestamp"],
          "id_mb": params["id_mb"],    
          "hostname": params["hostname"],
          "ipv4": params["ipv4"],
          "users": params["users"]
      }

      mysql_insert(params["id_mb"], params["timestamp"], params["hostname"], params["ipv4"], params["users"])

      return host_post, 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
