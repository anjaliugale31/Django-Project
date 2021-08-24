from django.core.management.base import BaseCommand, CommandError
import requests
from pyquery import PyQuery

class Command(BaseCommand):
    help = 'scrapping the pages by index '

    def add_arguments(self, parser):
        parser.add_argument('page-number', nargs='+', type=int)

    def handle(self, *args, **options):
        page_no=options['page-number']
        # print(page_no)
        lst=[]
        request1=requests.get('https://www.tutorialspoint.com/python3/index.htm')
        html=PyQuery(request1.text)
        # print(html)

        # for i in html.items('a'):
        #     lst.append(i)
        # print(lst)