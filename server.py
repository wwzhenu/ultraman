import asyncio
import base64
import tornado.web
import json
import cv2
import numpy as np
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

faceCascade = cv2.CascadeClassifier(
    r"/usr/local/lib/python3.9/site-packages/cv2/data/haarcascade_frontalface_default.xml")

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)

        img = data["img"]
        imgData = base64.b64decode(img)

        img1 = cv2.imdecode(np.array(bytearray(imgData)),cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.15,
            minNeighbors=5,
            minSize=(5, 5)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
            cv2.putText(img1, "KUN", (x, y), font, 1, (0, 255, 0), 2)
        
        newImgData = np.array(cv2.imencode('.jpg',img1)[1])
        # tempFile = open("a.jpg", mode="ab")
        # tempFile.write(newImgData)
        # tempFile.close()

        resp = dict()
        resp["img"] = str(base64.b64encode(newImgData),'utf-8')
        resp["name"] = "迪迦奥特曼"
        self.write(resp)


async def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(options.port)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
