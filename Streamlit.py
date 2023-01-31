import streamlit as st
import cv2
from streamlit_option_menu import option_menu
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, VideoProcessorBase, WebRtcMode
import streamlit.components.v1 as components
import requests
from streamlit_lottie import st_lottie
RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})


# class MobileCamera:
#     def getVideo(self, camera):
#         self.camera = camera
#         cap = cv2.VideoCapture(self.camera)
#         while True:
#             ret, frame = cap.read()
#
#
#         cap.release()
#         cv2.destroyAllWindows()

# cam = MobileCamera()
placeholder = st.empty()
checker = True
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

class VideoTransformer(VideoTransformerBase):
    def transform1(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # img = cv2.flip(img, 1)
        cv2.putText(img, "label", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        # key = cv2.waitKey(1)

        return img

lottie_thief = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_i72c01.json")

with st.sidebar:
    selected = option_menu(
        menu_title="Instrusion Warning",
        options=["Home","Camera", "Notification", "Config Area"],
        menu_icon="cast",
        default_index=0,
        icons=["house","webcam","bell","gear"]
    )

if selected == "Home":
    st.title("PROJECT2: INSTRUSION WARNING")
    col1, col2 = st.columns(2)
    with col1:
        st.header("What is an Intrusion Warning System?")
        st.write("An intrusion warning system is a system whose aim is to monitor and detect unauthorized access to a building. These systems are used for different purposes and in different contexts both residential or commercial. The main purpose of an intrusion alarm system is to protect from burglary, vandalism, property damage, and, of course, the security of the individuals inside the building.")
    with col2:
        st_lottie(lottie_thief)
    checker = st.checkbox("Check", value=True)
if selected == "Camera":
    st.title("Instrusion Warning Camera")
    webrtc_ctx = webrtc_streamer(
        key="opencv-filter",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=VideoTransformer,
        media_stream_constraints={
            "video": {
                "width": {"min": 800, "ideal": 1200, "max": 1920},
            }
        },
        async_processing=True,
    )
if selected == "Notification":
    st.title("Notification History")
if selected == "Config Area":
    st.title("Config Area")



def show_alert():
    a = components.html(
        """
        <style>
        body {
        position: relative
        }
    .alert-noti {
      position: absolute;
      top: 0px;
      right:50px;
      width: 250px;
      background-color: #eee;
      border-radius: 5px;
      overflow: hidden;
      padding: 16px;
      border-left: 5px solid red;
      box-shadow: 10px 10px 8px #888888;
        color: red;
      font-weight: 600;
    }
    .alert-delete {
      position: absolute;
      top: 0;
      right: 0;
      padding: 3px;
      cursor: pointer;
    }
    .icon-delete {
      width: 20px;
      height: 20px;
       color: black;
    }
    </style>
        <div class="alert-noti">
          <span>Có Kẻ Đột Nhập</span>
          <div class="alert-delete">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="icon-delete"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </div>
        </div>
        """
    )
    return a


while True:
    if checker == True:
        placeholder.warning('Có Kẻ Xâm Nhập', icon="⚠️")
    else:
        placeholder.success('Khu Vực An Toàn', icon="✅")





