import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

class uploadEtsy():
    def __init__(self, x):
        self.x = x
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.etsy.com/")
        self.upload()

    def upload(self):
        self.logIn()
        self.uploadImages()
        self.enterTitle()
        self.enterDate()
        self.enterCategory()
        self.enterDescription()
        self.selectSection()
        self.enterTags()
        self.enterMaterials()
        self.enterPrice()
        self.publish()
        self.x.clearImageFolder()
        self.x.driver.quit()
        self.driver.quit()
        

    def logIn(self):
        try:
            accept_cookie = self.driver.find_element_by_css_selector("button.width-full.btn.btn-outline.btn-outline-black").click()
        except:
            pass
        self.driver.implicitly_wait(10)
        sign_in = self.driver.find_element_by_css_selector("a#sign-in.inline-overlay-trigger.signin-header-action.select-signin").click()
        username = self.driver.find_element_by_css_selector("input#join_neu_email_field.input.input-large")
        username.send_keys("email")
        password = self.driver.find_element_by_css_selector("input#join_neu_password_field.input.input-large")
        password.send_keys("password")
        password.send_keys(u'\ue007')
        shop = self.driver.find_element_by_css_selector("span#gnav-account-shop-seller-description.text-link-copy").click()
        try:
            expand_menu = self.driver.find_element_by_css_selector("button.collapse-button.unstyled-button.bl-xs-1.bt-xs-1.pl-xs-2.pr-xs-2.text-center.hide-md.hide-sm.hide-xs.pt-xs-2.pb-xs-2").click()
        except:
            pass
        listings = self.driver.find_element_by_xpath("//span[contains(text(), 'Listings')]").click()
        add_listing = self.driver.find_element_by_xpath("//span[contains(text(), 'Add a listing')]").click()

    def uploadImages(self):
        i = 1
        while i < self.x.images + 1:
            upload_image = self.driver.find_element_by_id("listing-edit-image-upload")
            upload_image.send_keys("/Users/PDA/Desktop/Etsy/Romanov%s.jpg" % (i))
            i = i + 1
        time.sleep(7)

    def enterTitle(self):
        title = self.driver.find_element_by_css_selector("input#title.input.character-counter-input")
        title.send_keys(self.x.title)

    def enterDate(self):
        select_who = Select(self.driver.find_element_by_id("who_made"))
        select_who.select_by_visible_text("Another company or person")
        select_type = Select(self.driver.find_element_by_id("is_supply"))
        select_type.select_by_visible_text("A finished product")
        select_age = Select(self.driver.find_element_by_id("when_made"))
        select_age.select_by_visible_text(self.x.date)

    def enterCategory(self):
        category = self.driver.find_element_by_id("taxonomy-search")
        category.send_keys(self.x.category)
        time.sleep(3)
        category.send_keys(u'\ue007')

    def enterDescription(self):
        renewal = self.driver.find_element_by_xpath("//span[contains(text(), 'Automatic')]")
        self.driver.execute_script("arguments[0].click();", renewal)
        description = self.driver.find_element_by_id("description")
        description.send_keys(self.x.content)

    def selectSection(self):
        select_section = Select(self.driver.find_element_by_id("sections"))
        select_section.select_by_visible_text(self.x.section)

    def enterTags(self):
        tags = self.driver.find_element_by_css_selector("input#tags.input")
        for i in self.x.tags:
            tags.send_keys(i)
            tags.send_keys(u'\ue007')

    def enterMaterials(self):
        materials = self.driver.find_element_by_css_selector("input#materials.input")
        for i in self.x.material:
            materials.send_keys(i)
            materials.send_keys(u'\ue007')

    def enterPrice(self):
        price = self.driver.find_element_by_id("price_retail-input")
        price.send_keys(self.x.price)

    def publish(self):
        shipping = self.driver.find_element_by_xpath("//span[contains(text(), 'Enter custom shipping options')]")
        self.driver.execute_script("arguments[0].click();", shipping)
        select_shipping = Select(self.driver.find_element_by_id("shipping-costs-selector"))
        select_shipping.select_by_visible_text("I'll enter fixed costs manually")
        process_time = Select(self.driver.find_element_by_id("processing-time-selector"))
        process_time.select_by_visible_text("1 business day")
        publish = self.driver.find_element_by_xpath("//button[contains(text(), 'Publish')]").click()
        time.sleep(2)
        confirm = self.driver.find_element_by_xpath("//button[@data-ui='confirm']").click()
        time.sleep(15)
       
        
        
            
