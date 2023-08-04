# importing required modules
from pypdf import PdfReader
import functions as func
 

content = []
def filterPage(text, cm, tm, fontDict, fontSize):
    
    # idk, some objects have bigger fontSize but these are not texts
    # if not fontSize == 1.0:
    #     return

    # print(fontDict['/BaseFont'])
    
    # text on first page
    # if fontDict['/BaseFont'] == '/YDEHYS+Majoris-Regular':
    #     return


    # if fontDict["/BaseFont"] == '/CNYOHE+TimesNewRomanPSMT':

    isAppended = False

    if text == '':
        return
    
    text = text.replace('\n', "<br>")

    while '  ' in text:
        text = text.replace('  ', ' ')
    
    if text == ' ':
        i = len(content)
        content[i-1] = content[i-1] + ' '
        return

    if '. <br>' not in text:
        # text = text.replace('<br>', '<a style="color:#FF0000">UMBURCH ENTFERNT</a>')
        text = text.replace('<br>', '')

    if '. <br>' in text:
        text = text + '</p><p style="background:#DCDCDC; margin: 10px;">'

    if ' / 164' in text:
        text = text + '<br><p style="background:#DCDCDC; margin: 10px;">'

    # if fontDict["/BaseFont"] == "/YOFADM+FiraSans-Regular":
    #     text = '<a style="color:#FF00FF">' + text + "<a>"

    # if fontSize == 1.0:
    #     text = '<a style="color:#FF00FF">' + text + "<a>"

    # print(fontDict)
    # print(fontDict["/FontDescriptor"])
    # print(fontDict["/FontDescriptor"]["/Ascent"])

    content.append(text)

  
def store(p_content):
    f = open("output-edit.html", "w")
    # f.write(func.toString(p_content))
    f.write(func.toString(p_content))
    f.close()


def main():
    print("PDF EXTRACTOR")

    #create PDFReader and read File
    reader = PdfReader(open('all.pdf', 'rb'))
    
    #iterate over all pages and filter content
    print("Extracting...")

    reader.pages[4].extract_text(visitor_text=filterPage)

    # for p in reader.pages:
    #     p.extract_text(visitor_text=filterPage)


    content.append('</p>')

    #store filtered page in file
    store(content)

if __name__ == '__main__':
    main()