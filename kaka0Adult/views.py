from django.http import HttpResponse
from kaka0Adult.settings.base import get_aws_linux_ec2_private_ip

def index(request):
     ip = get_aws_linux_ec2_private_ip()
     return HttpResponse(f"""
 <!DCOTYPE html>
    <html lang="ko">

    <head>
        <title>Wecode 21기 고생많으셨습니다. </title>
    </head>

    <body>
          <H1> 21기 여러분 3개월동안 고생많으셨습니다!! 👍</H1>
    </body>

    </html>
     """
     )