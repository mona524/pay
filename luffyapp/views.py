from django.shortcuts import render,redirect,HttpResponse
from Alipay.src.alipay import AliPay
from Alipay.config.settings import AliPayConfig
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def pay(request):
    if request.method == 'POST':
        notify_url = 'http://192.168.137.124:8090/payedpage/'
        return_url = 'http:192.168.137.124:8090/payedpage/'
        money= request.POST.get('money')

        alipay = AliPay(appid=AliPayConfig.app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=AliPayConfig.merchant_private_key_path,
        alipay_public_key_path=AliPayConfig.alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True)

        # 生成支付的url
        query_params = alipay.direct_pay(
            subject="ipad",  # 商品简单描述
            out_trade_no="asdfasdfa",  # 商户订单号
            total_amount=float(money),  # 交易金额(单位: 元 保留俩位小数)
        )

        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

        return redirect(pay_url)

    return render(request,'paypage.html')

def payedpage(request):
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号

        app_id = "2016082500309412"
        # POST
        notify_url = "http://192.168.137.124:8090/page2/"
        # GET
        return_url = "http://192.168.137.124:8090/page2/"

        merchant_private_key_path = "keys/pri"
        alipay_public_key_path = "keys/pub"

        alipay = AliPay(
            appid=app_id,
            app_notify_url=notify_url,
            return_url=return_url,
            app_private_key_path=merchant_private_key_path,
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            debug=True,  # 默认False,
        )

        process_dict = json.loads(request.body.decode('utf-8'))
        sign = process_dict.pop('sign', '')
        result = alipay.verify(process_dict, sign)
        if result:
            # 验证成功
            return HttpResponse('支付成功')
        else:
            # 验证失败
            return HttpResponse('支付失败')








