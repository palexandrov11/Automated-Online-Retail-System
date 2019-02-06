from romanov import ScrapeRomanov
from etsy import uploadEtsy

if __name__ == '__main__':
    prod_id = input("Enter product id")
    scrapeUpload = uploadEtsy(ScrapeRomanov(int(prod_id)))
    
    
