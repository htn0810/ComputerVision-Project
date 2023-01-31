import cv2
import numpy as np
import time
import requests
import streamlit as st
import streamlit.components.v1 as components
import json
# Add Authen lib
import pickle
import streamlit_authenticator as stauth
from pathlib import Path

from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

from yoloDetect import YoloDetect

points = [[188, 122], [446, 119], [444, 442], [188, 441], [188, 122]]
detect = True
pre_time_frame = 0
new_time_frame = 0
model = YoloDetect(detect_class="person", frame_width=640, frame_height=480)
openCamera = False

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_thief = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_i72c01.json")
st.set_page_config(page_title="Instrument Warning",
                   page_icon=":no_pedestrians:",
                   layout="centered",
                   initial_sidebar_state="expanded",
                   menu_items=None)

# USER AUTHENTICATION
names = ["Thanh Nhan", "Van Phong"]
usernames = ["htnhan", "hvphong"]
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,"cokkie_name", "random_key", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("Login", "main")
if authentication_status == False:
    st.error("Username/password is incorrect")
if authentication_status == None:
    st.warning("Please enter your username and password")
if authentication_status:
    placeholder = st.empty()
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    with st.sidebar:
        selected = option_menu(
            menu_title="Instrusion Warning",
            options=["Home","Camera", "Notification", "Config Area"],
            menu_icon="cast",
            default_index=0,
            icons=["house","webcam","bell","gear"]
        )
    if selected == "Home":
        openCamera = False
        st.title("PROJECT2: INSTRUSION WARNING")
        col1, col2 = st.columns(2)
        with col1:
            st.header("What is an Intrusion Warning System?")
            st.write("An intrusion warning system is a system whose aim is to monitor and detect unauthorized access to a building. These systems are used for different purposes and in different contexts both residential or commercial. The main purpose of an intrusion alarm system is to protect from burglary, vandalism, property damage, and, of course, the security of the individuals inside the building.")
        with col2:
            st_lottie(lottie_thief)
    if selected == "Camera":
        openCamera = True
        #checkCamera = True
        st.title("Instrusion Warning Camera")
        frame_window = st.image([])
    if selected == "Notification":
        openCamera = False
        st.title("Notification")
        st.image("alert.png")
    if selected == "Config Area":
        openCamera = False
        st.title("Config Area")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            pst1 = st.text_input("Coordinate1",value="", placeholder="Position1...")
        with col2:
            pst2 = st.text_input("Coordinate2", value="", placeholder="Position2...")
        with col3:
            pst3 = st.text_input("Coordinate3", value="", placeholder="Position3...")
        with col4:
            pst4 = st.text_input("Coordinate4", value="", placeholder="Position4...")
        with col5:
            btnChange = st.button("CHANGE")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Black_from_a_camera.jpg/640px-Black_from_a_camera.jpg")


    def handle_left_click(event, x, y, flags, points):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append([x, y])

    def draw_polygon(frame, points):
        for point in points:
            frame = cv2.circle(frame, (point[0], point[1]), 5, (0, 0, 255), -1)
        frame = cv2.polylines(frame, [np.int32(points)], False, (255, 0, 0), thickness=2)
        return frame

    class MobileCamera:
        def getVideo(self, camera):
            global pre_time_frame, new_time_frame, detect, openCamera, frame_window, points
            self.camera = camera
            cap = cv2.VideoCapture(self.camera)
            while openCamera:
                instru_check = False
                new_time_frame = time.time()
                fps = 1/(new_time_frame - pre_time_frame)
                pre_time_frame = new_time_frame
                fps = int(fps)
                ret, frame1 = cap.read()
                ret, frame2 = cap.read()
                if not ret:
                    break
                diff = cv2.absdiff(frame1, frame2)
                frame2 = draw_polygon(frame2, points)
                if detect:
                    if diff is not None:
                        frame2, checker = model.detect(frame= frame2, points= points, instru_check=instru_check)
                        if checker:
                            placeholder.error('Có Kẻ Xâm Nhập', icon="⚠️")
                        else:
                            placeholder.success('Khu Vực An Toàn', icon="✅")

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
                # elif key == ord('d'):
                #     points.append(points[0])
                #     print(points)
                #     detect = True


                cv2.putText(frame2, str(fps) + " FPS", (500, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Intrusion Warning", frame2)
                cv2.setMouseCallback('Intrusion Warning', handle_left_click, points)
                rgb_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
                frame_window.image(rgb_frame)

            cap.release()
            cv2.destroyAllWindows()

    if(openCamera):
        cam = MobileCamera()
        cam.getVideo("http://10.230.208.185:4747/video")




