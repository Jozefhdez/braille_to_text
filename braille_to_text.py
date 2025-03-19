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

def generate_letters(braille: str) -> list[list[str]]:
    length_braille = 0
    for i in braille:
        if i != " ":
            length_braille += 1
        if i == "\n":
            break
    
    letter_count = length_braille // 2
    
    word_matrix = [[] for _ in range(letter_count)] 
 
    plain_text = ""
    for i in braille:
        if i != " " and i != "\n":
            plain_text += i
    
    index_matrix = 0
    for i in range(0, letter_count * 2, 2):
        word_matrix[index_matrix].append(plain_text[i])
        word_matrix[index_matrix].append(plain_text[i + 1])
        word_matrix[index_matrix].append(plain_text[i + length_braille - 1])
        word_matrix[index_matrix].append(plain_text[i + length_braille])
        word_matrix[index_matrix].append(plain_text[i + (length_braille * 2) - 2])
        word_matrix[index_matrix].append(plain_text[i + (length_braille * 2) - 1])
        index_matrix += 1
    
    word_matrix = clean_matrix(word_matrix)

    for row in word_matrix:
        print(row)

    return word_matrix

def clean_matrix(word_matrix: list[list[str]]) -> list[list[str]]:
    for i, value in enumerate(word_matrix):
        for j, char in enumerate(value):
            if char == "O":
                continue
            else:
                word_matrix[i][j] = "X"
    return word_matrix