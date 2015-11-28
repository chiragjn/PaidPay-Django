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
import time
from gcm import GCM
from django.http import JsonResponse
import hmac
import random

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


def gcm_push_message(message,topic,reg_id):
    # url = 'https://gcm-http.googleapis.com/gcm/send'
    # key = 'AIzaSyDFDd13x1XaM5iPRj7Y7tXwzNCv-ZnFQYY'
    # payload = {
    #     'data' : { 'message' : 'hello' },
    #     'to' : 'dq2NrwgkvuE:APA91bHYkyySv336pwYnQbHJ2u_s6VyvLk3qSdcjtTZI2Sj5Gf_nXZmX96YTS435m7BTdrFWhTfyiYvGWlKoweWZD-_x8QOFPnM-bpmpIJgkHMjed4ALqSDNH8jRSShZJ9FKssfU-BhV'
    # }
    # headers = {'Content-Type': 'application/json', 'Authorization': key}
    # r = requests.post(url,data=json.dumps(payload),headers=headers)
    #
    # print r.text
    # topic = 'paren'
    # message = 'teats'
    gcm = GCM('AIzaSyDFDd13x1XaM5iPRj7Y7tXwzNCv-ZnFQYY')
    data = {'topic': topic,'message': message}
    # reg_id = ['cnC55gD0PXY:APA91bEeEZYDAsRGfVElz3BSudnCOsXJ9qwTjVzlsKiEvUopZIT7XKOlNwnLEckc-Kg05k4W4icXhpCjKGTl5M-uRelT_1iPk9nx6DX0gUqWBcNa7tuN9AaQ5dBJF7TLAnOVDPeK4m9u']
    response = gcm.json_request(registration_ids=reg_id, data=data)
    print response


def citrus_bill_generator(request):
    access_key = 'SU21NGP0DRCE73DXSDFA'
    secret_key = '99840bf4d61c8942ef6325bbb1ec48e9ded25faa'
    return_url = 'http://49.248.127.26:1235/returnbill'
    value = request.GET['amount']
    txnid = str(int(time.time())) + str(int(random.random() * 99999) + 10000);
    data_string = ('merchantAccessKey=' + access_key +
                  '&transactionId=' + txnid +
                  '&amount=' + value)
    signature = hmac.new(secret_key, data_string, hashlib.sha1).hexdigest()
    amount = {"value" : value, "currency": 'INR'}
    bill = {
            "merchantTxnId": txnid,
            "amount": amount,
            "requestSignature": signature,
            "merchantAccessKey": access_key,
            "returnUrl": return_url
    }
    print "chillies"
    return JsonResponse(bill)


@csrf_exempt
def citrus_return_url(request):
    secret_key = '99840bf4d61c8942ef6325bbb1ec48e9ded25faa'
    print "lol"
    if request.method == 'POST':
        data_string = (request.POST.get('TxId') + request.POST.get('TxStatus') +
                      request.POST.get('amount') + request.POST.get('pgTxnNo') +
                      request.POST.get('issuerRefNo') + request.POST.get('authIdCode') +
                      request.POST.get('firstName') + request.POST.get('lastName') +
                      request.POST.get('pgRespCode') + request.POST.get('addressZip'))

        signature = hmac.new(secret_key, data_string, hashlib.sha1).hexdigest()
        print "hsgjskdf"
        if signature == request.POST.get('signature'):
            print "herebitch"
            return HttpResponse("<body>Done")
        else:
            error = { "error" : "Transaction Failed", "message": "Signature Verification Failed" }


def test_ret(request):
    return render(request,'test.html')