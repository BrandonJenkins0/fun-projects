# Importing modules
import PyPDF2
import time
from itertools import chain
import pandas as pd
import warnings
import sys
warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    file_location = input("Enter file path for PDF: ").replace("\"", "")
    pdfFileObj = open(file_location, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    page_numbers = pdfReader.getNumPages()
    done = []
    number = []
    vendor = []

    for num in range(page_numbers):
        page = pdfReader.getPage(num)
        page_ser = pd.Series([x.strip().replace('\n', '') for x in page.extractText().replace('--', '  ').split('  ')])
        page_ser_filt = page_ser[page_ser != ''].reset_index(drop=True)
        mapp = page_ser_filt[page_ser_filt.str.contains('Returned:')].index + 1
        usd_filt = page_ser_filt[page_ser_filt.str.contains('USD')].index - 1
        c = list(page_ser_filt[mapp].values)
        d = list(page_ser_filt[usd_filt])
        if len(d) > 0:
            vendor.append(d)
        if len(c) > 0:
            done.append(c)
            number.append([num + 1] * (len(c)))

    amounts = list(chain.from_iterable(done))
    number = list(chain.from_iterable(number))
    del amounts[-1]; del number[-1]
    vendor = pd.Series(chain.from_iterable(vendor)).drop_duplicates().reset_index(drop=True)
    final_dat = pd.DataFrame({'Page Number': number, 'Vendor': vendor, 'Amounts': amounts}).set_index('Page Number')
    final_dat.to_clipboard()

    print('\n            SUCCESS!')
    print('\nThe values are now in your clipboard.\n')
    print('\nClosing window in ...')
    for i in range(6, 0, -1):
        sys.stdout.write(str(i) + ' ')
        sys.stdout.flush()
        time.sleep(1)


if __name__ == '__main__':
    main()
