# Create your views here.
import json
import bs4
import requests
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from myapi.models import LinkItem

@csrf_exempt
def getResponse(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        linkAmazon = json_data['link']
        print(linkAmazon)
        item = LinkItem.objects.get(linkAmazon=linkAmazon)
        ingredients = scrapPage(item)

        response = {
            "name": item.productName,
            "ingredients": ingredients,
            "error": False
        }
        return JsonResponse(response, safe=False)
        """
        try:
            
        except:
            response = {
                "message": "Error occured",
                "error": True
            }
            return JsonResponse(response, safe=False)
        """

def removeBefore(str):
    return re.sub(r'^.*?Ingrédients', 'Ingrédients', str)
def removeN(str):
     return "".join(c for c in str if c not in ('\x95','\n','/','.',';',',','*',':','+'))

def split_sentence(sentence):
    return re.split(' ',sentence)

def remove_space(sentence):
    return ' '.join(sentence.split())

def scrapPage(item):
    url = item.linkBeauty
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    box = soup.select_one(
        "#page > div > div.row > div.bt__container__product > main > div > div.col-xs-12 > div:nth-child(6) > div:nth-child(4) > h2 > div").parent.parent.getText()
    box2 = removeN(box)
    box3 = box2.replace('Formule', '')
    regex = re.compile(".*?\((.*?)\)")
    box4 = re.findall(regex, box3)
    if(len(box4)>0):
        box5 = box3.replace('(' + box4[0] + ')', '')
    else:
        box5=box3
    box6 = box5.replace('Voir les fiches composants','')
    box7 = remove_space(box6)
    tab = split_sentence(box7)
    return tab