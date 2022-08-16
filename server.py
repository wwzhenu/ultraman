import asyncio
import base64
import tornado.web
import json
import cv2
import numpy as np
import sqlite3
from deploy.python.predict_system import predictSingleImg

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

conn=sqlite3.connect("ultraman.db")

class MainHandler(tornado.web.RequestHandler):    
    def post(self):
        # 获取图片数据
        data = json.loads(self.request.body)
        img = data["img"]
        imgData = base64.b64decode(img)
        # 读取图片
        img1 = cv2.imdecode(np.array(bytearray(imgData)),cv2.IMREAD_COLOR)
        # 预测
        data = predictSingleImg("deploy/configs/inference_ultraman.yaml",img1)
        name = 'marin'
        # 获取预测到的图片名称
        if len(data) > 0:
            rs = data[0]
            name = rs['rec_docs']        
        # 数据查询
        sql = "SELECT * FROM ultraman WHERE name = '%s'" % name
        row = conn.execute(sql).fetchone()
        # 返回
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
