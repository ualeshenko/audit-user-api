
hostname=`hostname`
users=`who`

curl -d "{\"hostname\":\"${hostname}\",\"users\": \"Yurii\"}" -H "Content-Type: application/json" http://localhost:5000/post
