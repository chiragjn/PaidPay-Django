from django.shortcuts import render
import json
from django.http import HttpResponse
from decimal import *
import hashlib
import datetime
import pytz
from app.models import Product, Prototype, MainUser, PersonalTransfer, Transaction
from django.views.decorators.csrf import csrf_exempt
import qrcode
import base64
import StringIO
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
        # data = json.loads(request.body)
        pt = Prototype()
        try:
            merchant = MainUser.objects.get(id=request.POST['user_id'])
        except:
            return HttpResponse("error", status=500)
        pt.merchant = merchant
        ist = pytz.timezone("Asia/Kolkata")
        pt.key = hashlib.md5(str(datetime.datetime.now(tz=ist))+"42HACKSTREET").hexdigest()
        pt.save()
        pti = PersonalTransfer()
        pti.amount = Decimal(request.POST['amount'])
        pti.currency = request.POST['currency']
        pti.description = request.POST['description']
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


@csrf_exempt
def complete_transaction(request):
    try:
    # print request.body
    # data = json.loads(request.body)['json']
        if request.POST:
            consumer = request.POST.get('user_id')
            useracc = MainUser.objects.get(id=consumer)
            key = request.POST.get('key')
            prototype = Prototype.objects.get(key=key)
            type = request.POST.get('type')
            mode = request.POST.get('mode')
            ## type 1 is merchant and type 2 is personal and mode 2 is self
            if type == 1:
                products = Product.objects.filter(prototype=prototype)
                merchant = prototype.merchant
                total = Decimal(0)
                for p in products:
                    total += p.quantity*p.price
                merchant.balance += total
                merchant.save()
                ts = Transaction()
                ts.prototype = prototype
                ts.customer = useracc
                ts.status = 1
                ts.mode = mode
                ts.save()
                if mode == 2:
                    useracc.balance -= total
                    useracc.save()
            else:
                pt = PersonalTransfer.objects.filter(prototype=prototype)
                receiver = prototype.merchant
                sender = useracc
                total = Decimal(0)
                for p in pt:
                    total += p.amount
                receiver.balance += total
                receiver.save()
                ts = Transaction()
                ts.prototype = prototype
                ts.customer = useracc
                ts.status = 1
                ts.mode = mode
                ts.save()
                if mode == 2:
                    useracc.balance -= total
                    useracc.save()
                gcm_push_message("You've received funds in your paypaid account!","You have got funds!",receiver.gcm)
    except Exception,e:
        print e
        return HttpResponse("error",status=400)
    return HttpResponse("done")

@csrf_exempt
def history(request):
    try:
        if request.POST:
            user_id = request.POST.get('user_id')
            print user_id
            useracc = MainUser.objects.get(id=user_id)
            #get transactions done by user
            ts = Transaction.objects.filter(customer=useracc)
            # get requests by user
            ps = Prototype.objects.filter(merchant=user_id)
            val = []
            for p in ps:
                k = Transaction.objects.filter(prototype=p)
                if k:
                    val.append(p)
            ## amount, date, + or - , payee
            tx = []
            for v in val:
                products = Product.objects.filter(prototype=v)
                total = Decimal(0)
                for p in products:
                        total += p.quantity*p.price
                pt = PersonalTransfer.objects.filter(prototype=v)
                for p in pt:
                        total += p.amount
                tx.append(["{0:.2f}".format(total),v.created_at.strftime("%d/%m/%y"),-1,v.merchant.name])
            px = []
            for j in ps:
                tsx = Transaction.objects.filter(prototype=j)
                if tsx:
                    products = Product.objects.filter(prototype=j)
                    total = Decimal(0)
                    for p in products:
                            total += p.quantity*p.price
                    pt = PersonalTransfer.objects.filter(prototype=j)
                    for p in pt:
                            total += p.amount
                    px.append(["{0:.2f}".format(total),j.created_at.strftime("%d/%m/%y"),+1,tsx[0].customer.name])

            return HttpResponse(json.dumps({'plus':px,'minus':tx}))
        #val contains successful receipts by user
    except Exception,e:
        print e
        return HttpResponse("Error")
    return HttpResponse("Done")


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
    response = gcm.json_request(registration_ids=[reg_id], data=data)
    print response


def citrus_bill_generator(request):
    access_key = 'SU21NGP0DRCE73DXSDFA'
    secret_key = '99840bf4d61c8942ef6325bbb1ec48e9ded25faa'
    return_url = 'https://morning-reaches-5621.herokuapp.com/returnbill'
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
            return HttpResponse("< body>")
        else:
            error = { "error" : "Transaction Failed", "message": "Signature Verification Failed" }


def test_ret(request):
    return render(request,'test.html')

def cart(request):
    return render(request,'cart.html')