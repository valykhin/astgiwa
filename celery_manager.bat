@echo off
DEL D:\studing\django\astgiwa\celerybeat.pid
echo ' ' > D:\studing\django\astgiwa\celery_beat.log
echo ' ' > D:\studing\django\astgiwa\celery_worker.log
If '%1'=='start' start /I manage.py celery beat -f celery_beat.log
If '%1'=='start' start /I manage.py celery worker -A astgiwa -f celery_worker.log
