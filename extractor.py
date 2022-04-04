'''extractor.py
Extracts/parses pentryansvar data form a string.
'''
import re, logging
from json import JSONEncoder

TEST_STRINGS = [
    "Pentry 1: Henning, Alvin, Simon P, Sofie & Hugo Te19B",
    "Pentry 2: Anton, Lukas, Leia, Shayan, Jennifer & Erik  Te19A"
]
TEST_STRING = ""
#Regex för att extrahera grunddata (pentrynamn, pentrynummer, och ansvarig klass + annat grupperat efter som vi matchar sen
PENTRY_RESPONSIBLE_CLASS_REGEX = "(\(?((te {0,}[0-9]{2,}[a-z])|personal)\)?)" #Matchar en ansvarig klass eller en ansvarig grupp
PENTRY_NUMBER_REGEX = "(pentry ([1-2])):" #Matchar pentrynummer
PENTRY_RESPONSIBLE_PERSON_REGEX = "([^ ,&][a-zA-Z]([a-zA-Z]|( |-))+[^ ,&])" #Matchar personer som är ansvariga för pentryt
logger = logging.getLogger(__name__)
class Pentryansvar:
    def __init__(self, pentry_name, pentry_number, responsible_class, responsible_persons):
        '''Initierar en ny klass som innehåller data om pentryansvar.'''
        self.pentry_name = pentry_name
        self.pentry_number = pentry_number
        self.responsible_class = responsible_class
        self.responsible_persons = responsible_persons

    def __str__(self):
        return str(self.__dict__)
class PentryansvarJSONSerializer(JSONEncoder):
    '''Serializes pentryansvar data into JSON.'''
    def default(self, o):
        return o.__dict__

def parse_pentryansvar_string(string):
    #Matcha grunddata
    logger.info(f"Konverterar sträng {string} till pentrydata...")
    string = string.strip() #Strippa texten från whitespace etc
    logger.debug("Matchar och grupperar matchningar...")
    pentry_information = re.search(PENTRY_NUMBER_REGEX, string, re.IGNORECASE)
    if pentry_information != None:
        pentry_name = pentry_information.group(1)
        pentry_number = pentry_information.group(2)
        string = string.replace(pentry_name, "")
    else:
        logger.warning("Pentry kunde inte hittas!")
        pentry_name = pentry_number = None
    responsible_class_find = re.search(PENTRY_RESPONSIBLE_CLASS_REGEX, string, re.IGNORECASE)
    if responsible_class_find != None:
        responsible_class = responsible_class_find.group(2).replace(" ", "") #Get the responsible class name
        string = string.replace(responsible_class_find.group(0), "") #Remove the found class name from the string
    else:
        logger.warning("Ansvarig klass kunde inte hittas!")
        responsible_class = None
    print(string)
    responsible_persons = re.findall(PENTRY_RESPONSIBLE_PERSON_REGEX, string, re.IGNORECASE)
    if responsible_persons == []:
        logger.warning("Ansvariga personer kunde inte hittas!")
    else:
        #Iterera genom ansvariga personer för att hämta första gruppen, som innehåller hela deras namn
        responsible_persons = [
            partial_match[0] #Välj första gruppen
            for partial_match in responsible_persons
        ]
    logger.info("Konverterar till matchningsobjekt...")
    pentry_data = Pentryansvar(
        pentry_name,
        pentry_number,
        responsible_class,
        responsible_persons
    )
    logger.debug(f"Pentrydata: {pentry_data}")
    return pentry_data
