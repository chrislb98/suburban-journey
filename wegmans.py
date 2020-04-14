import requests
import sys
import json
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Get the anonymous session cookie with location data
def get_cookie():

    getcookie_url = "https://shop.wegmans.com/api/v2/user_sessions"
    getcookie_url2 = "https://shop.wegmans.com/api/v2/users"
    cookie_json = {"binary":"web-ecom","binary_version":"2.25.122","is_retina":False,"os_version":"Win32","pixel_density":"2.0","push_token":"","screen_height":1080,"screen_width":1920}
    
    #send first request to get an Authorization Bearer header token
    response = requests.post(getcookie_url, json=cookie_json)
    data=json.loads(response.content)
    #print ("Acquired cookie %s") % data["session_token"]
    
    #send the second request to get the api key
    response = requests.post(getcookie_url2, headers={"Authorization":"Bearer " + data["session_token"]})
    #print ("Acquired api key %s") % response.cookies['session-prd-weg']
    return(response.cookies['session-prd-weg'])
    
	
#Get store list based on provided state
def get_stores(province, cookie):
    getstores_url = "https://shop.wegmans.com/api/v2/stores?_nocache=1586788268363&show_ecommerce=true&show_pickup=true"
    
    #pull the stores
    response = requests.get(getstores_url)
    data=json.loads(response.content)
    
    #iterate through each store
    for item in data['items']:
        if item["address"]["province"] == province:
            if item["has_pickup"] == True:
                print("Address: %s") % item["address"]["address1"]
                get_timeslots(item["id"], cookie)



#Get timeslots the selected store
def get_timeslots(id, cookie):
    storeselect_url = "https://shop.wegmans.com/api/v2/user"
    timeslots_url = "https://shop.wegmans.com/api/v2/timeslots"
    cookies = {'session-prd-weg':cookie}
    store_json = {"store_id":id}
    
    #attach a store to your user session
    select = requests.patch(storeselect_url, cookies=cookies, json=store_json)
    
    #pull the times for your current store
    response = requests.get(timeslots_url, cookies = cookies)
    data=json.loads(response.content)
    print (data["message"])

def main():
    
    #Check that enough arguments were provided
    if len(sys.argv) != 3:
        print "(+) usage: %s <state> <frequency in seconds>" % (sys.argv[0])
        print "(+) eg: %s VIRGINIA 60" % sys.argv[0]
        sys.exit(-1)

    #Set the repeat frequency
    frequency = sys.argv[2]  
    frequency = float(frequency)
    
    #Get access cookie
    print ("Finding Wegmans pickup timeslots in the state of %s every %.1f seconds." % (sys.argv[1], frequency))
    cookie = get_cookie()
    
    #Check times, repeating on intervals
    while True:
        get_stores(sys.argv[1], cookie)
        print("Pausing for %.1f seconds..." % frequency)
        time.sleep(frequency)
    
if __name__ == "__main__":
    main()
