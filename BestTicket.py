import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from twilio.rest import Client

class BestTicket:
    def __init__(self):
        pass

    def stripper(self,str):
        str = str.replace('-','')#helper function to format the strings
        str = str.replace('.','')
        return str

    def getBest(self, day):
        with Display(visible=False, size=(1200, 1500)):
            dayBuffer = day
            if day >= 831:#this is a little hack for not wanting to do month-changing logic
                dayBuffer += 70

            options = Options()
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
            options.add_argument('user-agent={0}'.format(user_agent))
            options.add_argument('--disable-blink-features=AutomationControlled')#these options help us not get nuked by servers
            options.add_argument("--disable-extensions")
            options.add_experimental_option('useAutomationExtension', False) 
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            browser = webdriver.Chrome(options=options)#initiate driver with aforementioned options
            browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")#this also helps idk why

            URL = "https://wwws.airfrance.it/search/offers?pax=1:0:0:0:0:0:0:0&cabinClass=ECONOMY&activeConnection=0&connections=FLR:A:20220{}%3ESAO:C&bookingFlow=LEISURE&gclid=EAIaIQobChMI9uHo5cyr-AIVg7HtCh10KwGKEAAYASABEgK1KvD_BwE&gclsrc=aw.ds".format(str(dayBuffer))#queries the site for plane tickets on given days

            browser.get(URL)#stablishes a connection

            time.sleep(35)#sleepy time cuz the site slow

            cookie_btn= browser.find_element_by_css_selector("#bw-cookie-banner-container > div.bw-cookie-banner__main > div > div.bw-cookie-banner__button-wrapper.bw-cookie-banner__card > button.bw-cookie-banner__button.bw-cookie-banner__button-basic.bw-cookie-banner__first-button")
            cookie_btn.send_keys(Keys.ENTER)#goddamn cookie pop-ups

            smallestPrice = 1000 #placeholder

            try:
                for i in range(1,20):
                    bestOffer = browser.find_element_by_xpath('/html/body/bw-app/bwc-page-template/mat-sidenav-container/mat-sidenav-content/div/main/div/bw-search-result-container/div/div/section/bw-flight-lists/bw-flight-list-result-section/section/bw-itinerary-list/ol/li[{}]/bw-itinerary-row/div/div/div[2]/div/bw-itinerary-select/button/span[1]/span/span/span[2]/bw-price/span'.format(i))
                    label = str(bestOffer.text)                
                    priceIndex = label.index("EUR")    
                    price = int(self.stripper(label[:(priceIndex-1)]))
                    if (price < smallestPrice):
                        smallestPrice = price
            except:
                browser.close()
                if (smallestPrice > 500):
                    return (str(smallestPrice) + " Euros no dia: 20220{}".format(dayBuffer))
                else:
                    return (str(smallestPrice) + " Euros no dia: 20220{} link: \n {}".format(dayBuffer, URL))

bestPrices = []

client = Client("twilio_ssid","twilio_auth_token")

for i in range(0,22):
    bestPrices.append(BestTicket().getBest(815+i))
    print(bestPrices[i])

separator_ = "\n"
message = separator_.join(bestPrices)

client.messages.create(to="her_number", from_="my_twilio_number", body=message)





