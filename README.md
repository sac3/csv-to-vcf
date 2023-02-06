csv_to_vcf

A Python script to convert a CSV file containing contact information to a VCF file (vCard 2.1 format). The script also fetches the photos from a URL and resizes them to 300px width while maintaining the aspect ratio. The script prints the progress of the conversion.

Requirements
Python 3.x
csv module
base64 module
requests module
io module
PIL module
Input
The script expects a CSV file containing the following columns:

first_name
last_name
phone_number
email (optional)
photo_url (optional)

Output
The script outputs a VCF file with the same name as the input CSV file but with a .vcf extension.

Usage
scss
Copy code
csv_to_vcf(csv_file, vcf_file)
where:

csv_file: the name of the input CSV file
vcf_file: the name of the output VCF file

Example
python
Copy code
csv_to_vcf("contacts.csv", "contacts.vcf")


Limitations
The script only supports vCard version 2.1 and assumes that the columns in the CSV file are named as specified in the Input section. The script also assumes that the photos are in JPEG format. If your data is in a different format, you'll need to modify the code accordingly.