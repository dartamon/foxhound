from django.shortcuts import render
from django.http import HttpResponse
import pycurl, json, StringIO
import json, ast
# Use requests to query the API website and assign results to a variable
import requests
from .models import QueryModel


def links(mined_urls, results, resultTags):
    try:
        z = 0
        for z in range(z, len(results["items"][z])):
            mined_urls.append(results["items"][z]["link"].encode("ascii", "ignore"))
            resultTags.append(results["items"][z]["title"].encode("ascii", "ignore"))
            resultTags.append(results["items"][z]["snippet"].encode("ascii", "ignore"))
    except KeyError, e:
        print e


def index(request):
    return render(request, 'sample/index.html')

def runFoxhound(request):
    index_num = 1  # index_num represent the number of iterations of the startIndex parameter in order to get 100 images
    mined_urls = []
    key = "AIzaSyAjlYK7bngoiPxBE9koo09RWZK3oTNR0mo"
    cx = "008280251192147562951:rghr1k2p058"
    url = "https://www.googleapis.com/customsearch/v1"
    activeRecord = []
    # Append input parameters
    inputTags = []
    if 'query1' in request.POST:
        inputTags.append(request.POST['query1'].encode('ascii', 'ignore'))
    if 'query2' in request.POST:
        inputTags.append(request.POST['query2'].encode('ascii', 'ignore'))
    if 'query3' in request.POST:
        inputTags.append(request.POST['query3'].encode('ascii', 'ignore'))

    if len(inputTags) != 0:
        activeRecord = QueryModel.objects.create(savedtags = inputTags)
        activeRecord.save()
        activeRecord.sessionname = str(activeRecord.id)
        activeRecord.save()
    else:
        activeRecord = QueryModel.objects.get(sessionname=str(request.POST['sessionname']))
        inputTags = ast.literal_eval(json.dumps(activeRecord.savedtags))

    if 'query4' in request.POST:
        inputTags.append(request.POST['query4'].encode('ascii', 'ignore'))
    if 'query5' in request.POST:
        inputTags.append(request.POST['query5'].encode('ascii', 'ignore'))
    if 'query6' in request.POST:
        inputTags.append(request.POST['query6'].encode('ascii', 'ignore'))

    i = 0
    activeRecord.savedtags = inputTags;
    activeRecord.save()

    # Need to locate the top results per keyword into the top results in total
    # Also need to associate images with the keywords and have a way to have the image
    # impact the added keyword

    resultTags = []

    for i in range(i, len(inputTags)):
        parameters = {"q": inputTags[i],
                      "cx": cx,
                      "key": key,
                      "searchType": "image",
                      "start": 1,
                      }
        page = requests.request("GET", url, params=parameters)
        results = json.loads(page.text)
        links(mined_urls, results, resultTags)

    print 'Number of urls ' + str(len(mined_urls))

    context = {
        'queryImageUrls': '',
        'resultImageUrls': mined_urls,
        'sessionid': activeRecord.sessionname,
        'initialTags': inputTags,
        'resultTags': resultTags
    }

    return render(request, 'sample/search.html', context)
