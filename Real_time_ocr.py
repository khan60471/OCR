import cv2
import pytesseract
import pyttsx3

# Configure the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize the TTS engine
tts_engine = pyttsx3.init()

def preprocess_image(image):
    """
    Preprocess the image for better OCR results.
    - Convert to grayscale
    - Apply bilateral filter to reduce noise while keeping edges sharp
    - Use adaptive thresholding to enhance text regions
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    return thresh

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    preprocessed_frame = preprocess_image(frame)

    # Perform OCR
    text = pytesseract.image_to_string(preprocessed_frame)

    if text.strip():
        # Convert the recognized text to speech
        tts_engine.say(text)
        tts_engine.runAndWait()

    # Display the OCR results on the frame
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the frame with the detected text
    cv2.imshow('Real-Time OCR with TTS', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
# Set properties for the TTS engine
tts_engine.setProperty('rate', 150)    # Speed of speech
tts_engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
