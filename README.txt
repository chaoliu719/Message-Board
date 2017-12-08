kill gunicorn
kill -9 $(ps -ef|grep gunicorn|gawk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')
在服务器上用gunicorn
gunicorn -b 0.0.0.0:80 Board:app
在本地调试，先修改Board.py
python Board.py