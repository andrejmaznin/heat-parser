import re

PHONE_NUMBER_REGEX = re.compile(
    r'[\+\d]?(\d{2,3}[-\.\s]??\d{2,3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'  # noqa
)

EMAIL_REGEX = re.compile(  # noqa
    """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""" # noqa
)

PERSON_NAME_REGEX = re.compile('[\u0401A-Z\u0410-\u042F]\S+\s[\u0401A-Z\u0410-\u042F]\S+')  # noqa

QUOTED_NAME_REGEX = re.compile("""[«"][\u0401A-Z\u0410-\u042F].*[»"]""")  # noqa


class Currents:
    url: str = None
    domain: str = None

    def get_currents(self):
        return {'domain': self.domain, 'url': self.url}

    def get_domain(self):
        return self.domain

    def get_url(self):
        return self.url


currents = Currents()
