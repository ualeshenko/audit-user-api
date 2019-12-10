import os, socket
import requests, json 

url="http://127.0.0.1:5000/post"
header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"} 
host_id = 1
list_users = os.system("who | cut -d' ' -f1 | sort | uniq")
hostname = os.system("hostname")
data_post = {"hostname": hostname, "users": list_users }


requests.post(url, data=data_post, headers=header)

#response_json = response_decoded_json.json()

#print(response_json)


#status = os.system('systemctl is-active --quiet ufw')
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#if status == 0:
#    print( "UFW started" )
#else:
#    print( "UFW stopped" )

#result = sock.connect_ex(('127.0.0.1',number))


#print(list_users)
