import cv2
from PIL import Image



def show_cv2_img(cv2_img):
    """
    Transforms a cv2 image into a PIL image
    """

    return Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))


def show_multiple_cv2_imgs (list_cv2_imgs):

    """
    Transforms multiple cv2 Images into PIL images and shows them
    """

    list_PIL_imgs = []

    for img in list_cv2_imgs:
        list_PIL_imgs.append(show_cv2_img(img))

    return display(*list_PIL_imgs)