from django.test    import TestCase, Client
from rest_framework import status

from .models import User

class UserTest(TestCase):
    def setUp(self):
        User.manager.create_user(
            nickname     = '김코딩',
            phone_number = '01012345678',
            email        = 'coding@gmail.com',
            password     = '12345678',
            gender       = '남자',
            birth        = '1993.05.01')

    def tearDown(self):
        User.objects.all().delete();

    def test_signup_success(self):
        client = Client()

        body = {
                'nickname'    : '이코드',
                'phone_number': '01098765432',
                'email'       : 'coding2@gmail.com',
                'password'    : '12345678',
                'gender'      : '여자',
                'birth'       : '1995.05.01'
            }

        response = client.post('/users/signup', body)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_failed_dueto_duplicated_nickname(self):
        client = Client()

        body = {
                'nickname'    : '김코딩',
                'phone_number': '01098765432',
                'email'       : 'coding2@gmail.com',
                'password'    : '12345678',
                'gender'      : '여자',
                'birth'       : '1995.05.01'
            }

        response = client.post('/users/signup', body)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_signup_failed_dueto_duplicated_email(self):
        client = Client()

        body = {
                'nickname'    : '김코딩',
                'phone_number': '01098765432',
                'email'       : 'coding@gmail.com',
                'password'    : '12345678',
                'gender'      : '남자',
                'birth'       : '1995.05.01'
            }

        response = client.post('/users/signup', body)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


    def test_signup_failed_dueto_duplicated_phone_number(self):
        client = Client()

        body = {
                'nickname'    : '이코순',
                'phone_number': '01012345678',
                'email'       : 'cosoon@gmail.com',
                'password'    : '12345678',
                'gender'      : '여자',
                'birth'       : '1995.05.01'
            }

        response = client.post('/users/signup', body)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_signup_failed_dueto_leak_user_info(self):
        client = Client()

        body = {
                'nickname'    : '이코순',
            }

        response = client.post('/users/signup', body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_signup_failed_dueto_invalid_email(self):
        client = Client()

        body = {
                'nickname'    : '이코순',
                'phone_number': '01098765431',
                'email'       : 'cosoongmail.com',
                'password'    : '12345678',
                'gender'      : '여자',
                'birth'       : '1995.05.01'
            }

        response = client.post('/users/signup', body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message':'THE_EMAIL_IS_NOT_APPROPRIATE'})

    def test_signup_failed_dueto_invalid_password(self):
        client = Client()

        body = {
                'nickname'    : '이코순',
                'phone_number': '01098765431',
                'email'       : 'cosoon@gmail.com',
                'password'    : '1234',
                'gender'      : '여자',
                'birth'       : '1995.05.01'
            }

        response = client.post('/users/signup', body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message':'THE_PASSWORD_IS_NOT_APPROPRIATE'})