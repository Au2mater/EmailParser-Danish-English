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

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install git+https://github.com/Au2mater/EmailParser-Danish-English.git
```

## Usage

```python
import da_en_email_parser_ahmaba as ep

content = ('Date sent: Dec 15, 2023 09:45 AM\n'
           'To: support@company.com\n'
           'CC: management@company.com\n'
           'Subject: VS: Weekly Project Update and Forwarded Message\n'
           'Hello Team,\n\n'
           'I hope this email finds you well. Here is the update on our ongoing projects:\n'
           '- Project A: Milestone achieved, and client feedback incorporated.\n'
           '- Project B: On track, no issues reported.\n\n'
           'In addition to the project updates, I wanted to share a forwarded message from our client:\n'
           '------------------------------\n\n'
           'Please review the forwarded message and let me know if there are any further actions required.\n\n'
           'Best regards,\n'
           'Your Name'
           '----- Forwarded Message -----\n'
           'From: client@example.com\n'
           'Date: Dec 14, 2023 03:20 PM\n'
           'Subject: Re: Project Feedback\n'
           'Hi Team,\n'
           'I appreciate the quick response and the changes made. Everything looks good now. Thanks!\n\n'
           'Best Regards,\n'
           'John Doe\n')

# full parsing pipeline
def parse_message(content , verbose=False):
    message = ep.start_pipeline(content, verbose=verbose)
    ep.extract_header(message)
    ep.extract_greeting(message)
    ep.extract_signature(message)
    ep.clean_body(message)
    ep.extract_submessage(message,'forward')
    ep.extract_submessage(message,'history')
    
    return message

parse_message(content)

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
