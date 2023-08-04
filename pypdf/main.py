# importing required modules
from pypdf import PdfReader
import functions as func
 

content = []
def filterPage(text, cm, tm, fontDict, fontSize):
    
    # idk, some objects have bigger fontSize but these are not texts
    if not fontSize == 1.0:
        return

    print(fontDict['/BaseFont'])
    
    # text on first page
    # if fontDict['/BaseFont'] == '/YDEHYS+Majoris-Regular':
    #     return


    if fontDict["/BaseFont"] == '/CNYOHE+TimesNewRomanPSMT':
        content.append(text)

  
def store(p_content):
    f = open("output-edit.txt", "w")
    f.write(func.toString(p_content))
    f.close()


def main():
    print("PDF EXTRACTOR")

    #create PDFReader and read File
    reader = PdfReader(open('all.pdf', 'rb'))
    
    #iterate over all pages and filter content
    print("Extracting...")

    reader.pages[1].extract_text(visitor_text=filterPage)

    # for p in reader.pages:
    #     p.extract_text(visitor_text=filterPage)

    #store filtered page in file
    store(content)

if __name__ == '__main__':
    main()