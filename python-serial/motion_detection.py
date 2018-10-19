# import the necessary packages
from imutils.video import VideoStream
import datetime
import imutils
import time
import cv2
import API
from time import sleep
from telegram.ext import Updater, CommandHandler
import telegram
import subprocess


is_armed = False

def alert(frames, api, bot, chat_id):
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    # api.alert_leds()
    message = "Alert: " + now
    print(message)

    subprocess.call(["ffplay", "-nodisp", "-autoexit", "./sounds/horn.wav"])

    try:
        bot.send_message(chat_id=chat_id, text=message)
    except:
        print("failed to send to user")

    for frame in frames:
        # save image
        file_path = "./images/" + now + ".jpg"
        cv2.imwrite(file_path, frame)
        # send image
        # try:
        #     bot.send_photo(chat_id=chat_id, photo=open(file_path, 'rb'))
        # except:
        #     print("failed to send image")
        # sleep(1.5)


def motion_detection(min_area, api, bot, chat_id):
    global is_armed
    # webcam
    vs = VideoStream(src=0).start()
    # vs = cv2.VideoCapture(0)
    time.sleep(2.0)

    is_alerted = False
    alert_time = datetime.datetime.now()

    # initialize the first frame in the video stream
    firstFrame = None

    # loop over the frames of the video
    while True:
        # only do vision if camera is armed
        if not is_armed:
            firstFrame = None
            continue
        # grab the current frame and initialize the occupied/unoccupied
        # text
        frame = vs.read()
        text = "Unoccupied"

        # end of stream
        if frame is None:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < min_area:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"

            frames = []

            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            frames.append(frame)

            for _ in range(3):
                frame = vs.read()
                frame = imutils.resize(frame, width=500)

                cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

                frames.append(frame)
                sleep(0.25)

            alert(frames, api, bot, chat_id)

            # video
            # height, width, layers = frame.shape
            # video_out = cv2.VideoWriter('test.avi', -1, -1 (width, height))
            # video_out = cv2.VideoWriter('test.avi', -1, -1 (500, 500))

            # start_time = time.time()
            # print("RECORDING VIDEO")
            # while time.time() - start_time < 5:
            #   frame = vs.read()
            #   frame = imutils.resize(frame, width=500)
            #   video_out.write(frame)
            # print("FINISHED RECORDING VIDEO")

            # video_out.release()


        # draw the text and timestamp on the frame
        # cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        #   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        #   (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # show the frame and
        # cv2.imshow("Security Feed", frame)
        # cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame Delta", frameDelta)

        # key = cv2.waitKey(1) & 0xFF

        # # if the `q` key is pressed, break from the lop
        # if key == ord("q"):
        #     break

    # cleanup the camera and close any open windows
    vs.stop()
    # vs.stop() if args.get("video", None) is None else vs.release()
    cv2.destroyAllWindows()


# telegram bot
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
    print(update.message.chat_id)

def send_txt(bot, chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)

def arm(bot, update):
    global is_armed
    
    if is_armed:
        bot.send_message(chat_id=update.message.chat_id, text="I am already armed")
    else:
        is_armed = True
        bot.send_message(chat_id=update.message.chat_id, text="I am now armed")

def disarm(bot, update):
    global is_armed
    
    if is_armed:
        is_armed = False
        bot.send_message(chat_id=update.message.chat_id, text="I am now disarmed")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="I am already disarmed")

def help(bot, update):
    message = "Once armed if motion is detected an alert will be sent via message including pictures with time stamps and the LEDs will light up too.\n /arm arms Homie Bot\n/disarm disarms Homie Bot\n/help this menu"
    bot.send_message(chat_id=update.message.chat_id, text=message)

def start_program():
    global is_armed

    lochie_chat_id = 487912709
    bot_token = "629389428:AAGeiLSafnaVEwTfqA67TNpNcucnPsE2HTo"
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(CommandHandler('arm', arm))
    dispatcher.add_handler(CommandHandler('disarm', disarm))
    dispatcher.add_handler(CommandHandler('help', help))
    updater.start_polling()

    bot = telegram.Bot(bot_token)
    send_txt(bot, lochie_chat_id, "Homie Bot, at your service!\ntype /help for information")

    # bot.send_photo(chat_id=lochie_chat_id, photo=open('TEST.jpg', 'rb'))
    # quit()

    # api = API.API("/dev/ttyACM0")
    # api.alert_leds()
    api = None
    is_armed = True
    motion_detection(500, api, bot, lochie_chat_id)




if __name__ == "__main__":
    start_program()
