import re

PHONE_NUMBER_REGEX = re.compile(
    r'[\+\d]?(\d{2,3}[-\.\s]??\d{2,3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'  # noqa
)

EMAIL_REGEX = re.compile('[a-zA-Z]+@\S+.\S+')  # noqa

PERSON_NAME_REGEX = re.compile('[\u0401A-Z\u0410-\u042F]\S+\s[\u0401A-Z\u0410-\u042F]\S+')  # noqa

QUOTED_NAME_REGEX = re.compile("""[«"]+[\u0401A-Z\u0410-\u042F].*[»"]+""")  # noqa

PROTOCOL = 'https://'


class Currents:
    path: str = None
    domain: str = None

    def get_currents(self):
        return {'domain_found': self.domain, 'path': self.path}

    def get_domain(self):
        return self.domain

    def get_url(self):
        return self.path


currents = Currents()
