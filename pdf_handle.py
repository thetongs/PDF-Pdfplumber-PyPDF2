## Working with PDFs using pdfplumber and pypdf2
#

## Installations
# pip install PyPDF2
# pip install pdfplumber

## Requirements
#
import PyPDF2
import pdfplumber

def meta_data():
    pdf = pdfplumber.open("CV.pdf")

    print("Number of pages : {}".format(len(pdf.pages)))
    print("Pages : {}".format(pdf.pages))

    print("Document Information")
    print(pdf.metadata)

    print("Author name : {}".format(pdf.metadata["Author"]))
    print("Creator : {}".format(pdf.metadata["Creator"]))

    pdf.close()

def extract_first():
    pdf = pdfplumber.open("CV.pdf")
    page = pdf.pages[0]
    text = page.extract_text()

    print("First page data : {}".format(text))
    pdf.close()

def extract_whole():
    pdf = pdfplumber.open("CV.pdf")
    n = len(pdf.pages)

    final = ""
    for page in range(n):
        data = pdf.pages[page].extract_text()
        final = final + "\n" + data
    
    print("Whole document data : {}".format(final))

    pdf.close()

def rotation_check():
    pdf = pdfplumber.open("CV.pdf")
    l = int(pdf.pages[0].rotation)

    if(l):
        print("Page is rotated by : {}".format(l))
    else:
        print("Page is not rotated")
    
    # Using PyPDF2

    pdf_obj = open("CV.pdf", 'rb')
    pdf_read_obj = PyPDF2.PdfFileReader(pdf_obj)
    pdf_read_page_rotation = pdf_read_obj.getPage(0).get("/Rotate")

    if(pdf_read_page_rotation == None):
        print("This page is not rotated")
    else:
        print("Page is rotated bye : {}".format(pdf_read_page_rotation))
    
def rotate_back():
    pdf_obj = open("Rotated_CV.pdf", 'rb')
    pdf_read_obj = PyPDF2.PdfFileReader(pdf_obj)
    n_pages = pdf_read_obj.getNumPages()
    for n in range(n_pages):
        pdf_read_page_rotation = pdf_read_obj.getPage(n).get("/Rotate")
        pdf_read_page_rotation = int(pdf_read_page_rotation)

        if(pdf_read_page_rotation):
            pdf_read_page_obj = pdf_read_obj.getPage(n)
            pdf_read_page_obj.rotateCounterClockwise(pdf_read_page_rotation)

            pdfwritter = PyPDF2.PdfFileWriter()
            pdfwritter.addPage(pdf_read_page_obj)

            pdf_obj1 = open("Rotated_CV1.pdf", "wb")
            pdfwritter.write(pdf_obj1)
            pdf_obj.close()
            pdf_obj1.close()

def merger():
    file_names = ["Rotated_CV.pdf", "Rotated_CV1.pdf"]
    merger = PyPDF2.PdfFileMerger()

    for pdf in file_names:
        with open(pdf, "rb") as file:
            merger.append(pdf)

    with open("merger.pdf", "wb") as f:
        merger.write(f)
    
    print("Merger done")

def splitter():
    with open('merger.pdf', 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        n = reader.getNumPages()

        for page in range(n):
            writter = PyPDF2.PdfFileWriter()
            writter.addPage(reader.getPage(page))

            op_file = "split_{}.pdf".format(page)
            print("Splitted : {}".format(op_file))

            with open(op_file, 'wb') as f:
                writter.write(f)
        
        print("Splitting done")

if(__name__ == "__main__"):
    meta_data()
    extract_first()
    extract_whole()
    rotation_check()
    rotate_back()
    merger()
    splitter()

## End
