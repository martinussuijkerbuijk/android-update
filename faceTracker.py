import cv2
import numpy as np
from numpy import interp
import serial


# Set video object
video = cv2.VideoCapture(0)
width = 640
height = 480
video.set(3, width) #Setting webcam's image width video_capture.set(4,480) #Setting webcam' image height
video.set(4, height)

# Arduino stuff
ser_android = serial.Serial('COM3', 19200, timeout=1)

# Set parameters for face extraction and other ones
models_path = "D:/Github/facialAttributeClassification/models"

#Load predictor
facecascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye = cv2.CascadeClassifier("haarcascade_eye.xml")

rangeX = [102, 78]
rangeY = [60, 120]


def crop_face(img, face, padding): #Crop the given face
    for (x, y, w, h) in face:
        if y - padding <= 0:
            y0 = 0
        else:
            y0 = y - padding
        if x - padding <= 0:
            x0 = 0
        else:
            x0 = x - padding
        faceslice = img[y0:y+h+padding, x0:x+w+padding]
    return faceslice


#black bar width
bar = 129

def gen():
    """Video streaming generator function."""
    while True:
        ret, frame = video.read()
        #frame = frame[:, bar:1024 - bar]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_image = clahe.apply(gray)


        face = facecascade.detectMultiScale(clahe_image, scaleFactor=1.1, minNeighbors=15, minSize=(10, 10),
                                            flags=cv2.CASCADE_SCALE_IMAGE)
        # eye_track = eye.detectMultiScale(clahe_image, scaleFactor=1.1, minNeighbors=15, minSize=(10, 10),
        #                                     flags=cv2.CASCADE_SCALE_IMAGE)


        if len(face) == 1:  # Use simple check if one person is detected
            x, y, w, h = face[0]
            x_mean = np.mean((x, x+w))
            y_mean = np.mean((y, y+h))
            cv2.circle(frame, (int(x_mean), int(y_mean)), radius=2, color=(255, 0, 0), thickness=1)
            rad_x = interp(x_mean, [0,width], rangeX)
            rad_y = interp(y_mean, [0,height], rangeY)

            # Send to serial port
            ser_android.write(f"{str(int(rad_x))}x".encode())
            ser_android.write(f"{str(int(rad_y))}y".encode())


        elif len(face) > 1: # focus on one person
            for e in face[:1]:
                x, y, w, h = e
                x_mean = np.mean((x, x + w))
                y_mean = np.mean((y, y + h))
                cv2.circle(frame, (int(x_mean),int(y_mean)), radius=2, color=(255,0,0), thickness=1)
                # Send to serial port
                ser_android.write(f"{str(int(rad_x))}x".encode())
                ser_android.write(f"{str(int(rad_y))}y".encode())
        else:
            ser_android.write(f"{str(90)}x".encode())
            ser_android.write(f"{str(90)}y".encode())
            cv2.imshow("face tracker", frame)

        cv2.imshow("face tracker", frame)
        # press q to Quit
        if cv2.waitKey(10) & 0xFF == ord('q'):
            ser_android.write(f"{str(90)}x".encode())
            ser_android.write(f"{str(90)}y".encode())

            break
    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    gen()
