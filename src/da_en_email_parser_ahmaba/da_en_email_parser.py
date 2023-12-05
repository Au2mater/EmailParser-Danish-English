import re
import email.utils as em_parser
import dateutil.parser as dt_parser1
from collections import OrderedDict
import dateparser as dt_parser2

test_message = (
'Date sent: Nov 30, 2023 11:37 PM\n'
'To: customerservice@buisness.com\n'
'Subject: Alert Center: Performance CPU Utilization Exceeds 90% '
'(7 out of threshold / 8 total) -  Escalation Step 1\n'
'Regards'
)

field_synonyms = (
    {'sendt': 'Date sent'
     ,'cc':'CC'
     ,'fra':'Sender'
     ,'til': 'To'
     ,'emne':'Subject'
     ,'date sent': 'Date sent'
     ,'sender':'Sender'
     ,'to': 'To'
     ,'subject':'Subject'
     })

def log_pipeline(f):
    """Decorator function to log the execution of the decorated function and any new fields added to the message."""    
    def wrapper(*args, **kw):
        in_msg = dict(args[0])
        verbose = in_msg['verbose']
        f(*args, **kw)
        out_msg = args[0]
        new_keys = [key for key in out_msg.keys() if key not in in_msg ]
        if verbose:
            print(f'Just ran {f.__name__}') 
            if len(new_keys)>  0:
                print('and added the following:')
                for key in new_keys:
                    print(f'{key} = {out_msg[key]}')
            else: print('no new fields added')
            print('------------')
        return out_msg
    return wrapper

def start_pipeline(message_string:str ,verbose =False):
    """Initialize the message dictionary for the email processing pipeline.

    Parameters:
    - message_string (str): The input email message string.
    - verbose (bool): Flag to indicate whether to print verbose logs.

    Returns:
    - message (OrderedDict): The initialized message dictionary.
    """
    message = OrderedDict()
    message['tail'] = message_string
    message['verbose'] = verbose
    if verbose: print(f"Initial message: \n {message_string[:100]}...\n------------")
    return message

def parse_date_string(date_str:str):
    """Parse a date string using two different date parsers.

    Parameters:
    - date_str (str): The input date string.

    Returns:
    - result: Parsed datetime object.
    """
    try: 
        result = dt_parser1.parse(date_str, fuzzy=True , dayfirst=True)
    except: 
        result = dt_parser2.parse(date_str ,languages=['da','en'] )
    return result

# parse_date_string('31. oktober 2024')


def parse_header_fields(message:dict):
    """Parse string in header fields to appropriate data types [email addresses, names, and dates].

    Parameters:
    - message (dict): The message dictionary.

    Returns:
    - message (dict): Updated message dictionary with parsed header fields.
    """

    if 'Date sent' in message.keys():
        datetime_string = message['Date sent']
        parsed_datetime = parse_date_string(datetime_string)
        
        message['Date sent'] = parsed_datetime
            
    for field in ['To','CC','Sender']:
        if field in message.keys():
            adresses = message[field]
            message[field] = adresses.split(',')
            recpients = []
            for recepient in message[field]:
                name, email_address = em_parser.parseaddr(recepient)
                recpients.append({'name':name,'address':email_address})
            message[field] = recpients

    return message


@log_pipeline
def extract_header(message:dict):
    """Extract header information from the email message.

    Parameters:
    - message (dict): The message dictionary.

    Returns:
    - message (dict): Updated message dictionary with extracted header information.
    """

    infotype_pattern = r'^[A-Z][a-z]{0,6}[ ]{0,1}[A-Za-z]{1,6}\:[ ]' 
    info_pattern = r'[^\n]+'
    
    message['header_text'] = ''
    content = message['tail']

    for line in content.splitlines():
        match = re.match(infotype_pattern + info_pattern, line, re.MULTILINE)
        if match:
            sep = line.find(':')
            field = line[:sep]
            if field.lower() in field_synonyms:
                field  = field_synonyms[field.lower()]
                message[field] = line[sep+2:]
                message['header_text'] += line + '\n' # add line to header text
                message['tail'] = message['tail'].split(line)[-1] # remove line from tail
            else: break
        else: break
    
    message = parse_header_fields(message)
    return message


# extract_header(start_pipeline(test_message))

@log_pipeline
def extract_greeting(message:dict):
    """Extract greeting information from the email message.

    Parameters:
    - message (dict): The message dictionary.

    Returns:
    - message (dict): Updated message dictionary with extracted greeting information.
    """
    # Define a regular expression pattern for common Danish greetings
    greeting_pattern = r'^(hej|hall[oå]|god[]{0,1}morgen|god[]{0,1}dag|hejsa|kære|att\.|til\s.{3,60}$)'
    content = message['tail']

    for line in content.splitlines()[:5]:
        # Search for the greeting pattern in the text
        match = re.search(greeting_pattern,line,re.IGNORECASE)
        # If a match is found, it's a greeting
        if match:
            message['greeting'] = line
            split = message['tail'].find(line) + len(line) # locate line in tail
            message['tail'] = message['tail'][split:] # remove line from tail
            break
    return message

@log_pipeline
def extract_signature(message:dict):
    """Extract signature information from the email message.

    Parameters:
    - message (dict): The message dictionary.

    Returns:
    - message (dict): Updated message dictionary with extracted signature information.
    """
    # Define a regular expression pattern for common Danish greetings
    da_sig = ['med[ ]venlig[ ]hilsen','venlig[ ]hilsen','hilsen','de[ ]bedste[ ]hils[e]{0,1}ner'
              ,'mange[ ]hilsner','vh','kh','mvh','dbh']
    en_sig = ['sent[ ]by','best[ ]regards','kind[ ]regards','sincerely','regards']
    sigs = '|'.join(da_sig+en_sig)
    sig_pattern = f'^({sigs})'
    
    content = message['body'] = message['tail']

    for line in content.splitlines():
        # Search for the greeting pattern in the text
        match = re.search(sig_pattern,line,flags=re.IGNORECASE)
        # If a match is found, it's a greeting
        if match:
            message['signature'] = line
            split = message['tail'].find(line) + len(line) # locate line in tail
            message['body'] = message['tail'][:split-len(line)] # remove signature from body
            message['tail'] = message['tail'][split:] # remove body and signature from tail
            break
    return message

@log_pipeline
def clean_body(message:dict):
    """Clean the body of the email message by removing emojis, symbols, and extra whitespaces.

    Parameters:
    - message (dict): The message dictionary.

    Returns:
    - message (dict): Updated message dictionary with cleaned body.
    """
    # Define a pattern to match emojis and symbols
    symbol_pattern = re.compile('[ \t]{2,}|※|_{3,}')

    # Remove emojis and symbols from the text
    message['body'] = symbol_pattern.sub(' ', message['body'])
    message['body'] = symbol_pattern.sub(' ', message['body'])
    message['body'] = str.strip(message['body'])
    
    return message

@log_pipeline
def extract_submessage(message:dict, m_type:str):
    """Extract nested mails that are forwarded or responded to.

    Parameters:
    - message (dict): The message dictionary.
    - m_type (str): Type of submessage ['forward'|'history'].

    Returns:
    - message (dict): Updated message dictionary with extracted submessage.
    """
    indicators = ['Sender:','Fra:']
    message_types = {'forward':'vs:','history':'sv:'}
    if 'Subject' in message.keys() and message_types[m_type] in message['Subject'].lower():
        for i in indicators:
            if i in (tail:=message['tail']):
                if message['verbose']: print(f'{m_type} submessage detected')
                substring = tail.find(i)
                message[m_type] = start_pipeline(tail[substring:])
                extract_header(message[m_type])
                if len(t:=message[m_type]['header_text']) > 5:
                    message['body'] = message['body'].split(t)[0] # remove signature from body
                    message['tail'] = message['tail'].split(t)[0]
                extract_greeting(message[m_type])
                extract_signature(message[m_type])
                break
    return message


