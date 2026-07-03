import redis
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

r=redis.Redis(host='localhost', port=6379)

class customratelimit:
    def __init__(self,get_response):
        self.get_response=get_response
        self.limit=30
        self.window=60
        
    def __call__(self,request):
        ip=self.get_client_ip(request)
        key=f"rate_limit:{ip}"
        
        current= r.incr(key)
        print("run")
        
        if current==1:
            r.expire(key,self.window)
        if current > self.limit:
            return JsonResponse({"error":"rate limit exceeded"},status=status.HTTP_429_TOO_MANY_REQUESTS)
            
        return self.get_response(request)
        
    
    def get_client_ip(self,request):
        x_forwarded=request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')