import os

from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage

# 
import cv2
from PIL import Image
import numpy as np
import tensorflow as tf

from .utils import FileStorage


def home(request):
    status = ""
    output = ""
    fss = FileStorage()
    try:
        image = request.FILES["image"]
        print("Name", image.file)
        _image = fss.save(image.name, image)
        path = str(settings.MEDIA_ROOT) + "/" + image.name
        # image details
        image_url = fss.url(_image)
        # Read the image
        img = cv2.imread(path)
        img_arr = Image.fromarray(img, "RGB")
        resized_img = img_arr.resize((50,50))

        # 
        input = np.expand_dims(resized_img, axis=0)

        # load model
        model = tf.keras.models.load_model(str(settings.BASE_DIR) + "/model.h5")
        result = model.predict(input)

        x = str(np.argmax(result))
        print("Here is ", x)
        if x == "0":
            output = "Cat"
        elif x == "1":
            output = "Dog"
        elif x == "2":
            output = "Monkey"
        elif x == "3":
            output = "Parrot"
        elif x == "4":
            output = "Elephant"
        elif x == "5":
            output = "Bear"
        else:
            output = "Error"
        print("Out", output)
       
        return TemplateResponse(
            request,
            "home.html",
            {
                "status": "Image Uploaded",
                "image": image,
                "image_url": image_url,
                "output": output
            },
        )
    except MultiValueDictKeyError:

        return TemplateResponse(
            request,
            "home.html",
            {"status": "No Image Selected"},
        )
