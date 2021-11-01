import base64
import logging
import traceback

from cryptography.fernet import Fernet
from django.conf import settings


class Encryptor(object):
    def __init__(self):
        self.key = settings.ENCRYPTION_KEY

    def encrypt(self, text: str):
        try:
            # convert integer etc to string first
            txt = str(text)
            # get the key from settings
            cipher_suite = Fernet(self.key)  # key should be byte
            # #input should be byte, so convert the text to byte
            encrypted_text = cipher_suite.encrypt(txt.encode("ascii"))
            # encode to urlsafe base64 format
            encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
            return encrypted_text
        except Exception as e:
            # log the error if any
            logging.getLogger("error_logger").error(traceback.format_exc())
            return None

    def decrypt(self, text: str):
        try:
            # base64 decode
            txt = base64.urlsafe_b64decode(text)
            cipher_suite = Fernet(self.key)
            decoded_text = cipher_suite.decrypt(txt).decode("ascii")
            return decoded_text
        except Exception as e:
            # log the error
            logging.getLogger("error_logger").error(traceback.format_exc())
            return None
