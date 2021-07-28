from django.http import HttpResponse
from kaka0Adult.settings.base import get_aws_linux_ec2_private_ip

def index(request):
     ip = get_aws_linux_ec2_private_ip()
     return HttpResponse(f"Hello, world\nyour private ip is {ip}")