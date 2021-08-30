from django.core.management.base import BaseCommand, CommandError
import requests
from pyquery import PyQuery 
from blog.models import Post
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count
import urllib
import wget
from glob import glob



class Command(BaseCommand):
    help = 'scrapping the pages by index '

    def add_arguments(self, parser):
        parser.add_argument('page-number', nargs='+', type=int)


    def handle(self, *args, **options):
        page_no=options['page-number'][0]
        count=0
        request1=requests.get('https://www.tutorialspoint.com/python3/index.htm')
        html=PyQuery(request1.text)   #created pyquery object
        pages=list(html(".chapters a").items())
        total_pages=len(pages)
        all_data=[]
        for tag in range(total_pages):
            if(count<page_no):
                each_page=requests.get('https://www.tutorialspoint.com'+pages[tag].attr('href'))
                each_html=PyQuery(each_page.text)
                title_html=each_html(".tutorial-content h1").text()
                text_each=each_html(".tutorial-content p").text() 
                text_img=each_html(".cover img").attr("src")
                # File_image=glob(text_img+"*.jpg")

                if(text_img):
                    img_name=each_html(".cover img").attr("src")
                    img_url="https://www.tutorialspoint.com"+text_img
                    image_filename = wget.download(img_url,"media/documents")

                    with open('media/documents'+img_name,'wb') as img_file:
                        image=requests.get(image_filename)
                        img_file.write(image.content)
                if(Post.objects.filter(title=title_html)):
                    print("Already in database")
                    break
                else:
                    scraped_data=Post(author=User.objects.get_or_create(username="demo")[0],
                    title=each_html(".tutorial-content h1").text(),
                    text=each_html(".tutorial-content p").text(),
                    published_date=timezone.now(),
                    image_file=img_name if text_img else None)
                    all_data.append(scraped_data)
                    count+=1
        Post.objects.bulk_create(all_data)





