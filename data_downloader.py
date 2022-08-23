'''data_downloader.py
Laddar ner och sparar pentrydata.
'''
import os, logging, json, requests, datetime, pytz

#Logging
import data_utilities
import extractor

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG #Logga allt
)

#Filsökvägar
SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIRECTORY = os.path.dirname(SCRIPT_PATH)
PENTRY_DATA_FOLDER = os.path.join(SCRIPT_DIRECTORY, "data")

def run():
    '''Kör huvudkoden för att ladda ner och extrahera data.'''
    #Kontrollera efter mapp med pentrydata. Om den inte finns, skapa den.
    if not os.path.exists(PENTRY_DATA_FOLDER):
        logger.info("En mapp för pentrydata existerar inte. Skapar en...")
        os.mkdir(PENTRY_DATA_FOLDER)
        logger.info("Mapp för pentrydata skapad.")

    #Hämta data från skolans API så länge det inte är helg
    current_time = datetime.datetime.now(tz=pytz.timezone("Europe/Stockholm"))
    if not current_time.isoweekday() > 5:
        logger.info("Hämtar data från skolans API...")
        request = requests.get("https://api.ssis.nu/cal/?room=Hela%20skolan",
                               headers={
                                   "User-Agent": "Python/SSISPentryAnsvarParser (Contact: 20alse@stockholmscience.se)"
                               })
        schedule_data_json = request.json()
        parsed_pentrys_data = []
        for event in schedule_data_json: #Loopa igenom event
            logger.debug(f"Testar att behandla {event}...")
            event_subject = event["subject"]
            event_parsed = extractor.parse_pentryansvar_string(event_subject)
            """Om vi får tillbaka ett pentrynamn så vet vi att eventet åtminstone har med pentryt att göra.
            (det kan ju ha med annat att göra, t.ex. en föreläsning för hela skolan)
            """
            if event_parsed.pentry_name != None:
                logger.info("Hittat data som berört ett pentry! Lägger till i lista med data...")
                parsed_pentrys_data.append(event_parsed)
            else:
                logger.debug("Eventet verkar inte beröra ett pentry. Skippar...")
        #Spara ner data
        logger.info("Sparar ner data...")
        current_week_number = str(current_time.isocalendar()[1])
        data_utilities.save_pentry_data(current_week_number, parsed_pentrys_data)
        logger.info("Data nersparat.")
    else:
        logger.info("Kontroll för pentrydata ska inte köras då det är helg. Avslutar skript.")

    logger.info("Skriptet är klart.")

if __name__ == "__main__":
    run()
