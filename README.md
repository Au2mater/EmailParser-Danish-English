# EmailParser-Danish-English
EmailParser-Danish-English is small simple Python library to parse email text to structured python dictionaries.
Suitable for pre-processing for NLP tasks.

Auto detect and extract the following:
 - Sender
 - Date (Automatically parsed into a python date type)
 - Recepients
 - Greeting
 - Email body
 - Signature
 - Nested Forwarded mail
 - Nested reply history

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install git+https://github.com/Au2mater/EmailParser-Danish-English.git
```

## Usage

```python
import da_en_email_parser_ahmaba as ep

content = '''Date sent: Dec 15, 2023 09:45 AM
To: support@company.com
CC: management@company.com
Subject: VS: Weekly Project Update and Forwarded Message
Hello Team,

I hope this email finds you well. Here is the update on our ongoing projects:
- Project A: Milestone achieved, and client feedback incorporated.
- Project B: On track, no issues reported.

In addition to the project updates, I wanted to share a forwarded message from our client:
------------------------------

Please review the forwarded message and let me know if there are any further actions required.

Best regards,
Your Name
----- Forwarded Message -----
From: client@example.com
Date: Dec 14, 2023 03:20 PM
Subject: Re: Project Feedback
Hi Team,
I appreciate the quick response and the changes made. Everything looks good now. Thanks!

Best Regards,
John Doe
'''


# full parsing pipeline
def parse_message(content , verbose=False):

    message = ep.start_pipeline(content, verbose=verbose)
    ep.extract_header(message)
    ep.extract_greeting(message)
    ep.extract_signature(message)
    ep.clean_body(message)
    ep.extract_submessage(message,'forward')
    ep.extract_submessage(message,'history')
    del message['verbose']
    
    return message

message = parse_message(content)
# returns an ordered dict with the following keys:
# odict_keys(['tail', 'header_text', 'Date sent', 'To', 'CC', 'Subject', 'greeting', 'body', 'signature', 'forward'])

print(message['Date sent']) # the date as a date type
# 2023-12-15 09:45:00

print(message['body']) # the body without the greeting and the signature
# I hope this email finds you well. Here is the update on our ongoing projects:
# - Project A: Milestone achieved, and client feedback incorporated.
# - Project B: On track, no issues reported.
# In addition to the project updates, I wanted to share a forwarded message from our client:
# ------------------------------
# Please review the forwarded message and let me know if there are any further actions required.


```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
