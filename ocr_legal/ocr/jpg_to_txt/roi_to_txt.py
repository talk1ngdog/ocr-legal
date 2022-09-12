import pytesseract


def roi_to_txt(roi):
    """
    Takes a cv2 image and returns the text contained in it

    Parameters
    ----------
    roi : cv2 Image
        Region of image containing the block of text to be fed to the OCR engine

    Returns
    -------
    str
        The text contained in the image
    """

    txt = pytesseract.image_to_string(roi, lang='ita')

    return txt
