'''data_utilities.py
Innehåller funktioner relaterat till att hämta sparad pentrydata.
(data cachas och sparas till filer
'''
import os, logging, json
from extractor import PentryansvarJSONSerializer
logger = logging.getLogger(__name__)

#Filsökvägar
SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIRECTORY = os.path.dirname(SCRIPT_PATH)
PENTRY_DATA_FOLDER = os.path.join(SCRIPT_DIRECTORY, "data")

def read_data_from_json_file(file_path):
    '''Funktion för att läsa data från en JSON-fil.

    :param file_path: Sökvägen att läsa filer ifrån.'''
    logger.debug(f"Läser json från {file_path}...")
    return json.loads(open(file_path, "r").read())

def write_data_to_json_file(file_path, content, json_serializer=None):
    '''Funktion för att skriva data till en JSON-fil.

    :param file_path: Sökvägen att skriva till.

    :param content: Innehållet att skriva till filen.

    :param json_serializer: Om inte None, definierar en serializer att använda när data ska skrivas till filen.'''
    logger.debug(f"Skriver json till {file_path}...")
    with open(file_path, "w") as json_file:
        json_file.write(json.dumps(content, cls=json_serializer, indent=4))
    logger.debug("JSON skriven till fil.")

def get_paths_for_pentry_data(week):
    '''Hämtar filsökvägar där pentrydata sparas.

    :param week: Veckonumret för data.'''
    week_data_folder = os.path.join(PENTRY_DATA_FOLDER, week)
    week_data_file = os.path.join(week_data_folder, "data.json")
    return week_data_folder, week_data_file

def save_pentry_data(week, content):
    '''Funktion för att spara pentrydata för en viss vecka.'''
    logger.info(f"Sparar pentrydata för vecka {week}...")
    week_data_folder, week_data_file = get_paths_for_pentry_data(week)
    if not os.path.exists(week_data_folder):
        logger.debug("Mapp för veckodata finns inte. Skapar...")
        os.mkdir(week_data_folder)
    else:
        logger.debug("Mapp för veckodata finns.")
    write_data_to_json_file(week_data_file, content, PentryansvarJSONSerializer) #Skriv data med serializer
    logger.info(f"Pentrydata för vecka {week} sparad.")

def get_pentry_data(week):
    '''Hämtar pentrydata för vecka.

    :returns En dictionary med data om data finns, annars None.'''
    logger.info(f"Försöker hämta pentrydata för vecka {week}...")
    week_data_folder, week_data_file = get_paths_for_pentry_data(week) #Hämta filsökvägar
    if not all([os.path.exists(path) for path in [week_data_folder, week_data_file]]): #...och kontrollera att de existerar (annars finns ingen data tillgänglig).
        logger.info("Ingen data för den efterfrågade veckan finns tillgänglig! Returnerar None...")
        return None
    else:
        logger.info("Data för den efetrfrågade veckan fills tillgänglig. Returnerar...")
        return read_data_from_json_file(week_data_file) #Läs data
