from PIL import Image, ImageFilter, ImageEnhance
import os
from Crawler import Crawl

class processor:
    def __init__(self, input, output, input_format,output_format):
        if not os.path.isdir(input):
            os.mkdir(input)
        if not os.path.isdir(output):
            os.mkdir(output)
        self.input_path = input
        self.output_path = output
        self.input_format = input_format.split("/")
        self.output_format = output_format

    def processImage(self, image):

        image=image.convert('L')
        image = image.filter(ImageFilter.GaussianBlur(radius=1))
        image = image.filter(ImageFilter.CONTOUR)
        contrast = ImageEnhance.Contrast(image)
        image = contrast.enhance(2)
        return image

    def process(self):
        for file in Crawl(self.input_path):
            file_format = file.split(".")[len(file.split("."))-1]
            if file_format in self.input_format:
                try:
                    image = Image.open(file)
                    image = self.processImage(image)
                    base_name = os.path.basename(file).split(".")[0]
                    file_name = (self.output_path+"/"+base_name+"."+self.output_format)
                    image.save(file_name, self.output_format)
                except OSError:
                    print("Could not open file!")
