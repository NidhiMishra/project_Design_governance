import asyncio
from aiohttp import web
from aiohttp.web import json_response
import aiohttp_cors

import random
import string

letters = string.ascii_lowercase
color=['Blond','red','brown','white']
beers=[]
breweries=[]
counter =0
for i in range(10):
    tmpBrewery = {
        "id": i,
        "name":'brewery_'+str(i),
        "adresse":'adresse '+str(i),
        "breweryBeer": []
    }
    for beer in range(11,22,2):
        beerObject = {
           "brewery": tmpBrewery["id"],
           "id": counter,
           "name":  ''.join(random.choice(letters) for i in range(10)),
           "color": random.choice(color),
           "alcool":random.randint(1, 10),
           "quantity":random.randint(1,200),
           "price": random.randint(1,20)
       }
        tmpBrewery["breweryBeer"].append(beerObject)
        beers.append(beerObject)
        counter+=1
    breweries.append(tmpBrewery)

def getAllBeers(request):
    return json_response(data=beers)

def getAllBreweries(request):
    return json_response(data=breweries)

async def createOrder(request):
    data = await request.json()
    order = {
        "id": random.randint(1, 1000),
        "restaurant": random.randint(1, 1000),
        "beers": [],
    }
    for el in data:
        order['beers'].append(el)
    print(order)
    return web.Response()

def getBeersForBrewery(request):
     id = int(request.match_info['id'])
     brewery = breweries[id]
     return json_response(data=brewery['breweryBeer'])

async def createBeer(request):
     data = await request.json()
     beer = {
         "brewery": data["brewery"],
         "id": random.randint(1, 1000),
         "name":  data["name"],
         "color": data["color"],
         "alcool":data["alcool"],
         "quantity": data["quantity"],
         "price": data["price"]
     }
     print(beer)
     breweries[data["brewery"]]["breweryBeer"].append(beers)
     return web.Response()

def getNoManyBeers(request):
    id = int(request.match_info['id'])
    tmpBeers = breweries[id]["breweryBeer"]
    tr =[]
    for beer in tmpBeers:
      if (beer["quantity"] < 50):
          tr.append(beer)
    return json_response(data=tr)



app = web.Application()

# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*",
        )
})

cors.add(app.router.add_get('/beers', getAllBeers))
cors.add(app.router.add_get('/breweries', getAllBreweries))
cors.add(app.router.add_post('/order', createOrder))
cors.add(app.router.add_get('/beers/{id:\d+}', getBeersForBrewery))
cors.add(app.router.add_post('/add', createBeer))
cors.add(app.router.add_get('/noMany/{id:\d+}', getNoManyBeers))



web.run_app(app, port=8080)
