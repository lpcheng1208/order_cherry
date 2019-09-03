ps aux|grep order_server.py|grep -v grep|awk '{print $2}'|xargs kill -9
nohup python order_server.py >/dev/null &
