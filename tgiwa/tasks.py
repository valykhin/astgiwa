# -*- coding: utf-8 -*-
from celery.task import periodic_task
from celery.schedules import crontab
from datetime import timedelta

from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import TestRequest, TestConfiguration, Test, URL, Queue, Defect
from searching_defects import search_defect
import smtplib
from email.mime.text import MIMEText


@periodic_task(run_every=crontab(minute='*/2'))
def create_tests():
    print "Starting test request processing"
    unprocessed_test_requests = TestRequest.objects.filter(status='U')
    req_count = len(unprocessed_test_requests)
    print "Number of unprocessed test requests: " + str(req_count)
    for test_req in unprocessed_test_requests:
        test_configs = TestConfiguration.objects.filter(test_request=test_req).order_by('test_request__creation_time')
        urls = URL.objects.filter(test_request=test_req)
        try:
            for test_config in test_configs:
                for url in urls:
                    test = Test(test_configuration=test_config, url=url, status='U', test_request=test_req)
                    test.save()
                    print "Created test №" + str(test.id)
                    try:
                        schedule_time = Queue.objects.latest('scheduled_time').scheduled_time + timedelta(seconds=30)
                    except Queue.DoesNotExist:
                        schedule_time = now()
                    queue = Queue(test=test, scheduled_time=schedule_time)
                    test.status = 'S'
                    test.save()
                    queue.save()
                    print "Created queue №" + str(queue.id)
            test_req.status = 'S'
            test_req.save()
        except Exception:
            print Exception.message
    print "Test request processing has done"


@periodic_task(run_every=crontab(minute='*/2'))
def start_test():
    print "Prepare to start testing"
    last_in_queue = Queue.objects.select_related().filter(test__status='S').order_by('scheduled_time', '-priority').last()
    if last_in_queue is not None:
        print "Start testing"
        status = search_defect(str(last_in_queue.test.url),last_in_queue.test.id, last_in_queue.test.test_configuration.browser.name)
        if status == 0:
            print "Changing test status"
            last_in_queue.test.status = 'T'
            last_in_queue.test.save()
        else:
            print "Test status not changed. Status is " + str(status)
    else:
        print "There is no scheduled tests"


@periodic_task(run_every=crontab(minute='*/1'))
def send_results():
    print "Sending results to users"
    test_reqs = TestRequest.objects.filter(status='S').order_by('creation_time')
    for test_req in test_reqs:
        count_all_tests = Test.objects.filter(test_request=test_req).count()
        count_tested = Test.objects.filter(test_request=test_req, status='T').count()
        if (count_all_tests == count_tested) and (count_all_tests != 0):
            print "All test processed in request: " + str(test_req.id)
            print "Sending results to email: " + test_req.email
            gmail_user = 'ilialsd@gmail.com'
            gmail_pwd = 'x66vskwgqd'
            FROM = 'ilialsd@gmail.com'
            TO = 'ivalykhin@gmail.com'
            SUBJECT = 'The contents of %s' % test_req.id
            results = Defect.objects.select_related('test', 'test__test_configuration', 'test__url').filter(test__test_request=test_req).order_by('creation_time')
            TEXT = render_to_string('results.html', {'test_request': test_req, 'results': results}).encode('utf-8')
            msg = MIMEText(TEXT, _charset='ascii', _subtype='html')
            msg['Subject'] = SUBJECT
            msg['From'] = FROM
            msg['To'] = test_req.email
            server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server_ssl.ehlo() # optional, called by login()
            server_ssl.login(gmail_user, gmail_pwd)
            # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
            server_ssl.sendmail(FROM, TO, msg.as_string())
            #server_ssl.quit()
            server_ssl.close()
            print 'Successfully sent the mail'
            test_req.status = 'P'
            test_req.save()
        else:
            print "Not all tests processed for request: " + str(test_req.id)
    print "Sending has completed"
