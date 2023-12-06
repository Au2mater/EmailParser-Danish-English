
field_synonyms = {
    'sendt': 'Date sent'
     ,'cc':'CC'
     ,'fra':'Sender'
     ,'til': 'To'
     ,'emne':'Subject'
     ,'date sent': 'Date sent'
     ,'sender':'Sender'
     ,'to': 'To'
     ,'subject':'Subject'
     }

# Danish and english greetings
greetings = ['hello', 'hi', 'hey', 'dear'
             , 'hej', 'hall[oå]', 'god[]{0,1}morgen'
             , 'god[]{0,1}dag', 'hejsa', 'kære'
             , 'att\\.', 'til\\s']

# Danish and English signatures
da_sig = ['med[ ]venlig[ ]hilsen','venlig[ ]hilsen','hilsen','de[ ]bedste[ ]hils[e]{0,1}ner'
        ,'mange[ ]hilsner','vh','kh','mvh','dbh','tak','på[ ]forhånd[ ]tak']
en_sig = ['sent[ ]by','best[ ]regards','kind[ ]regards','sincerely','regards']


greeting_pattern = f"^({'|'.join(greetings)})"+".{0,60}$"
sig_pattern = f"^({'|'.join(da_sig+en_sig)})"+".{0,60}$"


test_message = '''
Date sent: Dec 15, 2023 09:45 AM
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