import asyncio
import base64
import tornado.web
import json
import cv2
import numpy as np
import sqlite3

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
define("path", default="/usr/local/lib/python3.9/site-packages/cv2/data/haarcascade_frontalface_default.xml", help="run on the given port", type=str)

conn=sqlite3.connect("ultraman.db")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("ultraman.xml")
class MainHandler(tornado.web.RequestHandler):    
    def post(self):
        faceCascade = cv2.CascadeClassifier(options.path)
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
            tmp_img = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(tmp_img)
            sql = "SELECT * FROM ultraman WHERE id = %d" % label
            row = conn.execute(sql).fetchone()
        
        newImgData = np.array(cv2.imencode('.jpg',img1)[1])

        resp = dict()
        # resp["img"] = str(base64.b64encode(newImgData),'utf-8')
        # resp["name"] = "迪迦奥特曼"
        resp["img"] = row[2]
        resp["name"] = row[1]
        self.write(resp)


async def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(options.port)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
