from flask import Flask
from flask_restful import Api, Resource, reqparse
import mysql.connector
import json

app = Flask(__name__)
api = Api(app)

def mysql_insert(host_id,hostname, users):
    mydb = mysql.connector.connect(
      host="localhost",
      user="dev",
      passwd="fallout",
      database="audit"
    )

    mycursor = mydb.cursor()

    print(hostname, users)
    sql = "INSERT INTO hosts (host_id, hostname, users) VALUES (%s, %s, %s)"
    #sql = "INSERT INTO hosts (host_id, hostname, users) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE hostname = VALUES(hostname), users = VALUES(users)"
    #sql = "IF EXISTS(select * from hosts where id=%s) update hosts set hostname='%s' users='%s' where id=3012 ELSE insert into test(name) values('john');"
    var = ( host_id, hostname, users )
    mycursor.execute(sql, var)
    mydb.commit()

@app.route('/post', methods=['POST'])
def post():
      parser = reqparse.RequestParser()
      parser.add_argument("host_id")
      parser.add_argument("hostname")
      parser.add_argument("users")
      params = parser.parse_args()
 
      host_post = {
          "host_id": params["host_id"],    
          "hostname": params["hostname"],
          "users": params["users"]
      }

      mysql_insert(params["host_id"],  params["hostname"], params["users"])

      return host_post, 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
