from schwifty import IBAN, BIC
import qrcode

# |PL|62114020040000350278400642|000100|abc|przelew|||
# |{country_code}|{account_number}|{amount}|{recipient_name}|{title}|||
# country_code = 'PL' - Polska
# account_number = '13 1160 2202 0000 0000 2987 3563' - Polski Czerwony Krzyż

# def print_receipt - print a receipt on the zebra printer which will include the qr code and all the details of the transaction
# def log_transaction - log the transaction details for auditing purposes. It could write the transaction details to a file or a database.

def inputs():
    country_code = input("Podaj kod kraju: ")
    account_number = input("Podaj numer konta: ")
    amount = input("Podaj kwote: ")
    recipient_name = input("Podaj nazwe odbiorcy: ")
    title = input("Podaj tytul przelewu: ")

    checking(country_code, account_number, amount)
    get_string_from_template(country_code, account_number, amount, recipient_name, title)
    return country_code, account_number, amount, recipient_name, title


def get_string_from_template(country_code, account_number, amount, recipient_name, title):
    template = f"|{country_code}|{account_number}|{amount}|{recipient_name}|{title}|||"
    return template


def amount_conversion(amount):
    return str(int(amount * 100)).zfill(8)


def checking(country_code, account_number, amount):
    country_code = country_code.upper()
    amount = amount.replace(",", ".")
    try:
        iban = IBAN(country_code + account_number)
        print(iban)
    except:
        print("Invalid country code or account number")
        exit()
    
    try:
        if amount.count(".") > 1 or amount == "" or amount == "0":
            raise ValueError
        float(amount)
    except ValueError:
        print("Podaj poprawna kwote")
        exit()
    
    return country_code, iban, amount

def qr_code(template):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(template)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save("qrcode.png")
    return img

country_code, account_number, amount, recipient_name, title = inputs()
country_code, iban, amount = checking(country_code, account_number, amount)
amount_str = amount_conversion(float(amount))
template = get_string_from_template(country_code, iban[2:], amount_str, recipient_name, title)
img = qr_code(template)

print(iban)
print(iban.formatted)
print(iban.bic)
print(template)
img.show()