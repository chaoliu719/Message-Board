kill gunicorn
kill -9 $(ps -ef|grep gunicorn|gawk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')
�ڷ���������gunicorn
gunicorn -b 0.0.0.0:80 Board:app
�ڱ��ص��ԣ����޸�Board.py
python Board.py