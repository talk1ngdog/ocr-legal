import cv2


def detect_horizontal_lines (cv2_img):
    """
    Detect horizontal lines in `cv2_img`

    Parameters
    ----------
    cv2_img

    Returns
    -------
    cv2 Image
        A mask containing all the horizontal lines in the original `cv2_img`
    """

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (36, 1))
    horizontal_lines = cv2.morphologyEx(cv2_img, cv2.MORPH_OPEN, horizontal_kernel, iterations = 1)

    return horizontal_lines

def detect_vertical_lines (cv2_img):
    """
    Detect vertical lines in `cv2_img`

    Parameters
    ----------
    cv2_img

    Returns
    -------
    cv2 Image
        A mask containing all the vertical lines in the original `cv2_img`
    """

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 36))
    vertical_lines = cv2.morphologyEx(cv2_img, cv2.MORPH_OPEN, vertical_kernel, iterations = 1)

    return vertical_lines
    
def remove_from_img (cv2_img, mask):
    """
    Given an image and a mask, this function removes the object contained in the mask from the image

    Parameters
    ----------
    cv2_img : cv2 Image
        Original image
    mask : cv2 Image
        Image containing the pixels to be removed from the image

    Returns
    -------
    cv2 Image
        The original image given in input without the objects contained in the mask
    """

    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    for c in contours:
        cv2.drawContours(cv2_img, [c], -1, (255,255,255), 2)

    return cv2_img
