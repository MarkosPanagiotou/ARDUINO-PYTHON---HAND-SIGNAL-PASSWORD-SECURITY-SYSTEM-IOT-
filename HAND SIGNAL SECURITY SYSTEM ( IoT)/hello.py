import cv2
import controller as cnt
from cvzone.HandTrackingModule import HandDetector
import time

# -------------------- Setup --------------------
detector = HandDetector(detectionCon=0.8, maxHands=1)
video = cv2.VideoCapture(0)

password = [5, 2, 3, 4, 2, 1, 0]

current_step = 0
attempts = 0
max_attempts = 5
per_finger_delay = 1.5  # δευτερόλεπτα για να σηκώσεις το επόμενο finger
ready_timer = 5          # δευτερόλεπτα πριν ξεκινήσει η διαδικασία
refresh_time = 5         # δευτερόλεπτα μετά επιτυχία

# -------------------- Helper --------------------
def reset_sequence():
    global current_step
    current_step = 0

# -------------------- Ready Countdown --------------------
for i in range(ready_timer,0,-1):
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, f"Get Ready: {i}", (200,200),
                cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255),5)
    cv2.imshow("frame", frame)
    cv2.waitKey(1000)

print("🎯 Start hand-signal input!")

# -------------------- Main Loop --------------------
can_input = True  # flag για να δέχεται input μόνο όταν True
refresh_start = None
show_success = False
success_display_time = 2  # seconds to show "Success!" on camera
success_start = None

while True:
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)

    hands, img = detector.findHands(frame)
    finger_count = 0
    fingerUp = [0,0,0,0,0]

    if hands:
        lmList = hands[0]
        fingerUp = detector.fingersUp(lmList)
        finger_count = sum(fingerUp)

        if can_input:
            expected_finger = password[current_step]

            if finger_count == expected_finger:
                print(f"Step {current_step+1}: Correct ({finger_count}) ✅")
                cnt.send_fingers(fingerUp)
                current_step += 1

                # 1.5 δευτερολέπτων για να σηκώσεις το επόμενο finger
                start_time = time.time()
                while time.time() - start_time < per_finger_delay:
                    ret, frame = video.read()
                    frame = cv2.flip(frame, 1)
                    hands,_ = detector.findHands(frame)
                    if hands:
                        fingerUp = detector.fingersUp(hands[0])
                        finger_count = sum(fingerUp)
                        cv2.putText(frame, f"Finger count: {finger_count}", (20,460),
                                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                    cv2.imshow("frame", frame)
                    if cv2.waitKey(1) == ord("k"):
                        break

            elif finger_count !=0:  # λάθος
                print(f"Step {current_step+1}: Wrong ({finger_count}) ❌")
                cnt.buzzer_wrong()
                attempts +=1
                time.sleep(0.5)
                if attempts >= max_attempts:
                    print("⚠️ Emergency! Too many wrong attempts!")
                    cnt.buzzer_emergency()
                    attempts =0
                    reset_sequence()

        # ------------------ Sequence complete ------------------
        if current_step == len(password) and can_input:
            print("🎉 Password Correct! All LEDs ON")
            cnt.send_fingers([1,1,1,1,1])  # ανάβουν όλα τα LEDs
            cnt.buzzer_success()
            can_input = False
            refresh_start = time.time()  # ξεκινάει ο 5 δευτερολέπτων χρονομετρητής
            show_success = True
            success_start = time.time()

    # ------------------ Show success message ------------------
    if show_success:
        elapsed_success = time.time() - success_start
        cv2.putText(frame, "SUCCESS! ✅", (150, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
        if elapsed_success >= success_display_time:
            show_success = False

    # ------------------ Refresh timer ------------------
    if not can_input:
        elapsed = time.time() - refresh_start
        cv2.putText(frame, f"Refresh in: {int(refresh_time - elapsed)+1}s", (100,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255),3)
        if elapsed >= refresh_time:
            reset_sequence()
            can_input = True
            attempts = 0
            print("🔄 Ready for new attempt")

    # Display live finger count
    cv2.putText(frame, f"Finger count: {finger_count}", (20,460),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("k"):
        break

video.release()
cv2.destroyAllWindows()
