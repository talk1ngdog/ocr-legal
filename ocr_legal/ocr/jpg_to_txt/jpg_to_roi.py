import cv2

def threshold (cv2_img):
    """
    Threshold the image's pixels to 0 or 255

    Parameters
    ----------
    cv2_img

    Returns
    -------
    cv2 Image
        A thresholded cv2 image (its pixels' intensity are either 0 or 255)
    """

    # turn pixels black or white
    return cv2.threshold(cv2_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


def dilate_text_blocks (thresh_img, orig_img, kernel_shape = cv2.MORPH_RECT, size = (64, 64)):
    """
    Given a jpg image it dilates the text contained to help with the detection

    Parameters
    ----------
    thresh_file : cv2 Image
        A thresholded cv2 image (its pixels' intensity are either 0 or 255)

    orig_img : cv2 Image in grayscale
        The original image before dilation that will be automatically passed to `detect_text_blocks`

    kernel_shape :
        The shape of the kernel used to dilate the image (e.g. rectangle, ellipse, ...)

    size : (int, int)
        The size of the kernel

    Returns
    -------
    numpy.ndarray
        A cv2 image with dilated text
    str
        The path to the original image, it's returned so that it can be fed directly to `detext_text_blocks`
    """


    # get the kernel and dilate the image according to it
    kernel = cv2.getStructuringElement(kernel_shape, size)
    dilated_image = cv2.dilate(thresh_img, kernel, iterations = 1)

    return dilated_image, orig_img

def detect_text_blocks (cv2_dilated_image, orig_img, return_only_biggest_box = False):
    """
    To be used in conjunction with `dilate_text_blocks` it detects the dilated text blocks

    Parameters
    ----------
    cv2_dilated_image : numpy.ndarray
        A cv2 image (that is stored in memory as a numpy array), it's suggested to be the output of `dilate_text_blocks`

    orig_img : cv2 Image in grayscale
        The original image before dilation

    return_only_biggest_box : bool
        Flag variable, the function instead of returning all the text blocks, only returns the biggest one
        (we assume this is the box that contains the body of text of the document)

    Returns
    -------
    list
        A list of regions of `img_file` that hopefully contain blocks of texts
    """

    contours, _ = cv2.findContours(cv2_dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    roi_regions = []

    for c in contours:
        # here we get the rectangle that best fit the contour coordinates
        x, y, w, h = cv2.boundingRect(c)

        # store the regions with blocks of text
        roi_regions.append(orig_img[y:y+h, x:x+w])

    if return_only_biggest_box:
        sum_dimensions = [sum(x.shape) for x in roi_regions]
        index_maximum = sum_dimensions.index(max(sum_dimensions))
        return roi_regions[index_maximum]

    return roi_regions