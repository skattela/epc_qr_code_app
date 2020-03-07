import unittest

import names
from PIL import Image
from pyzbar.pyzbar import decode

import epc_qrcode


class TestSum(unittest.TestCase):

    def test_1(self):
        name = names.get_full_name()
        iban = "DE12 3456 7890 1234 5678 90"
        amount = 34.56
        reference = "Some Reason"
        additional_text = "Text"
        content = {"name": name, "iban": iban, "amount": amount, "reference": reference,
                   "additional_text": additional_text}

        image = epc_qrcode.generate_epc_qrcode_with_info(content)
        image.save("test.png")

        result = decode(Image.open('old/test.png'))
        print(result.Decoded())
        self.assertEqual(content, result)

    def test_2(self):
        name = names.get_full_name()
        iban = "DE12 3456 7890 1234 5678 90"
        amount = 34.56
        reference = "Some Reason"
        content = {"name": name, "iban": iban, "amount": amount, "reference": reference}

        image = epc_qrcode.generate_epc_qrcode(content)
        image.save("test.png")

        result = decode(Image.open('old/test.png'))
        print(result.Decoded())
        self.assertEqual(content, result)


if __name__ == '__main__':
    unittest.main()
