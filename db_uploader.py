import os, django, csv, sys
from optparse import OptionParser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaka0Adult.settings')
django.setup()

from users.models import User
from products.models import Product, Category, Character, ImageUrl

CSV_PATH_CATEGORY = './csv/categories.csv'
CSV_PATH_CHARACTER = './csv/characters.csv'
CSV_PATH_USER = './csv/users.csv'
CSV_PATH_PRODUCT = './csv/products.csv'
CSV_PATH_PRODUCT_IMAGE = './csv/product_images.csv'

def delete_table_records():
    Category.objects.all().delete()
    Character.objects.all().delete()
    ImageUrl.objects.all().delete()
    Product.objects.all().delete()
    User.objects.all().delete()

def create_table_records():
    with open(CSV_PATH_CATEGORY, mode='r') as csv_file:
        rows = csv.reader(csv_file, delimiter = ',',)
        next(rows)
        categories = [Category(id=row[0], name=row[1]) for row in rows]
        Category.objects.bulk_create(categories)


    with open(CSV_PATH_CHARACTER, mode='r') as csv_file:
        rows = csv.reader(csv_file, delimiter = ',')
        next(rows)
        characters = [Character(id=row[0], name=row[1]) for row in rows]
        Character.objects.bulk_create(characters)

    with open(CSV_PATH_USER, mode='r') as csv_file:
        rows = csv.reader(csv_file, delimiter = ',')
        next(rows)
        users = [User(id=row[0], nickname=row[1], email=row[2], password=row[3], phone_number=row[4], gender=row[5], birth=row[6]) for row in rows]
        User.objects.bulk_create(users)

    with open(CSV_PATH_PRODUCT, mode='r') as csv_file:
        rows = csv.reader(csv_file, delimiter = ',')
        next(rows)
        products = [Product(id=row[0], category=Category.objects.get(id=row[1]), character=Character.objects.get(id=row[2]), name=row[3], stock=row[4], sell_count=row[5], price=row[6], content=row[7], created_at=row[8]) for row in rows]
        Product.objects.bulk_create(products)

    with open(CSV_PATH_PRODUCT_IMAGE, mode='r') as csv_file:
        rows = csv.reader(csv_file, delimiter = ',')
        next(rows)
        products = [ImageUrl(id=row[0], product=Product.objects.get(id=row[1]), url=row[2]) for row in rows]
        ImageUrl.objects.bulk_create(products)


if __name__ == '__main__':
    use = 'Usage: %prog [options]'
    parser = OptionParser(usage=use)
    parser.add_option("-d", "--delete", dest="delete", action="store_true", help="delete record of tables", default=False)
    parser.add_option("-c", "--create", dest="create", action="store_true", help="create record of tables", default=False)
    (options, args) = parser.parse_args()

    if(len(sys.argv) <= 1): 
        parser.print_help()
        exit()

    if options.delete:
       delete_table_records()
    
    if options.create:
        create_table_records()