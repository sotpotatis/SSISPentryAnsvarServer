from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from data_utilities import get_pentry_data
import logging, datetime, pytz

logger = logging.getLogger(__name__)

app = FastAPI()  # Skapa en app
#Initiera CORS-policys
logger.debug("Initierar CORS...")
CORS_ALL_WILDCARD = ["*"] #Wildcard för allt på CORS
CORS_ALLOWED_ORIGINS = CORS_ALL_WILDCARD
CORS_ALLOWED_HEADERS = CORS_ALL_WILDCARD,
CORS_ALLOWED_METHODS = CORS_ALL_WILDCARD
app.add_middleware( #Lägg till CORS-hanterare
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_headers=CORS_ALL_WILDCARD,
    allow_methods=CORS_ALLOWED_METHODS
)
logger.debug("CORS initierat.")
API_EXAMPLE_RESPONSE = [
    {
        "pentry_name": "Pentry 2",
        "pentry_number": "2",
        "responsible_class": "Te20A",
        "responsible_persons": ["Person 1", "Person 2", "Person 3", "Person 4", "Person 5"]
    },
    {
        "pentry_name": "Pentry 1",
        "pentry_number": "1",
        "responsible_class": "Te20B",
        "responsible_persons": ["Person 6", "Person 7", "Person 8", "Person 9", "Person 10"]
    }
]  # TODO: Använd exempelsvaret till automatisk dokumentation etc. (på wishlisten)


@app.get("/api/pentryansvar/")
async def get_pentryansvar_for_week(week_number: int = None):
    logger.info("Tog emot en förfrågan att hämta pentryansvar...")
    # Hämta ansvar
    if week_number == None:
        logger.info("Veckonummer är inte specificerat. Ställer in...")
        week_number = str(datetime.datetime.now(tz=pytz.timezone("Europe/Stockholm")).isocalendar()[
                              1])  # Hämta aktuellt veckonummer om det inte är ifyllt
    else:
        logger.info("Veckonummer är specificerat.")
        week_number = str(week_number)  # Konvertera till string
    logger.info("Returnerar svar...")
    pentryansvar_data = get_pentry_data(week_number)
    # Returnera data om den finns, annars, returnera ett fel
    if pentryansvar_data == None:
        raise HTTPException(status_code=404, detail="Det finns ingen data cachad för den veckan.")
    else:
        return pentryansvar_data
