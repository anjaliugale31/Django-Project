from blog.models import Post
from django.contrib.auth.models import User

from django.core.management.base import BaseCommand
import requests
from pyquery import PyQuery 
from django.utils import timezone


class Command(BaseCommand):
    help = 'scrapping the pages by there indexes '

    def add_arguments(self, parser):
        parser.add_argument('page-number', nargs='+', type=int)

    #command line index handled 
    def handle(self, *args, **options):
        page_no=options['page-number'][0]
        count=0
        request1=requests.get('https://www.tutorialspoint.com/python3/index.htm')
        html=PyQuery(request1.text)   #created pyquery object
        pages=list(html(".chapters a").items())  #scraped all html Anchor tag
        total_pages=len(pages)
        all_data=[]
        for tag in range(total_pages):
            if(count<page_no):
                each_page=requests.get('https://www.tutorialspoint.com'+pages[tag].attr('href'))
                each_html=PyQuery(each_page.text)
                title_html=each_html(".tutorial-content h1").text()
                text_each=each_html(".tutorial-content")
                text_each("h1").remove()
                text_each("#google-top-ads").remove()
                text_each('.google-bottom-ads').remove()
                text_each('#bottom_navigation').remove()
                text_each('.tutorial-menu').remove()
                text_each('.button-borders').remove()
                text_val=text_each.text()
                
                text_img=each_html(".cover img").attr("src")

                if(text_img):
                    img_name=each_html(".cover img").attr("src").split("/")[-1]
                    img_url="https://www.tutorialspoint.com"+text_img

                    # one way by downloading image
                    # image_filename = wget.download(img_url,"media/documents")
                    # print(image_filename)

                    # 2nd way by creating new directory and displaying the image 
                    with open('media/documents/'+img_name,'wb') as img_file:
                        image=requests.get(img_url)
                        img_file.write(image.content)
                if(Post.objects.filter(title=title_html)):
                    # print("Already in database")
                    continue
                else:
                    scraped_data=Post(author=User.objects.get_or_create(username="demo")[0],
                    title=title_html,
                    text=text_val,
                    published_date=timezone.now(),
                    image_file="/documents/"+img_name if text_img else None)
                    all_data.append(scraped_data)
                    count+=1
        Post.objects.bulk_create(all_data)
        #condition for 
        if(count>0):
            print("Number of pages scrap :",count)
        else:
            print("All pages scrap")





