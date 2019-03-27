import re
import csv
import argparse

parser = argparse.ArgumentParser(description='Find phone numbers corresponding to entered provider')
parser.add_argument('-i', '--input_file', default='input.txt',
                    help='input text file to search numbers in (default: input.txt)')
parser.add_argument('-c', '--codes_file', default='ua_cell_codes.csv',
                    help='csv file to lookup provider codes (default: ua_cell_codes.csv)')
parser.add_argument('-p', '--provider', action='append',
                    help='provider name to filter phone numbers (multiple providers can be entered)')
parser.add_argument('-o', '--output_file', default='phones.csv',
                    help='csv output file to save all the phone numbers found in input that match entered providers (default: ua_cell_codes.csv)')

args = parser.parse_args()


# -i input.txt -c ua_cell_codes.csv -p "Vodafone Україна" -p lifecell -o phones.csv

def list_phone_numbers(text_file):
    l = []
    for line in text_file:
        for f in re.findall(r'((\+\d{2,3}\s*)?[(]?\d{2,3}[)]?\s*\d{3}(-?\d{2}){2})', line):
            l.append(f[0])
    return l


def get_paterns_dict(csv_file):
    d = {}
    for row in csv_file:
        d[row['number_pattern']] = row['provider']
    return d


# next function filters codes in file according to entered provider names
def filter_codes(file, providers):
    with open(file, newline='', encoding="utf8") as csvfile:
        d = {}
        reader = csv.DictReader(csvfile)
        pattern_dict = get_paterns_dict(reader)
        for pattern in pattern_dict:
            if providers is None or pattern_dict[pattern] in providers:
                d[re.sub(r'\s', '', pattern)] = pattern_dict[pattern]
        return d


def get_numbers(file, codes):
    with open(file, encoding="utf8") as input_text_file:
        d = {}
        for num in list_phone_numbers(input_text_file):
            cleaned_num = re.sub(r'[^\d]', '', num)[-9:]
            for code in codes:
                if cleaned_num[:3] == re.sub(r'[^\d]', '', code):
                    d[num] = codes[code]
                elif cleaned_num[:2] == re.sub(r'[^\d]', '', code):
                    d[num] = codes[code]
    return d


final_result = get_numbers(args.input_file, filter_codes(args.codes_file, args.provider))

with open(args.output_file, 'w', newline='', encoding="utf8") as csvfile:
    fieldnames = ['phone', 'provider']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for phone in final_result:
        writer.writerow({'phone': phone, 'provider': final_result[phone]})
