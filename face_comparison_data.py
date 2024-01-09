import os
import sys
import itertools
import json
from typing import Optional
from colorama import Fore
from colorama import Back
from colorama import Style
import face_recognition


# Your image comparison function
def compare_images(img_1: str, img_2: str, tlr: float) -> Optional[str]:

    print(Back.CYAN + Fore.BLACK + f"\nComparing the face in image '{img_1}' and the face in image '{img_2}'..." + Style.RESET_ALL)

    base_image = face_recognition.load_image_file(img_1)
    candidate_image = face_recognition.load_image_file(img_2)

    try:
        biden_encoding = face_recognition.face_encodings(base_image)[0]
        unknown_encoding = face_recognition.face_encodings(candidate_image)[0]
    except IndexError as e:
        print(Back.MAGENTA + Fore.BLACK + "The face is unidentifiable. Consider using image of a higher quality and ensure the face is visible." + Style.RESET_ALL)
        status = ''

    try:
        # Run face_recognition function
        results = face_recognition.compare_faces(
            [biden_encoding], 
            unknown_encoding, 
            tolerance=tlr # Adjust the max euclidean distance between the face vectors (lower = more strict) 0.6 by default
            )[0]
    except UnboundLocalError as e:
        results = None

    status = None
    # Return stylized status of the dace_recognition run
    if results == True:
        print(Back.GREEN + Fore.BLACK + f"The faces are the same." + Style.RESET_ALL)
        status = True 
    
    elif results == False:
        print(Back.RED + Fore.BLACK + f"The faces are different." + Style.RESET_ALL)
        status = False
    
    else:
        print(Back.MAGENTA + Fore.BLACK + f"Returned: {results}" + Style.RESET_ALL)
        status = ''

    return {'img1':img_1,'img2':img_2,'same':status}



def main(image_dir: str, tlr: float=0.6, json_out: bool=False) -> Optional[str]:

    print("\n" + Back.CYAN + Fore.BLACK + "All images are going to bo compared to the first image in the secified directory." + Style.RESET_ALL)
    ready = input(Back.CYAN + Fore.BLACK + "Are you ready to continue? (press 'enter' to continue or type 'n' to exit):" + Style.RESET_ALL + " ")
    if ready == 'n':
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
                print(Back.CYAN + Fore.BLACK + f"Writing faces comparison data into 'faces_comparison.json' in '{image_dir}' folder..." + Style.RESET_ALL)
                with open("faces_comparison.json", "w") as f:
                    json.dump(comparison_results, f)
            sys.exit()

    comparison_results()


if __name__ == '__main__':
    
    image_dir = "medvedchuk"

    main(image_dir, tlr=0.6, json_out=True)