import bcrypt

from django.db.models import Manager, Q 

class ProductManager(Manager):
    def is_duplicated_user_info(self, nickname, email, phone_number):
        return self.get_queryset().filter(
            Q(nickname = nickname)| Q(email = email) |
            Q(phone_number = phone_number)).exists()
    
    def create_user(self, **user):
        user['password'] = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        return self.get_queryset().create(**user)