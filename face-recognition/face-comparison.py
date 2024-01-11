# Import necessary libraries
from os import path
import sys
import time
from colorama import Fore
from colorama import Back
from colorama import Style
import face_recognition

# Function to compare faces in two images
def compare_faces(folder: str, img_1: str, img_2: str, tlr: float) -> None:
    # Check if the input directory exists
    if not path.isdir(folder):
        # Print error message and exit if directory does not exist
        print(Back.MAGENTA + Fore.BLACK + f"Input directory '{folder}' does not exist." + Style.RESET_ALL)
        sys.exit()

    # Print status message
    print(Back.CYAN + Fore.BLACK + f"Comparing the face in image '{img_1}' and the face in image '{img_2}'..." + Style.RESET_ALL)

    # Load the base and candidate images
    base_image = face_recognition.load_image_file(path.join(folder, img_1))
    candidate_image = face_recognition.load_image_file(path.join(folder, img_2))

    try:
        # Get the face encodings for the base and candidate images
        base_encoding = face_recognition.face_encodings(base_image)[0]
        candidate_encoding = face_recognition.face_encodings(candidate_image)[0]
    except IndexError as e:
        # Print error message and exit if face is unidentifiable
        print(Back.MAGENTA + Fore.BLACK + "The face is unidentifiable. Consider using image of a higher quality and ensure the face is visible." + Style.RESET_ALL)
        sys.exit()

    # Run face_recognition function
    results = face_recognition.compare_faces(
        [base_encoding], 
        candidate_encoding, 
        tolerance=tlr # Adjust the max euclidean distance between the face vectors (lower = more strict) 0.6 by default
        )[0]

    # Print the result of the face comparison
    if results == True:
        print(Back.GREEN + Fore.BLACK + f"The face in '{img_1}' and the face in '{img_2}' are the same." + Style.RESET_ALL) 
    elif results == False:
        print(Back.RED + Fore.BLACK + f"The face in '{img_1}' and the face in '{img_2}' are different." + Style.RESET_ALL)
    else:
        print(Back.MAGENTA + Fore.BLACK + f"Got something weird: {results}" + Style.RESET_ALL)

# Main function
def main():
    # Define the folder and image names
    folder = "images"
    img_1 = "2.jpg"
    img_2 = "false0.jpg" # TEST: similar face but different person in real life; should return False
    tlr = 0.6 

    # Start the timer
    tic = time.perf_counter()
    # Run the face comparison
    compare_faces(folder, img_1, img_2, tlr)
    # Stop the timer
    toc = time.perf_counter()
    # Print the elapsed time
    print(Back.CYAN + Fore.BLACK + f"\nCompared images in {toc - tic:0.4f} seconds"+ Style.RESET_ALL)

# Run the main function
if __name__ == '__main__':
    main()


