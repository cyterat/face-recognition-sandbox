from os import path
import sys
from colorama import Fore
from colorama import Back
from colorama import Style
import face_recognition


def compare_faces(folder: str, img_1: str, img_2: str, tlr: float) -> None:

	# Check if the input directory exists
	if not path.isdir(folder):
	    print(Back.MAGENTA + Fore.BLACK + f"Input directory '{folder}' does not exist." + Style.RESET_ALL)
	    sys.exit()

	# img_2 = "false0.jpg" # TEST: similar face but different person in real life; should return False
	# img_2 = "error0.jpg" # TEST: similar face but different person in real life; should return Error

	print(Back.CYAN + Fore.BLACK + f"Comparing the face in image '{img_1}' and the face in image '{img_2}'..."+ Style.RESET_ALL)

	base_image = face_recognition.load_image_file(path.join(folder, img_1))
	candidate_image = face_recognition.load_image_file(path.join(folder, img_2))

	try:
		biden_encoding = face_recognition.face_encodings(base_image)[0]
		unknown_encoding = face_recognition.face_encodings(candidate_image)[0]
	except IndexError as e:
		print(Back.MAGENTA + Fore.BLACK + "The face is unidentifiable. Consider using image of a higher quality and ensure the face is visible." + Style.RESET_ALL)
		sys.exit()

	# Run face_recognition function
	results = face_recognition.compare_faces(
		[biden_encoding], 
		unknown_encoding, 
		tolerance=tlr # Adjust the max euclidean distance between the face vectors (lower = more strict) 0.6 by default
		)[0]

	# Return stylized status of the dace_recognition run
	if results == True:
		print(Back.GREEN + Fore.BLACK + f"The face in '{img_1}' and the face in '{img_2}' are the same." + Style.RESET_ALL) 
	elif results == False:
		print(Back.RED + Fore.BLACK + f"The face in '{img_1}' and the face in '{img_2}' are different." + Style.RESET_ALL)
	else:
		print(Back.MAGENTA + Fore.BLACK + f"Got something weird: {results}" + Style.RESET_ALL)


def main():
	folder = "medvedchuk"
	img_1 = "2.jpg"
	img_2 = "3.jpg"
	tlr = 0.6 

	compare_faces(folder, img_1, img_2, tlr)


if __name__ == '__main__':
	main()


