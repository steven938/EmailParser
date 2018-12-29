# EmailParser - An easy way to parse raw email texts

With Email Parser you can easily parse emails in their raw string format such as the following Outlook email. EmailParser uses primiarly several hard coded regex expressions as well as a classification machine learning model to detect parts of the emails. 
```
Hey John, 
I appreciate your feedback.
Steven

From: John, Doe <johndoe@hotmail.com>
Sent: December 13, 2018 2:47 PM
To: S Chen
Subject: Re: Steven Chen - Jobs 
 
Hi Steven, I looked at your github repo and i think you need a better README file.
Best,
John
 
From: S Chen <s_chen@hotmail.ca>
Date: Thursday, December 13, 2018 at 2:41 PM
To: "John Doe" <johndoe@hotmail.com>
Subject: Check out my repo
 
Hi John,
Check out my new repo
Thank you!
Steven Chen
```


# Overview
EmailParser was written to help with tasks including: separating the above example into two separate strings by header or removing the signature of the email. 

## Usage

In the following paragraphs, I am going to describe how you can get and use Scrapeasy for your own projects.

###  Getting it

To download scrapeasy, either fork this github repo or simply use Pypi via pip.
```sh
$ pip install EmailParser
```

### Using it

Scrapeasy was programmed with ease-of-use in mind. 

```Python
from EmailParser import EmailParser
parser = EmailParser()
```

## Methods
Below describe just some of the methods included. Check in-code comments and EmailParser.py for other miscellaneous methods you may find useful.
##### get_most_recent 
Returns string portion of most recent message in an email by removing everything below the first reply/forward email header it finds
```
parser.get_most_recent(email_text)
>>>Hey John, 
>>>I appreciate your feedback.
>>>Steven
```
##### get_all_separated 
returns a list/array of emails separated by reply and forward headers the email headers are NOT removed in the process - they will appear at the top of the emails

##### remove_header
Removes the header at the top of the email. Assumes there is only ONE HEADER in the email passed into function. After get_all_seperated returns list of emails, all replies/forwarded emails will have a header that can be removed by this function
```
parser.remove_header(email_text)
```

##### remove_signature
remove_signature returns the substring an email representing the email without signature. 
    The function does this by looking for regex patterns signifying the signature (eg. "sincerely,").
    If a regex pattern is not found, the function uses the Mailgun Talon machine learning model to identify
    Substrings with high probability of being a signature
    Parameter remove_phrase: if ```True```, the "thank you" "sincerely" etc. are included in the signature to be removed
    Parameter sender: email address or name of person sending email
```
parser.remove_signature(email_text, remove_phrase=True, sender="John Doe")
```

##### get_salutation
get_salutation finds common email salutations such as "hi", "dear", "hey [name]" and returns this phrase
```
parser.get_salutation(email_text)
```
##### get_header
This function searches a string to find the value associated with the email header.
    For example, in a forwarded email, if you want to find who it was sent from, then 
    Call the function get_header(email_text, "from")
    Parameter header: "from", "to", "sent", or "subject", etc. 
```
parser.get_header(email_text, header)
```
##### get_forwarded_sender
This method takes in a string of an email with an email header or an email header itself and returns a tuple of the (name, email) of the sender identified from the email header
    
How it works:
The name/email will typically be found in the "From:..." or "On... wrote:" line of an email header
Once this line is found, the method will look for an email eg. "....@....com"
Then it finds the name by removing anything in brackets <> [] from the line
```
parser.get_forwarded_sender(email_text)
```
##### get_sent_date
This method looks in an email (with its string email header) to find the time that the email sent
@:return datetime object representing the time sent found in an email header
```
parser.get_sent_date(email_text)
```

##### get_body
 get_body method just combines the remove_signature, get_salutation, and get_most_recent to isolate for the body of an email
```
parser.get_body(email_text, checksignature=True, check_salutation=False, check_reply_text=False, sender="", removephrase=False)
```