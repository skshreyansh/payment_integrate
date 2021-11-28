from django.shortcuts import render
import razorpay
# Create your views here.

from .models import Coffee
from django.views.decorators.csrf import csrf_exempt


def home(request):
    if request.method=="POST":
        name=request.POST.get("name")
        amount=int(request.POST.get("amount")) * 100
        client=razorpay.Client(auth=("rzp_test_DIn55o1zR6YHCx","ZwhgZL83K4jQS6wqKozxLtNG"))
        payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        coffee=Coffee(name=name,amount=amount,payment_id=payment['id'])
        print(payment)
        coffee.save()
        return render(request,"index.html",{'payment':payment})
        # print(name)
        # print(amount)
    return render(request,"index.html")

@csrf_exempt
def success(request):
    if request.method=="POST":
        a=request.POST
        print(a)
        order_id=""
        for key ,val in a.items():
            if key=="razorpay_order_id":
                order_id=val
                break
        user=Coffee.objects.filter(payment_id=order_id).first()
        user.paid=True
        user.save()
    return render(request,"success.html")