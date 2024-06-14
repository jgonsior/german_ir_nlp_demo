kill -s QUIT $(cat /home/josi3886/demo/backend/gunicorn.pid)
sleep 2
rm nohup.out
#. $HOME/.bashrc
#$HOME/miniconda3/bin/activate
#conda activate RAG_env_conda

/usr/bin/nohup gunicorn -w 2 -b 0.0.0.0:8080 -p gunicorn.pid --timeout 300 run:app &
