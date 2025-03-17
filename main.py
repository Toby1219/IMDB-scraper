import playwright
from playwright.sync_api import sync_playwright, Page, Playwright
from dataclasses import dataclass, asdict
from fake_useragent import UserAgent
import pandas as pd


@dataclass
class Movies:
    Movie_Id: int
    Movie_Name: str
    Movie_type: str
    Release_Date: str    
    Rateing: str
    Reviews: str
    Movie_Runtime: str
    Movie_Genre: list[str]
    Movie_Plot: str
    Metacritic: int
    Movie_Image: str
    Movie_url: str

class BotOne:
    def __init__(self, movie_date:tuple[str], movie_type:list[str], genre:list[str]):
        self.movie_date = movie_date
        self.movie_type, self.genre = self.formart_pram(movie_type, genre)
        self.url = self.parseUrl()
        self.extracted_data = []
        self.total_listing = 4000
        self.page = Page
        self.cur_total_listing:int
        
    def formart_pram(self, m_t, m_g):
       newList_type = ['feature' if x == "movie" else x.replace(" ", "_") for x in m_t]
       newList_genre = [x.replace(" ", "-") for x in m_g]
       return newList_type, newList_genre
       
    def parseUrl(self):
        url = f"""https://www.imdb.com/search/title/?title_type={",".join(self.movie_type)}&release_date={",".join(self.movie_date)}&genres={",".join(self.genre)}"""
        print(url)
        return url
     
    def start_browser(self, playwirght:Playwright):
        browser = playwirght.firefox.launch(headless=False)
        context = browser.new_context(
            user_agent = UserAgent().random,
            viewport = {'width': 650, 'height': 540}
            )
        self.page:Page = context.new_page()
        self.page.goto(self.url, timeout=800000)
    
    def current_total_item(self):
        listing_Movie = self.page.locator("li.ipc-metadata-list-summary-item > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > h3:nth-child(1)").all()
        index = len(listing_Movie)
        total = listing_Movie[index-1].inner_text()
        return int(total.split(" ")[0].replace(".", "").strip())
        
    def scroll(self):
        while self.cur_total_listing <= self.total_listing: 
            btn = self.page.locator("span.single-page-see-more-button")
            self.page.wait_for_timeout(5000)
            try:
                btn.click()
                self.cur_total_listing = self.current_total_item() 
                print("Total: ", self.cur_total_listing)  
            except playwright._impl._errors.TimeoutError:
                print("End of page")
                break
    
    def extractor(self, item:Page, selector, attrib=False, attrib_value=None):
        if attrib == True:
            try:
                return item.locator(selector).get_attribute(attrib_value, timeout=2000)
            except playwright._impl._errors.TimeoutError:
                return "No Data"
        else:        
            try:
                return item.locator(selector).inner_text(timeout=2000)
            except playwright._impl._errors.TimeoutError:
                return "No Data"
            
    def Parse_html(self):
        boxs = self.page.locator("li.ipc-metadata-list-summary-item > div > div > div.dli-parent").all()
        print("Total Movies: ", len(boxs))
        for x, item in enumerate(boxs, start=1):
            name_tag = item.locator("div > div:nth-child(2) > div > a > h3").inner_text()
            name = "".join(name_tag.split(".")[1:]).strip()
            
            movie_year= self.extractor(item, "div > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)")
            
            runtime = self.extractor(item, "div > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)")
            
            movie_type = self.extractor(item, "div > div:nth-child(2) > div:nth-child(2) > span:nth-child(3)")
            
            stars = self.extractor(item, "div > div:nth-child(2) > span > div > span.ratingGroup--imdb-rating > span.ipc-rating-star--rating")
            
            total_votes = self.extractor(item, "div > div:nth-child(2) > span > div > span.ratingGroup--imdb-rating > span.ipc-rating-star--voteCount")
            total_vote = total_votes.replace("(", "").replace(")", "").strip()
            
            meta_score = self.extractor(item, "div > div:nth-child(2) > span > span > span.metacritic-score-box")
            
            plot = self.extractor(item, "div:nth-child(2) > div.sttd-plot-container > div")
            
            movie_url = f"https://www.imdb.com{self.extractor(item, "div:nth-child(1) > div.dli-poster-container > div > a", True, 'href')}"
            
            image_url = self.extractor(item, "div:nth-child(1) > div.dli-poster-container > div > div:nth-child(2) > img", True, 'src')
            movie = Movies(
                    Movie_Id = x,
                    Movie_Name = name,
                    Movie_type = movie_type,
                    Release_Date = movie_year,
                    Rateing = stars,
                    Reviews = total_vote,
                    Movie_Runtime = runtime,
                    Movie_Genre = self.genre,
                    Movie_Plot = plot,
                    Metacritic =  f"{meta_score} Metascore",
                    Movie_Image = image_url,
                    Movie_url = movie_url
                )
            result = asdict(movie)
            print(result)
            self.extracted_data.append(result)
            
    def writer(self):
        df = pd.DataFrame(self.extracted_data)
        df.to_csv("Imdb_data.csv", index=False)
        df.to_excel("Imdb_data.xlsx", index=False)
        df.to_json("Imdb_data.json", indent=4, orient='records')   
    
    def main(self):
        with sync_playwright() as playwright:
            self.start_browser(playwright)
            self.cur_total_listing = self.current_total_item()
            self.scroll()
            self.Parse_html()
            self.writer()        
            self.page.close()
        
            

if __name__ == "__main__":
    bot = BotOne(('2024-01-01', "2024-12-31"), ["movie"], ["action", "comedy"])
    bot.main()


