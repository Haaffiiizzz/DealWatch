import schedule
import requests

def scraperTask():
    print("Sxcraper task")
    
schedule.every(1).minute.do(scraperTask)