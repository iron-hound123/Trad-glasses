import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic


def mediapipe_detection (image,model):
  #We do conversion because opencv takes immage to BGR but mediapipe needs RGB for detection
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #Color conversion BGR -> RGB
  image.flags.writeable = False                  #
  results = model.process(image)                 #Make prediction with holistic model
  image.flags.writeable= True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #color conversion RGB -> BGR
  return image,results

def draw_landmarks(image,results):
  mp_drawing.draw_landmarks(
        image,
        results.face_landmarks,
        mp_holistic.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_contours_style())
  mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.
        get_default_pose_landmarks_style())
  mp_drawing.draw_landmarks(
        image,
        results.right_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,)
  mp_drawing.draw_landmarks(
        image,
        results.left_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,)

def extract_keypoints(results):
  face=np.array([[res.x,res.y,res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(1404)
  pose=np.array([[res.x,res.y,res.z,res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(132)
  left_hand=np.array([[res.x,res.y,res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
  right_hand=np.array([[res.x,res.y,res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
  return np.concatenate([face,pose,left_hand,right_hand]) 
cap = cv2.VideoCapture(0)

first=True

#Access MediaPipeModel
with mp_holistic.Holistic(
    model_complexity=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Make detections
    image,results = mediapipe_detection(image,holistic)
    
    draw_landmarks(image,results)
    rh=extract_keypoints(results)
    print(rh.shape)
    
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('Trad-glasses', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()