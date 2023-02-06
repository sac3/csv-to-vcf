import csv
import base64
import requests
from io import BytesIO
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

def csv_to_vcf(csv_file, vcf_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        contacts = list(reader)
        total_contacts = len(contacts)
        
        with open(vcf_file, 'w') as v:
            with ThreadPoolExecutor(max_workers=5) as executor:
                # Start a new thread for each contact
                futures = [executor.submit(process_contact, contact, i, total_contacts, v) for i, contact in enumerate(contacts)]
                
                # Wait for all threads to finish
                for future in futures:
                    future.result()

def process_contact(contact, index, total_contacts, v):
    print("Processing contact {} of {}".format(index+1, total_contacts))
    photo_url = contact.get('photo_url')
    email = contact.get('email', '')
    if photo_url:
        response = requests.get(photo_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            width, height = img.size
            if width > 250:
                new_height = int(250 * height / width)
                img = img.resize((250, new_height), Image.ANTIALIAS)
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            encoded_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
            photo = "PHOTO;ENCODING=BASE64;TYPE=JPEG:{}\n".format(encoded_string)
        else:
            photo = ""
    else:
        photo = ""

    v.write("BEGIN:VCARD\n")
    v.write("VERSION:2.1\n")
    v.write("N:{0};{1}\n".format(contact['last_name'], contact['first_name']))
    v.write("FN:{0} {1}\n".format(contact['first_name'], contact['last_name']))
    v.write("TEL;TYPE=HOME,VOICE:{0}\n".format(contact['phone_number']))
    if email:
        v.write("EMAIL;TYPE=INTERNET,HOME:{}\n".format(email))
    v.write(photo)
    v.write("END:VCARD\n")

csv_to_vcf("contacts.csv", "contacts.vcf")
