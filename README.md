# EmailParser-Danish-English
EmailParser-Danish-English is small simple Python library to parse email text to structured python dictionaries.

Auto detect and extract the following:
 - Sender
 - Date
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

content = ('Date sent: Nov 30, 2023 11:37 PM\n'
 'To: customerservice@buisness.com\n'
 'Subject: Alert Center: Performance CPU Utilization Exceeds 90% (7 out of threshold / 8 total) -  Escalation Step 1\n'
 'Hi there,'
  'Check this out!'
 'Regards')

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
