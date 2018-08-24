# flasky

#使用CELERY功能必须打开WORKER和REDIS
/home/redis-2.8.17/src/redis-server /home/redis-2.8.17/redis.conf
celery -A app.worker.celery worker --loglevel=info
nohup celery -A app.worker.celery worker --loglevel=info &

#使用APS需要GUN启动时保证单一进程启动

学习
