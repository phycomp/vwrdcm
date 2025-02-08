# dicom_server.py
from tornado.ioloop import IOLoop#tornado.ioloop.
from tornado.web import RequestHandler, Application
from pydicom import dcmread
import numpy as np
import cv2
import json
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class DicomUploadHandler(RequestHandler):
    async def post(self):
        file = self.request.files['dicom_file'][0]
        filename = file['filename']
        save_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(save_path, 'wb') as f:
            f.write(file['body'])
        
        ds = dcmread(save_path)
        pixel_array = ds.pixel_array
        
        # DICOM圖像預處理
        if 'WindowWidth' in ds:
            img = self.apply_windowing(pixel_array, ds)
        else:
            img = self.normalize_image(pixel_array)
        
        preview_path = self.generate_preview(img, filename)
        
        response = {
            "meta": {
                "PatientID": ds.get('PatientID', ''),
                "StudyDate": ds.get('StudyDate', ''),
                "Modality": ds.get('Modality', '')
            },
            "preview_url": f"/preview/{os.path.basename(preview_path)}"
        }
        self.write(response)

    def apply_windowing(self, arr, ds):
        # 實現窗寬窗位處理
        pass

class AnnotationHandler(tornado.web.RequestHandler):
    def post(self):
        annotation_data = json.loads(self.request.body)
        # 保存標注到數據庫/文件系統
        self.write({"status": "success"})

def make_app():
    return Application([
        (r"/upload", DicomUploadHandler),
        (r"/annotate", AnnotationHandler),
        (r"/preview/(.*)", tornado.web.StaticFileHandler, {"path": "previews"})
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    IOLoop.current().start()
