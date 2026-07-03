from rest_framework.views import APIView
from rest_framework.response import Response
from user_records.models import CustomUser_details
from user_records.serializers import user_serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from rest_framework.generics import GenericAPIView,ListAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from category.models import event_category
from category.serializers import category_serializer
from event.models import Event
from event.serializers import EventSerializer
from event.isowner import IsOwner,myregistered
from rest_framework import viewsets
from registration.models import Registration
from registration.serializers import RegistrationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import redis
import pika
from .task import generate_invoice_task
from django.http import FileResponse
from invoice.models import Invoice
from rest_framework.decorators import action

r=redis.Redis(host='localhost',port=6379)
class user_api(APIView):
    def get(self, request,pk=None,format=None):
        if pk:
            obj=CustomUser_details.objects.get(pk=pk)
            serializer=user_serializer(obj)
            return Response(serializer.data)
            
        obj=CustomUser_details.objects.all()
        serializer=user_serializer(obj,many=True)
        return Response(serializer.data)
        
    def post(self,request):
        serializer=user_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':"data saved"})
        return Response(serializer.errors)
    def patch(self,request,pk=None,format=None):
        obj=CustomUser_details.objects.get(pk=pk)
        if not obj:
            return Response({"msg":"not found"})
        serializer=user_serializer(obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"updated record"})
        return Response(serializer.errors)
        
    def delete(self, request, pk=None,format=None):
        obj=CustomUser_details.objects.get(pk=pk)
        obj.delete()
        return Response({"msg":"deleted record"})
        
class listcategories(GenericAPIView,ListModelMixin,CreateModelMixin):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=event_category.objects.all()
    serializer_class= category_serializer
    def get(self,request):
        return self.list(request)
        
    def post(self,request):
        return self.create(request)
        
class listevent(ListAPIView,CreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Event.objects.all()
    serializer_class=EventSerializer
    
class myevent(ListAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Event.objects.all()
    serializer_class=EventSerializer

        
class modifyevent(RetrieveUpdateDestroyAPIView):
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsOwner]
    queryset=Event.objects.all()
    serializer_class=EventSerializer
    lookup_field="slug"
    
    
class Register(viewsets.ViewSet):
    authentication_classes=[SessionAuthentication]
    permission_classes=[myregistered]
    def list(self,request):
        d=Registration.objects.filter(user=request.user)
        serializer=RegistrationSerializer(d,many=True)
        return Response(serializer.data)
    def retrieve(self,request,pk=None):
        d=Registration.objects.get(pk=pk,user=request.user)
        serializer=RegistrationSerializer(d)
        return Response(serializer.data)
    def create(self,request):
        info=request.data
        serializer=RegistrationSerializer(data=info)
        if serializer.is_valid():
            request.session['reg_detail']=info
            instance=serializer.save()
            
            return Response({'msg':'details saved','context':RegistrationSerializer(instance).data})
        return Response(serializer.errors)
    
    def destroy(self, request,pk=None):
        d=Registration.objects.get(pk=pk)
        d.delete()
        return Response({'msg':"data deleted"})
        
        
    @action(detail=True, methods=["get"],)
    def check_in(self,request,pk=None):
        reg=Registration.objects.get(pk=pk,event__organizer__id=request.user.pk)
        reg.check_in()
        return Response({'detail': 'Checked in'})
    @action(detail=True, methods=["get"])
    def cancel(self,request,pk=None):
        reg=Registration.objects.get(pk=pk)
        reg.cancel()
        return Response({'detail': 'Cancelled. Waitlist promoted if applicable.'})

class DownloadInvoice(APIView):

    def get(self, request, invoice_id):
        invoice = Invoice.objects.get(id=invoice_id, user=request.user)

        return FileResponse(
            invoice.file.open('rb'),
            as_attachment=True,
            filename=f"invoice_{invoice.created_at}.pdf"
        )
        
import razorpay
from django.conf import settings
from payments.models import Payment
class CreateOrderView(APIView):
    def post(self, request):
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        pk = int(request.data.get('_id'))
        e=Registration.objects.get(id=pk)
        amount=e.amount_to_pay*100
        
        order_data = {
            "amount": int(amount),
            "currency": "INR",
            "payment_capture": 1
        }

        order = client.order.create(data=order_data)
        e.order_id=order["id"]
        e.save()
       # Payment.objects.create(order_id=order['id'],amount=order['amount'])

        return Response({
            "order_id": order["id"],
            "amount": order["amount"],
            "key": settings.RAZORPAY_KEY_ID,
        })
        
class VerifyPaymentView(APIView):
    def get(self,request):
        client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
    
        data = request.data
    
        params_dict = {
        "razorpay_order_id": data.get("razorpay_order_id"),
        "razorpay_payment_id": data.get("razorpay_payment_id"),
        "razorpay_signature": data.get("razorpay_signature"),
        }
    
        try:
            client.utility.verify_payment_signature(params_dict)
    
            obj = Registration.objects.get(order_id=data.get("razorpay_order_id"))
            #obj = Registration.objects.get(order_id='order_T8I54x5y1e7SpV')

            payment = Payment.objects.create(
            order_id=data.get("razorpay_order_id"),
            payment_id=data.get("razorpay_payment_id"),
            signature=data.get("razorpay_signature"),
            status="success",
            registration=obj,
            amount=obj.amount_to_pay
            )
            obj.paid = True
            obj.save()
            task = generate_invoice_task.delay(request.user.id, RegistrationSerializer(obj).data)
            return Response({"status": "Payment successful","invoice_task":task.id,'registration_details':RegistrationSerializer(obj).data})
    
        except Exception as e:
            return Response({
            "status": "Payment failed",
            "error": str(e)
            }, status=400)