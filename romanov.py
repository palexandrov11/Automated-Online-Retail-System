from selenium import webdriver
import requests
import re
import time
import os

class ScrapeRomanov():

    def __init__(self, i):
        self.i = i - 1
        self.driver = webdriver.Chrome()
        self.driver.get("http://romanovrussia.com/new-arrivals/")
        self.content = []
        self.tags = []
        self.title = None
        self.price = None
        self.images = None
        self.date = None
        self.material = None
        self.category = None
        self.section = None 
        self.start()

    def start(self):
        self.navigate()
        self.getContent()
        self.downloadImages()
        self.getDate()
        self.getTitle()
        self.generateContent()

    def navigate(self):
        items = self.driver.find_elements_by_class_name("link")
        item_list = list(filter(lambda y: y != '' and y != 'View Item', list(map(lambda x: x.text, items))))
        self.driver.find_element_by_link_text(item_list[self.i]).click()

    def getTitle(self):
        element_title = self.driver.find_element_by_css_selector("h1.entry-title.romanov-custom-template-header")
        self.title = element_title.text

    def getContent(self):
        element_content = self.driver.find_elements_by_xpath("//p")
        for x in element_content:
            if x.text[0] == '$':
                self.content.append(x.text)
                break
            elif x.text == 'Available':
                pass
            else:
                self.content.append(x.text)
        self.price = self.content.pop()
        self.price = self.price[1:]
        self.content = ' '.join(self.content)

    def getDate(self):
        try:
            self.date = re.search('\d{1,4}', self.content).group()
            if len(self.date) > 1:
                self.date = (int(self.date) // 10) * 10
            if self.date == 1900:
                self.date = "1900 - 1909"
            elif (self.date >= 1800) & (self.date < 1900):
                self.date = "1800s"
            elif (self.date >= 1700) & (self.date < 1800):
                self.date = "1700s"
            elif self.date < 1700:
                self.date = "Before 1700"
            else:
                self.date = str(self.date) + 's'
        except:
            self.date = '1950s'
            

    def downloadImages(self):
        image_counter = 0
        agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        image_elements = self.driver.find_elements_by_css_selector("img.scale-with-grid")
        sources = []
        for image in image_elements:
            sources.append(image.get_attribute("src"))
        print(sources)
        src_list = list(filter(lambda x : len(re.findall("http.*(350x350.jpg|.png)", x)) == 0, sources))
        print(src_list)
        for x in src_list:
            r = requests.get(x, stream=True, headers=agent)
            image_counter = image_counter + 1
            path = "/Users/PDA/Desktop/Etsy/Romanov%s.jpg" % (image_counter)
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        self.images = image_counter


    def generateContent(self):
    
        section_dict = {"ring" : "rings", "men" : "men's rings","earring" : "earrings", "brooch" : "brooches / pins",
                        "pins" : "brooches / pins", "necklace" : "necklaces / pendants", "pendant" : "necklaces / pendants",
                        "locket" : "lockets", "bracelet" : "bracelets", "cufflinks" : "cufflinks"}
        
        noun = set(re.findall('(ring|earring|bracelet|necklace|cufflinks|locket|pendant|chain|cross|brooch|pin|watch|wedding\sband)', self.content))
        noun.add('jewelry')
        metal = set(re.findall('(gold|silver|platinum)', self.content))
        stone = set(re.findall('(spinel|lapis|aquamarine|amethyst|turquoise|tourmaline|quartz|garnet|crystal|onyx|topaz|peridot|chrysolite|agate|alexandrite|chrysoberyl|jade|citrine|agate)', self.content))
        precious = set(re.findall('(diamond|sapphire|ruby|rubies|emerald|demantoid|pearl|enamel)', self.content))
        adjectives = set(re.findall('(Faberge|unisex|butterfly|bird|lion|snake|star|icon|flower|floral|heart|egg|bangle|link|chain|cuff|cluster|dangle|long|dangle|drop|stud|intaglio|armorial|signet|cluster)', self.content))
        period = set(re.findall('(georgian|victorian|edwardian|art\snouveau|art\sdeco)', self.content))
        generic = ['antique', 'vintage']
        wedding = set(re.findall('(Engagement|engagement)', self.title))
        gender = re.search('men', self.content)
        precious |= wedding
        if gender != None:
            precious.add("men's")
            self.section = section_dict['men']
            self.category = self.section
        counter = 0        
        for x in precious:
            for y in noun:
                if (len(x) + len(y) < 20) & (counter < 13):
                    self.tags.append(str(x) + ' ' + str(y))
                    counter += 1
        for x in stone:
            for y in noun:
                if (len(x) + len(y) < 20) & (counter < 13):
                    self.tags.append(str(x) + ' ' + str(y))
                    counter += 1
        for x in adjectives:
            for y in noun:
                if (len(x) + len(y) < 20) & (counter < 13):
                    self.tags.append(str(x) + ' ' + str(y))
                    counter += 1
        for x in metal:
            for y in noun:
                if (len(x) + len(y) < 20) & (counter < 13):
                    self.tags.append(str(x) + ' ' + str(y))
                    counter += 1
        for x in period:
            for y in noun:
                if (len(x) + len(y) < 20) & (counter < 13):
                    self.tags.append(str(x) + ' ' + str(y))
                    counter += 1
        for x in generic:
            for y in noun:
                if (len(x) + len(y) < 20) & (counter < 13):
                    self.tags.append(str(x) + ' ' + str(y))
                    counter += 1
                    
        self.material = list(metal | stone | precious)

        if self.section == None:
            for x in noun:
                if x in section_dict.keys():
                    self.section = section_dict[x]
                    self.category = self.section
                    break

    def clearImageFolder(self):
        while self.images > 0:
            os.remove("/Users/PDA/Desktop/Etsy/Romanov%s.jpg" % self.images)
            self.images -= 1








