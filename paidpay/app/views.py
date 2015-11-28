from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.core import serializers
import json
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import CreateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from decimal import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
import datetime
import csv
import hashlib
import datetime
import pytz
from app.models import Product, Prototype, MainUser, PersonalTransfer
from django.views.decorators.csrf import csrf_exempt
import qrcode
import base64
import StringIO
import requests

# Create your views here.
@csrf_exempt
def gen_prop(request):
    #generate prototype
    # print request.body
    # if request.POST:
    result = dict()
    try:
        data = json.loads(request.body)
        pt = Prototype()
        try:
            merchant = MainUser.objects.get(id=data['merchant_id'])
        except:
            return HttpResponse("error", status=500)

        pt.merchant = merchant
        ist = pytz.timezone("Asia/Kolkata")
        pt.key = hashlib.md5(str(datetime.datetime.now(tz=ist))+"42HACKSTREET").hexdigest()
        pt.save()

        qr_data = dict()
        qr_data['merchant'] = merchant.name
        qr_data['address'] = merchant.address
        qr_data['key'] = pt.key
        qr_data['type'] = 1
        qr_data['products'] = []

        for p in data['products']:
            name = p['name']
            sku = p['sku']
            manufacturer = p['manufacturer']
            price = p['price']
            currency = p['currency']
            desc = p['desc']
            quantity = p['quantity']
            pd = Product()
            pd.name = name
            pd.sku = sku
            pd.manufacturer = manufacturer
            pd.price = Decimal(price)
            pd.currency = currency
            pd.desc = desc
            pd.prototype = pt
            pd.quantity = quantity
            pd.save()
            qr_data['products'].append({
                'name': name,
                'price': "{0:.2f}".format(pd.price),
                'quantity': quantity,
                'currency': currency
            })
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(json.dumps(qr_data)))
        qr.make(fit=True)
        img = qr.make_image()
        output = StringIO.StringIO()
        img.save(output, 'GIF')
        contents = output.getvalue()
        data = base64.b64encode(contents)
        result['status'] = 'success'
        result['data'] = data
        return HttpResponse(json.dumps(result))
    except Exception,e:
        print e
    result['status'] = 'error'
    return HttpResponse(json.dumps(result), status=500)


@csrf_exempt
def gen_trans(request):
    result = dict()
    try:
        data = json.loads(request.body)
        pt = Prototype()
        try:
            merchant = MainUser.objects.get(id=data['user_id'])
        except:
            return HttpResponse("error", status=500)
        pt.merchant = merchant
        ist = pytz.timezone("Asia/Kolkata")
        pt.key = hashlib.md5(str(datetime.datetime.now(tz=ist))+"42HACKSTREET").hexdigest()
        pt.save()
        pti = PersonalTransfer()
        pti.amount = Decimal(data['amount'])
        pti.currency = data['currency']
        pti.description = data['description']
        pti.prototype = pt
        pti.save()
        #generate QR CODE
        qr_data = dict()
        qr_data['receiver'] = merchant.name
        qr_data['type'] = 2
        qr_data['amount'] = "{0:.2f}".format(pti.amount)
        qr_data['currency'] = pti.currency
        qr_data['description'] = pti.description
        qr_data['key'] = pt.key
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(json.dumps(qr_data)))
        qr.make(fit=True)
        img = qr.make_image()
        output = StringIO.StringIO()
        img.save(output, 'GIF')
        contents = output.getvalue()
        data = base64.b64encode(contents)
        result['status'] = 'success'
        result['data'] = data
        return HttpResponse(json.dumps(result))
    except Exception,e:
        print e
    result['status']='error'
    return HttpResponse(json.dumps(result), status=500)


def gcm_push_message():
    url = 'https://gcm-http.googleapis.com/gcm/send'
    key = 'AIzaSyDFDd13x1XaM5iPRj7Y7tXwzNCv-ZnFQYY'

    payload = {
        'data' : { 'message' : 'hello' },
        'to' : 'dq2NrwgkvuE:APA91bHYkyySv336pwYnQbHJ2u_s6VyvLk3qSdcjtTZI2Sj5Gf_nXZmX96YTS435m7BTdrFWhTfyiYvGWlKoweWZD-_x8QOFPnM-bpmpIJgkHMjed4ALqSDNH8jRSShZJ9FKssfU-BhV'
    }

    r = requests.post(url,data=json.dumps(payload),auth=('key','AIzaSyDFDd13x1XaM5iPRj7Y7tXwzNCv-ZnFQYY'))

    print r.text