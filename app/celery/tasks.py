from app import celery
from app.models_celery import Celery_task
import time,random
from datetime import datetime

@celery.task(bind=True, default_retry_delay=30, max_retries=3)
def mytask(self,id):
    try:
        for i in range(10):
            self.update_state(state='PROGRESS',
                              meta={'current': i, 'total': 10,'status': '任务[%s]运行中......'%i})
            time.sleep(5)
            key=random.randint(1,100)
            if key%10==1:
                raise Exception('%d'%key)
        print('任务[%s]完成！'%id)
        return {'current': 100, 'total': 100, 'status': '任务[%s]完成!'%id ,'result': 100 ,'end_time': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}
    except Exception as exc:
        raise self.retry(exc=exc,countdown=60)
