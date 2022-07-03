from flask import Flask, request
import json
import pandas as pd

masterlocations = pd.read_csv('/Users/joshvasilvasstar/Documents/clinicchat/tests/webhook_python/locations.csv')
zipcodes = pd.read_csv('/Users/joshvasilvasstar/Documents/clinicchat/tests/webhook_python/zip_lat_long.csv')

from math import radians, cos, sin, asin, sqrt
def dist(lat1, long1, lat2, long2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    # haversine formula 
    dlon = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c *0.621371
    return km

# https_tunnel = ngrok.connect()

app = Flask(__name__)
# run_with_ngrok(app)

@app.route('/',methods=["POST","GET" ])



def webhook() :
    if request. method == "GET":
        return "Hello YouTube!Not connerted to I-"
    elif request.method == "POST":
        payload = request.json
        print (payload)
        requestedZip=payload['variable']
        lat,long = zipcodes[zipcodes['zip']==requestedZip]['lat'], zipcodes[zipcodes['zip']==requestedZip]['long']
        locations = masterlocations.copy()
        locations['distances'] = locations.apply(lambda row: dist(lat, long, row['lat'], row['long']), axis=1)
        three_closest=locations.sort_values(by=['distances']).reset_index().loc[:2,:]
        three_closest['ans'] = three_closest['NAME']+'. '+three_closest['url']
        respo = 'Three nearest locations near you are: \n\n' + "\n".join(three_closest['ans'].to_list()) 
        value = {
  "output": {
    "generic":[
      {
        "response_type": "text",
        "values": [
          { "text": respo }
        ],
        "selection_policy": "random"
      }
    ]
  }
}
        
        print(type(value))
        return value
    else:
        print(request.data)
        return "200"


if __name__=='__main__':
    app.run(debug=True)
