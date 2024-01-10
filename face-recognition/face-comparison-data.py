import os
import sys
import itertools
import json
from typing import Optional
from colorama import Fore
from colorama import Back
from colorama import Style
import face_recognition


def compare_images(img_1: str, img_2: str, tlr: float) -> Optional[str]:
    """
    This function compares two images to determine if they contain the same face.

    Parameters:
    img_1 (str): The file path of the first image.
    img_2 (str): The file path of the second image.
    tlr (float): The tolerance for the face comparison. Lower values make the comparison more strict.

    Returns:
    Optional[str]: A dictionary containing the file paths of the input images and a boolean indicating whether the faces are the same.
    """

    # Print a message indicating that the comparison is starting
    print(Back.CYAN + Fore.BLACK + f"\nComparing the face in image '{img_1}' and the face in image '{img_2}'..." + Style.RESET_ALL)

    # Load the images
    base_image = face_recognition.load_image_file(img_1)
    candidate_image = face_recognition.load_image_file(img_2)

    try:
        # Get the face encodings for the images
        base_encoding = face_recognition.face_encodings(base_image)[0]
        candidate_encoding = face_recognition.face_encodings(candidate_image)[0]
    except IndexError as e:
        # If a face cannot be found in the image, print a message and set status to an empty string
        print(Back.MAGENTA + Fore.BLACK + "The face is unidentifiable. Consider using image of a higher quality and ensure the face is visible." + Style.RESET_ALL)
        status = ""

    try:
        # Compare the faces in the images
        results = face_recognition.compare_faces(
            [base_encoding], 
            candidate_encoding, 
            tolerance=tlr # Adjust the max euclidean distance between the face vectors (lower = more strict) 0.6 by default
            )[0]
    except UnboundLocalError as e:
        # If the face encodings were not successfully created, set results to None
        results = None

    status = None
    # Print a message indicating the result of the comparison and set the status accordingly
    if results == True:
        print(Back.GREEN + Fore.BLACK + f"The faces are the same." + Style.RESET_ALL)
        status = True 
    
    elif results == False:
        print(Back.RED + Fore.BLACK + f"The faces are different." + Style.RESET_ALL)
        status = False
    
    else:
        print(Back.MAGENTA + Fore.BLACK + f"Returned: {results}" + Style.RESET_ALL)
        status = ''

    # Return a dictionary containing the file paths of the input images and the comparison result
    return {"img1":img_1,"img2":img_2,"same":status}


def main(image_dir: str, tlr: float=0.6, json_out: bool=False) -> Optional[str]:
    """
    This function compares all pairs of images in a specified directory.

    Parameters:
    image_dir (str): The directory containing the images to be compared.
    tlr (float): The tolerance for the face comparison. Lower values make the comparison more strict.
    json_out (bool): If True, the comparison results will be written to a .json file.

    Returns:
    Optional[str]: A list of dictionaries containing the file paths of the input images and a boolean indicating whether the faces are the same.
    """

    # Print a message indicating that all images will be compared to the first image in the directory
    print("\n" + Back.CYAN + Fore.BLACK + f"All images in '{image_dir}' are going to be compared to the first image." + Style.RESET_ALL)
    
    # Ask the user if they are ready to continue
    ready = input(Back.CYAN + Fore.BLACK + "Are you ready to continue? (press 'enter' to continue or type 'n' to exit):" + Style.RESET_ALL + " ")
    if ready == "":
        pass
    else:
        print(Back.CYAN + Fore.BLACK + "\nExit" + Style.RESET_ALL)
        sys.exit()
    
    # Get all image filenames in the directory
    image_filenames = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

    # Generate all possible pairs of images (excluding combinations of the same images)
    image_pairs = list(itertools.combinations(image_filenames, 2))

    # Store dictionaries with comparison results
    comparison_results = []

    # Compare each pair of images
    for index, pair in enumerate(image_pairs):
        img1 = os.path.join(image_dir, pair[0])
        img2 = os.path.join(image_dir, pair[1])
        
        comparison_results.append(compare_images(img1, img2, tlr))

        # Stop comparison when all combinations with the first image have been performed
        # '-2' since combinations() doesn't combine image with itself and number of elements > index of the last element by 1
        if index == len(image_filenames)-2: 
            print("\n" + Back.CYAN + Fore.BLACK + f"Compared {len(image_filenames)} images." + Style.RESET_ALL)
            
            # Write comparison results to .json file if parameter set to True
            if json_out:
                print(Back.CYAN + Fore.BLACK + f"Writing faces comparison data into 'faces_comparison.json' in current working directory..." + Style.RESET_ALL)
                with open("faces_comparison.json", "w") as f:
                    json.dump(comparison_results, f)
            sys.exit()

    # Return the comparison results
    return comparison_results


if __name__ == "__main__":
    main(image_dir="images", tlr=0.6, json_out=True)
