import image_processor
import os

def checkMissed(input_path,output_path):
    file_list = []
    input_count = len(os.listdir(input_path))
    output_count = len(os.listdir(output_path))
    print("Total input: " ,input_count)
    print("Total processed: " ,output_count)

    for file_name in os.listdir(output_path):
        file_list.append(file_name.split(".")[0])
    for file_name in os.listdir(input_path):
        if not file_name.split(".")[0] in file_list:
            print(file_name,"was not processed")

input_path = "D:\PyCharm\Projects\GeneralImageCrawler\input\\"
output_path = "D:\PyCharm\Projects\GeneralImageCrawler\output\\"
processor = image_processor.processor(input_path,output_path,"jpg/png","png")
processor.process()
# checkMissed(input_path,output_path)
