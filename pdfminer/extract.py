from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("sample.pdf")

pdf_writer = PdfWriter()

pdf_writer.add_page(reader.pages[5])
pdf_writer.add_page(reader.pages[6])
pdf_writer.add_page(reader.pages[7])
pdf_writer.add_page(reader.pages[8])


with open("small.pdf",'wb') as out:
    pdf_writer.write(out)