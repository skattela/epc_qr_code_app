import qrcode
from PIL import Image, ImageDraw, ImageFont


def generate_epc_qrcode(content):
    print("Generationg qr_code")

    name = content.get("name")
    iban = content.get("iban")
    amount = content.get("amount")
    reference = content.get("reference")

    # Add euro if missing
    # validate iban
    # add float with 2 digits
    # iban = iban.replace(" ", "")
    # amount = float(amount)
    # reference = reference.strip()

    qr_code_raw = "BCD\n002\n1\nSCT\n\n%s\n%s\nEUR%s\n%s" % (name, iban, amount, reference)
    print(qr_code_raw)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # 15%
        box_size=10,
        border=4,
    )
    qr.add_data(qr_code_raw)
    qr.make(fit=True)

    qr_code_image = qr.make_image(fill_color="black", back_color="white")
    # qr_code_image.show()
    print("generated qr_code")
    return qr_code_image


def generate_epc_qrcode_with_info(content):
    qr_code_image = generate_epc_qrcode(content)
    print("Adding info picture to qr_code")
    qr_code_image_width, qr_code_image_height = qr_code_image.size
    # print(qr_code_image_height)
    # print(qr_code_image_width)

    name = content.get("name")
    iban = content.get("iban")
    amount = content.get("amount")
    reference = content.get("reference")

    fnt = ImageFont.truetype('LT_50138.ttf', 20)
    text = "Name: %s\nIBAN: %s\nAmount: EUR%.2f\nReference: %s" % (name, iban, amount, reference)
    if content.get("additional_text"):
        text += "\n\n%s" % content.get("additional_text")
    text_image = Image.new(mode="RGB", size=(qr_code_image_width, qr_code_image_height), color="white")
    draw = ImageDraw.Draw(text_image)
    draw.text((0, 100), text, fill="black", font=fnt)

    image = Image.new(mode="RGB", size=(qr_code_image_width * 2, qr_code_image_height), color="white")
    image.paste(qr_code_image, (0, 0))
    image.paste(text_image, (qr_code_image_width, 0))
    # image.save("epc-qrcode.png")
    # image.show()
    # file = open("epc-qrcode.png", 'rb')
    print("Added info image to qr_code")
    return image
