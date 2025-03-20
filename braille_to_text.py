from matplotlib import pyplot as plt
import cv2 as cv
import pytesseract

def get_string(path: str) -> str:
    """
    Reads an image from the given path, applies preprocessing, and extracts text using Tesseract OCR.
    Returns: Extracted text from the image.
    """
    img = cv.imread(path, 0)
    assert img is not None, "The file could not be read. Check the path."
    
    # Apply thresholding to enhance contrast
    _, img_thresholded = cv.threshold(img, 70, 255, cv.THRESH_BINARY_INV)
    
    # Apply Laplacian filter to enhance edges
    laplacian = cv.Laplacian(img_thresholded, cv.CV_64F)
    laplacian_abs = cv.convertScaleAbs(laplacian)

    # Show image with filters
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    
    # Titles for each subplot
    titles = ["Original Image", "Thresholded Image", "Laplacian Filter", "Absolute Laplacian"]
    
    # Images to display
    images = [img, img_thresholded, laplacian, laplacian_abs]
    
    # Loop through subplots and display each image with a title
    for ax, image, title in zip(axes.flat, images, titles):
        ax.imshow(image, cmap='gray')
        ax.set_title(title)
        ax.axis("off")

    # Adjust layout to prevent overlapping
    plt.tight_layout()
    plt.show()

    # Extract text from processed image
    text = pytesseract.image_to_string(laplacian_abs, config='--psm 6')
    return text

def generate_letters(braille: str) -> list[list[str]]:
    """
    Converts a Braille text representation into a structured matrix format.    
    Returns: list[list[str]]: 2D list representing Braille character encoding.
    """
    length_braille = 0
    for i in braille:
        if i != " ":
            length_braille += 1
        if i == "\n":
            break
    
    letter_count = length_braille // 2
    
    # Generate empty matrix with the amount of letters in the word
    word_matrix = [[] for _ in range(letter_count)] 

    # Generate plain text to facilitate construction of matrix word matrix
    plain_text = ""
    for i in braille:
        if i != " " and i != "\n":
            plain_text += i
    
    # Construct the matrix with braille code
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

    # Print word matrix
    for row in word_matrix:
        print(row)

    return word_matrix

def clean_matrix(word_matrix: list[list[str]]) -> list[list[str]]:
    """
    Replaces all non-'O' characters with 'X' to normalize the Braille matrix.
    Returns: list[list[str]]: Cleaned matrix with standardized Braille encoding.
    """
    for i, value in enumerate(word_matrix):
        for j, char in enumerate(value):
            if char == "O":
                continue
            else:
                word_matrix[i][j] = "X"
    return word_matrix

def generate_word(word_matrix: list[list[str]]) -> str:
    """
    Converts a matrix representation of Braille into a readable string.
    Returns: str: Translated text from Braille.
    """
    return ''.join(braille_dict.get(tuple(row), '?') for row in word_matrix)

braille_dict = {
    ('O', 'X', 'X', 'X', 'X', 'X'): 'A', ('O', 'X', 'O', 'X', 'X', 'X'): 'B',
    ('O', 'O', 'X', 'X', 'X', 'X'): 'C', ('O', 'O', 'X', 'O', 'X', 'X'): 'D',
    ('O', 'X', 'X', 'O', 'X', 'X'): 'E', ('O', 'O', 'O', 'X', 'X', 'X'): 'F',
    ('O', 'O', 'O', 'O', 'X', 'X'): 'G', ('O', 'X', 'O', 'O', 'X', 'X'): 'H',
    ('X', 'O', 'O', 'X', 'X', 'X'): 'I', ('X', 'O', 'O', 'O', 'X', 'X'): 'J',
    ('O', 'X', 'X', 'X', 'O', 'X'): 'K', ('O', 'X', 'O', 'X', 'O', 'X'): 'L',
    ('O', 'O', 'X', 'X', 'O', 'X'): 'M', ('O', 'O', 'X', 'O', 'O', 'X'): 'N',
    ('O', 'X', 'X', 'O', 'O', 'X'): 'O', ('O', 'O', 'O', 'X', 'O', 'X'): 'P',
    ('O', 'O', 'O', 'O', 'O', 'X'): 'Q', ('O', 'X', 'O', 'O', 'O', 'X'): 'R',
    ('X', 'O', 'O', 'X', 'O', 'X'): 'S', ('X', 'O', 'O', 'O', 'O', 'X'): 'T',
    ('O', 'X', 'X', 'X', 'O', 'O'): 'U', ('O', 'X', 'O', 'X', 'O', 'O'): 'V',
    ('X', 'O', 'O', 'O', 'X', 'O'): 'W', ('O', 'O', 'X', 'X', 'O', 'O'): 'X',
    ('O', 'O', 'X', 'O', 'O', 'O'): 'Y', ('O', 'X', 'X', 'O', 'O', 'O'): 'Z'
}

# Example usage
# In case using windows, change the path to: 'hola.png'
ejemplo1 = get_string('./braille/hola.png')
result = generate_letters(ejemplo1)
word = generate_word(result)
print(word) # Expected output: "hola"

# In case using windows, change the path to: 'taco.png'
ejemplo2 = get_string('./braille/taco.png')
result2 = generate_letters(ejemplo2)
word2 = generate_word(result2)
print(word2) # Expected output: "taco"
