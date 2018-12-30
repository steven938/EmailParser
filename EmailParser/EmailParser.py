"""
This file contains EmailParser class which contains methods for parsing an email.
Instance methods rely on the initialization of this EmailParser class which initializes the 'talon' machine learning
model for parsing complex email signatures.

Static Methods: ....
Instance Methods: ....
"""

import re
import talon
from EmailParser import datefinder

class EmailParser:
    #  emailHeaders stores regex patterns identifying the beginning of a email header:
    # eg. "From: recon@ia.ca Sent: saladmin@ia.ca"
    emailHeaders = r"(-| )*Original Message(-| )*(\n|\r\n|\n\s)*[ \t]*From:.*(\n|\r\n|\n\s)|(-| )*Original Message(-| )*|" + \
                   r"From:.*(\n|\r\n|\n\s)*[ \t]*Sent:.*(\n|\r\n|\n\s)|" + \
                   r"On\s(.+?)wrote:|" + \
                   r"From:.*(\n|\r\n|\n\s)*[ \t]*Date:.*(\n|\r\n|\n\s)|" + \
                   r"From:.*(\n|\r\n|\n\s)*[ \t]*To:.*(\n|\r\n|\n\s)|" + \
                   r"Subject:.*(\n|\r\n|\n\s)*[ \t]*Date:.*(\n|\r\n|\n\s)*[ \t]*From:.*(\n|\r\n|\n\s)*[ \t]*To:.*(\n|\r\n|\n\s)|" + \
                   r"(-| )*Forwarded message.*(-| )*(\n|\r\n|\n\s)*[ \t]*Date:.*(\n|\r\n|\n\s)|" + \
                   r"Expéditeur:.*(\n|\r\n|\n\s)*[ \t]*Date:.*(\n|\r\n|\n\s)"  # French headers

    def __init__(self):
        talon.init()  # initiates the talon machine learning model for parsing signatures

    """
    get_most_recent returns most recent message in an email by removing everything below the first reply/forward email header it finds
    """
    @staticmethod
    def get_most_recent(email_text):
        match = re.search(EmailParser.emailHeaders, email_text, re.IGNORECASE)
        if match is not None:
            span = match.span()
            email_text = email_text[0:span[0]]
        return email_text

    """
    get_all_separated returns a list/array of emails separated by reply and forward headers
    the email headers are NOT removed in the process - they will appear at the top of the emails
    """
    @staticmethod
    def get_all_separated(email_text):
        matches = re.finditer(EmailParser.emailHeaders, email_text, re.IGNORECASE + re.MULTILINE)
        results = []
        startingBoundary = 0
        if matches is not None:
            for match in matches:
                endingBoundary = match.span()[0]
                message = email_text[startingBoundary:endingBoundary]
                results.append(message)
                startingBoundary = endingBoundary
            lastMessage = email_text[startingBoundary:len(email_text)]
            results.append(lastMessage)
            return results

    """
    Removes the header at the top of the email
    Assumes there is only ONE HEADER in the email passed into function
    After get_all_seperated returns list of emails, all replies/forwarded emails will have a header that 
    can be removed by this function
    """
    @staticmethod
    def remove_headers(email_text):
        headerLines = "From:.*|" + "Date:.*|" + "To:.*|" + "Cc:.*|" + "Subject:.*|" + "Importance:.*|" + "Sent:.*|" + "Reply-To:.*|" + \
                      "-(-| )*Forwarded message.*-(-| )*|" + "-(-| )*Original Message-(-| )*|" + "On\s(.+?)wrote:|" + \
                      "Expéditeur:.*|Destinaire:.*|Objet:.*|" + \
                      "-(-| )*Original Appointment-(-| )*|" + "(-| )*Begin forwarded message:(-| )*|" + "(-| )*End forwarded message(-| )*"
        matches = re.finditer(headerLines, email_text, re.IGNORECASE + re.MULTILINE)
        for match in matches:
            email_text = email_text.replace(match.group(0), " ")
        return email_text

    """
    remove_signature returns the substring an email representing the email without signature. 
    The function does this by looking for regex patterns signifying the signature (eg. "sincerely,").
    If a regex pattern is not found, the function uses the Mailgun Talon machine learning model to identify
    Substrings with high probability of being a signature
    @:param remove_phrase: if True, the "thank you" "sincerely" etc. are included in the signature to be removed
    @:param sender: email address or name of person sending email
    """
    def remove_signature(self, email_text, remove_phrase=True, sender=""):
        signatureFound = False
        # below separates salutation part of the email from the body
        salutation = EmailParser.get_salutation(email_text)
        if salutation is not None:
            email_without_sig = email_text[len(salutation):]
        else:
            salutation = ""
            email_without_sig = email_text
        # common phrases denoting the beginning of the email signature
        sig_opening_statements = [
            "[a-z]*\s+regards,",
            "cheers",
            "many thanks",
            "thanks",
            "sincerely",
            "ciao",
            "Best",
            "bGIF",
            "thank you",
            "thankyou",
            "talk soon",
            "cordially",
            "yours truly",
            "thanking You",
            "best wishes"
        ]
        pattern = "[\n]+\s*(" + "|".join(sig_opening_statements) + ").*"
        matches = re.finditer(pattern, email_without_sig, re.IGNORECASE)

        signature_regex = None
        for match in matches:
            signature_regex = match  # the last regex match is counted as the signature
        if signature_regex is not None:
            signatureFound = True
            if remove_phrase:
                email_without_sig = email_without_sig[:signature_regex.span()[0]]
            else:
                email_without_sig = email_without_sig[:signature_regex.span()[1] + 1]

        # check to see if the entire body of the message has been 'stolen' by the signature. If so, return no sig so body can have it.
        if len(email_without_sig) == 0:
            email_without_sig = email_text
            signatureFound = False
        else:
            email_without_sig = salutation + email_without_sig
        # if signature be found using, use talon machine learning algorithm to search for signature
        if not signatureFound:
            cut = ""
            index = 0
            while len(cut) != len(email_text):
                curr = email_text[index]
                if curr == "\n":
                    body, sig = talon.signature.extract(cut, sender)
                    if sig is not None:
                        email_without_sig = body
                        break
                cut = cut + curr
                index += 1
        return email_without_sig

    """
    get_salutation finds common email salutations such as "hi", "dear", "hey [name]" and returns this phrase
    """
    @staticmethod
    def get_salutation(email_text):
        # Notes on regex:
        # Max of 5 words succeeding first Hi/To etc, otherwise is probably an entire sentence
        salutation_opening_statements = [
            "hi",
            "dear",
            "to",
            "hey",
            "hello",
            "good morning",
            "good afternoon",
            "good evening"]
        pattern = "\s*(?P<salutation>(" + "|".join(
            salutation_opening_statements) + ")+(\s*\w*)(\s*\w*)(\s*\w*)(\s*\w*)(\s*\w*)[\.,\xe2:]+\s*)"
        groups = re.match(pattern, email_text, re.IGNORECASE)
        salutation = None
        if groups is not None:
            if "salutation" in groups.groupdict():
                start = groups.span()[0]
                end = groups.span()[1]
                salutation = email_text[start:end]
        return salutation

    """
    get_body method just combines the remove_signature, get_salutation, and get_most_recent to get the body of an email
    this method is not static and requires EmailParser to be initialized
    @:param str sender: the sender email or name used by Talon machine learning library to find the signature
    """
    def get_body(self, email_text, check_signature=True, check_salutation=False, check_reply_text=False, sender="",
                 remove_phrase=False):
        if check_reply_text:
            email_text = EmailParser.get_most_recent(email_text)
        if check_salutation:
            sal = EmailParser.get_salutation(email_text)
            if sal:
                email_text = email_text[len(sal):]
        if check_signature:
            sig = EmailParser.remove_signature(self, email_text, sender=sender, remove_phrase=remove_phrase)
            if sig:
                email_text = sig

        return email_text

    """
    Removes links and repetitive line breaks from text
    """
    @staticmethod
    def remove_links_breaks(email_text, remove_breaks=True):
        patterns = "<.*>"
        if remove_breaks:
            patterns = patterns + "|\n|\r"
        matches = re.finditer(patterns, email_text, re.IGNORECASE + re.MULTILINE)
        for match in matches:
            email_text = email_text.replace(match.group(0), " ")
        return email_text

    """
    This function searches a string to find the value associated with the email header.
    For example, in a forwarded email, if you want to find who it was sent from, then 
    Call the function get_header(email_text, "from")
    @:param header: "from", "to", "sent", or "subject", etc. 
    """
    @staticmethod
    def get_header(email_text, header):
        headerPattern = "(?<=" + header + ":).*"
        result = re.search(headerPattern, email_text, re.IGNORECASE)
        if result is not None:
            return result.group(0).strip()
        return None

    """
    This method takes in a string of an email with an email header or an email header itself 
    and returns a tuple of the (name, email) of the sender identified from the email header
    
    How it works:
    The name/email will typically be found in the "From:..." or "On... wrote:" line of an email header
    Once this line is found, the method will look for an email eg. "....@....com"
    Then it finds the name by removing anything in brackets <> [] from the line
    """
    @staticmethod
    def get_forwarded_sender(email_text):
        header = EmailParser.get_header(email_text, "From")
        if header is None:
            match = re.search("On.*wrote:", email_text, re.IGNORECASE)
            if match is not None:
                header = match.group(0)
                header = header.split(",")[-1]
                header = header.replace("wrote:", "").replace("WROTE:", "")
                header = header.strip()
            else:
                return None, None
        email_match = re.search("[\w\.-]+@[\w\.-]+(\.[\w]+)+", header)
        name = header
        email = None
        if email_match is not None:
            email = email_match.group(0).strip()
        remove_match = re.search("<.*>|\[.*\]", header)
        if remove_match is not None:
            name = header.replace(remove_match.group(0), "").strip()
        return name, email

    """
    This method looks in an email (with its string email header) to find the time that the email sent
    @:return datetime object representing the time sent found in an email header
    """
    @staticmethod
    def get_sent_date(email_text):
        result = None
        header = EmailParser.get_header(email_text, "Sent")
        if header is None:
            match = re.search("On.*wrote:|-(-| )*Forwarded message.*-(-| )*", email_text, re.IGNORECASE)
            if match is not None:
                header = match.group(0)
            else:
                return result
        dates = datefinder.find_dates(header)
        for date in dates:
            result = date
        return result

    """
    Paramter Takes in a pywintype date object (native form of dates in the outlook MAPI)
    Returns a python datetime object  
    This is used because the MAPI returns email dates in the form a pywintype objects but datetime is more versatile
    and standard in python
    """
    @staticmethod
    def pywintype_to_datetime(time):
        datetime = None
        strRep = str(time)
        dates = datefinder.find_dates(strRep)
        for date in dates:
            datetime = date
        return datetime

    """
    Parameter takes in a pywintype date object
    Returns String 'HH:MM:SS' representing the time of a email.
    """
    @staticmethod
    def pywintype_to_time(time):
        result = None
        strRep = str(time)
        match = re.search("[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", strRep)
        if match is not None:
            result = match.group(0)
        return result

