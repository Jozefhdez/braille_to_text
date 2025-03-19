from matplotlib import pyplot as plt
import cv2 as cv
import pytesseract

def get_string(path: str) -> str:
    img = cv.imread(path, 0)
    assert img is not None, "The file could not be read. Check the path."

    _, img_thresholded = cv.threshold(img, 70, 255, cv.THRESH_BINARY_INV)
    laplacian = cv.Laplacian(img_thresholded, cv.CV_64F)
    laplacian_abs = cv.convertScaleAbs(laplacian)

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    titles = ["Original Image", "Thresholded Image", "Laplacian Filter", "Absolute Laplacian"]
    images = [img, img_thresholded, laplacian, laplacian_abs]
    for ax, image, title in zip(axes.flat, images, titles):
        ax.imshow(image, cmap='gray')
        ax.set_title(title)
        ax.axis("off")

    plt.tight_layout()
    plt.show()

    # Extract text from processed image
    text = pytesseract.image_to_string(laplacian_abs, config='--psm 6')
    return text