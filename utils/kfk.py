import gnsq

producer = gnsq.Producer('127.0.0.1:4150')

producer.publish('topic', 'hello gevent!')
producer.publish('topic', 'hello nsq!')