kill -s QUIT $(cat /home/josi3886/german_ir_nlp_demo/gunicorn.pid)
sleep 2
rm nohup.out
source venv/bin/activate;
/usr/bin/nohup gunicorn -w 2 -b 0.0.0.0:8081 -p gunicorn.pid run:app &
