import cv2
from natsort import natsorted
import os
import pandas as pd
from tqdm import tqdm

from ocr_legal.ocr.jpg_to_txt.jpg_to_roi import threshold, dilate_text_blocks, detect_text_blocks
from ocr_legal.ocr.jpg_to_txt.roi_to_txt import roi_to_txt
from ocr_legal.ocr.pdf_to_jpg.functions import from_pdf_to_jpg_folder


def from_jpg_folder_to_list_strings(path_to_document_folder):
    '''
    Take a folder containing each page of the document as a jpg (e.g. Document1 > page_0.jpg, page_1.jpg, ...) and ocr each page

    Parameters
    ----------
    path_to_document_folder : str
        Path to the folder that contains the jpg of the pages to be ocr'ed

    Returns
    -------
    list
        A list of strings where first element is the first page, second is the second page and so on
    '''

    text_pages = []

    for filename in natsorted(os.listdir(path_to_document_folder)):

        # get the whole page
        jpg_complete_text = cv2.imread(path_to_document_folder + '/' + filename, cv2.IMREAD_GRAYSCALE)

        # get only the main body of the document
        jpg_roi = detect_text_blocks(*dilate_text_blocks(threshold(jpg_complete_text), jpg_complete_text), return_only_biggest_box=True)
        text_pages.append(roi_to_txt(jpg_roi))

    return text_pages

def from_pdf_folder_to_dataframe(path_to_pdf_folder, path_to_output_folder):
    '''
    Take a folder with pdf and return a dataframe with the text in the pdf

    Parameters
    ----------
    path_to_pdf_folder : str
        Path to the folder containing the documents to ocr
    path_to_output_folder : str
        Path to the folder containing the documents in jpg

    Returns
    -------
    pandas DataFrame
        This dataframe contains in each row a document id and the body of the document
    '''

    # iterate over the pdf files and create the jpg
    for filename in natsorted(os.listdir(path_to_pdf_folder)):
        if filename.endswith('.pdf'):
            from_pdf_to_jpg_folder(path_to_pdf_folder + '/' + filename, path_to_output_folder)


    df = pd.DataFrame(columns = ['document_id', 'body'])

    # iterate over the folders containing the jpg and create an entry of the dataframe
    for i, document in tqdm(enumerate(natsorted(os.listdir(path_to_output_folder)))):
        txt_document_body = from_jpg_folder_to_list_strings(str(path_to_output_folder) + '/' + document)
        df.loc[i] = {'document_id': str(document), 'body': txt_document_body}

    return df
#%%
