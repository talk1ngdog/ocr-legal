#%%
#%%
import os
from glob import glob
from pdf2image import convert_from_path


def from_pdf_to_jpg_folder(pdf_file, output_folder):
    """
    It takes a pdf file and transforms it into a folder by the same name which contains each page stored as a jpg

    Parameters
    ----------
    pdf_file : str
        The path to the pdf file
    output_folder : str
        The path to the folder that will contain each document stored as a collection of jpg
    """

    # get the last name in the path and then remove its extension (usually .pdf)
    pdf_file_without_ext = os.path.splitext(os.path.basename(pdf_file))[0]

    if not os.path.isdir(output_folder + '/' + pdf_file_without_ext):
        os.makedirs(output_folder + '/' + pdf_file_without_ext)

    # this converts the pdf into a list of PIL images
    images = convert_from_path(pdf_file)

    counter = 0
    for img in images:
        img.save(output_folder + '/' + pdf_file_without_ext + '/page_' + str(counter) + '.jpg')
        counter += 1

    return
