import os
from PIL import Image, ImageDraw
import face_recognition


def flatten_tuples(t): 
    # Iterate over each element in the tuple
    for x in t:
        # If the element is a tuple, recursively call flatten_tuples
        if isinstance(x, tuple):
            yield from flatten_tuples(x)
        else:
            # If the element is not a tuple, yield the element
            yield x


def _ellipse_eyes(face_landmarks, eye_size):
    """
    This function modifies eye coordinates to work with ImageDraw ellipse 
    """
    eye_halves_size = int(eye_size/2)

    # Flatten left eye coordinates tuples
    flat_left_eye_coords = tuple([
        f for f in flatten_tuples((face_landmarks['left_eye'][5], face_landmarks['left_eye'][2])) # coords sequence [x0,y0,x1,y1]
        ])

    # Reorder coords to follow the rule x0 <= x1 and y0 <=y1 needed for ellipse
    flat_left_eye_coords = [
        flat_left_eye_coords[0]-eye_halves_size, 
        flat_left_eye_coords[3]-eye_halves_size, 
        flat_left_eye_coords[2]+eye_halves_size, 
        flat_left_eye_coords[1]+eye_halves_size
        ]

    # Flatten right eye coordinates tuples
    flat_right_eye_coords = tuple([
        f for f in flatten_tuples((face_landmarks['right_eye'][5], face_landmarks['right_eye'][2])) # coords sequence [x0,y0,x1,y1]
        ])

    # Reorder coords to follow the rule x0 <= x1 and y0 <=y1 needed for ellipse
    flat_right_eye_coords = [
        flat_right_eye_coords[0]-eye_halves_size,
        flat_right_eye_coords[3]-eye_halves_size,
        flat_right_eye_coords[2]+eye_halves_size,
        flat_right_eye_coords[1]+eye_halves_size
        ]

    return flat_left_eye_coords, flat_right_eye_coords


def apply_weird_makeup_to_image(image_name, eye_size=5):
    """
    This function uses facial landmarks to draw shapes over them.
    """

    print("\nApplying digital makeup to image: ", image_name)

    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file(os.path.join("images",image_name))

    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)
    # print("\nFacial landmarks list: ", [f for f in face_landmarks_list[0].keys()])

    pil_image = Image.fromarray(image)

    for face_landmarks in face_landmarks_list:

        # Assign eyes coordinates to the respective variables
        left_eye, right_eye = _ellipse_eyes(face_landmarks, eye_size)[0], _ellipse_eyes(face_landmarks, eye_size)[1]

        d = ImageDraw.Draw(pil_image, 'RGBA')

        # Eyebrows
        d.polygon(face_landmarks['left_eyebrow'], fill=(0, 255, 255, 128))
        d.polygon(face_landmarks['right_eyebrow'], fill=(0, 255, 255, 128))
        d.line(face_landmarks['left_eyebrow'], fill=(0, 255, 255, 150), width=4)
        d.line(face_landmarks['right_eyebrow'], fill=(0, 255, 255, 150), width=4)

        # Lips
        d.polygon(face_landmarks['top_lip'], fill=(252, 142, 172, 220)) # outline
        d.line(face_landmarks['top_lip'], fill=(255,0,0, 250), width=1) # fill
        d.polygon(face_landmarks['bottom_lip'], fill=(252, 142, 172, 220)) # outline
        d.line(face_landmarks['bottom_lip'], fill=(255,0,0, 250), width=1) # fill

        # Nose
        d.polygon(face_landmarks['nose_tip'], fill=(81, 181, 63), outline=(0, 127, 0))

        # Eyes
        d.ellipse(left_eye, fill=(0, 0, 0, 255), outline=(255, 255, 255, 255))
        d.ellipse(right_eye, fill=(0, 0, 0, 255), outline=(255, 255, 255, 255))

    pil_image.show()


def main():
    image = "0.jpg"
    size=7
    apply_weird_makeup_to_image(image, size)


if __name__ == "__main__":
    main()