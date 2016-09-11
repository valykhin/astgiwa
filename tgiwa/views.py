from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render_to_response
from .models import Browser, Resolution, TestConfiguration, TestRequest, URL, OperatingSystem, Test, Defect
from forms import TestRequestForm


# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def request_for_test(request):
    template = loader.get_template('request_for_test.html')
    context = RequestContext(request, {'form': TestRequestForm
    })
    return HttpResponse(template.render(context))


def create_request(request):
    try:
        test_request = TestRequest(email=request.POST['email'], status='U')
        test_request.save()
        resolutions = Resolution.objects.filter(pk__in=request.POST.getlist('resolutions'))
        browsers = Browser.objects.filter(pk__in=request.POST.getlist('browsers'))
        try:
            for resolution in resolutions:
                for browser in browsers:
                    test_config = TestConfiguration(test_request=test_request, resolution=resolution, browser=browser)
                    test_config.save()
            for url_ in request.POST.getlist('urls'):
                url = URL(test_request=test_request)
                url.parse(url_)
                url.save()
        except IntegrityError:
            print Exception
            test_request.delete()
    except (IOError, test_request.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('neironet_detail.html', {
            'net': net,
            'error_message': "Wrong net file.",
        }, context_instance=RequestContext(request))
    else:
        context = RequestContext(request, {
        'prediction': 'nema',
    })
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('tgiwa.views.request_created', args=(test_request.id,)))


def request_created(request, request_id):
    test_request = get_object_or_404(TestRequest, pk=request_id)
    test_configs = TestConfiguration.objects.select_related().filter(test_request=test_request).\
        order_by('browser__operating_system', 'browser__company', 'browser__name', 'browser__version',
                 'resolution__height')
    urls = URL.objects.filter(test_request=test_request)
    template = loader.get_template('request_created.html')
    context = RequestContext(request, {
        'test_request': test_request, 'test_configs': test_configs, 'urls': urls
    })
    return HttpResponse(template.render(context))


def test_results(request, request_id):
    test_request = get_object_or_404(TestRequest, pk=request_id)
    results = Defect.objects.select_related('test', 'test__test_configuration', 'test__url').filter(test__test_request=test_request).order_by('creation_time')
    template = loader.get_template('results.html')
    context = RequestContext(request, {
        'test_request': test_request, 'results': results
    })
    return HttpResponse(template.render(context))


def contacts(request):
    template = loader.get_template('contacts.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))


def info(request):
    template = loader.get_template('info.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
