import requests
import sys
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Get the anonymous session cookie with location data
def get_cookie():

    getcookie_url = "https://shop.wegmans.com/api/v2/user_sessions"
    getcookie_url2 = "https://shop.wegmans.com/api/v2/users"
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    cookie_json = {"binary":"web-ecom","binary_version":"2.25.122","is_retina":False,"os_version":"Win32","pixel_density":"2.0","push_token":"","screen_height":1080,"screen_width":1920}
    
    #send first request to get an Authorization Bearer header token
    response = requests.post(getcookie_url, json=cookie_json, proxies=proxies, verify=False)
    data=json.loads(response.content)
    #print ("Acquired cookie %s") % data["session_token"]
    
    #send the second request to get the api key
    response = requests.post(getcookie_url2, headers={"Authorization":"Bearer " + data["session_token"]}, proxies=proxies, verify=False)
    #print ("Acquired api key %s") % response.cookies['session-prd-weg']
    return(response.cookies['session-prd-weg'])
    
	
#Get store list based on provided state
def get_stores(province, cookie):
    getstores_url = "https://shop.wegmans.com/api/v2/stores?_nocache=1586788268363&show_ecommerce=true&show_pickup=true"
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    
    #pull the stores
    response = requests.get(getstores_url, proxies=proxies, verify=False)
    data=json.loads(response.content)
    
    #iterate through each store
    for item in data['items']:
        if item["address"]["province"] == province:
            if item["has_pickup"] == True:
                print("Address: %s") % item["address"]["address1"]
                get_timeslots(item["id"], cookie)



#Get timeslots the selected store
def get_timeslots(id, cookie):
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    timeslots_url = "https://shop.wegmans.com/api/v2/timeslots"
    cookies = {'session-prd-weg':"" + cookie}
    response = requests.get(timeslots_url, cookies = cookies, proxies=proxies, verify=False)
    data=json.loads(response.content)
    print (data["message"])

def main():
    
    if len(sys.argv) != 3:
        print "(+) usage: %s <state> <frequency in seconds>" % (sys.argv[0])
        print "(+) eg: %s VIRGINIA 60" % sys.argv[0]
        sys.exit(-1)

    print ("Finding Wegmans pickup timeslots in the state of %s" % sys.argv[1])
    frequency = sys.argv[1]  
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    cookie = get_cookie()
    get_stores(sys.argv[1], cookie)
    
if __name__ == "__main__":
    main()