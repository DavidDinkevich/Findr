import ast
import json
import math

model_names=['clip','yolov5','efficientnet','resnet','inceptionv3']
def get_first_interval_values(json_string):
    try:
        data = json.loads(json_string)
        first_items =[]
        for key in data:
            if key in model_names:
                if key == 'clip':
                    for result in data[key]:
                        for interval in result['intervals']:
                            first_items.append(interval[0])
                else:
                    for item in data[key]:
                        if (float(item['accuracy'])>80):
                            first_items.append(item["interval"][0])
        first_items = list(set(first_items))
        return first_items


    except json.JSONDecodeError:
        print("Invalid JSON string")
        return []
def frames_to_seconds(first_items, num_frames, length):
    seconds=[]
    for frame in first_items:
        seconds.append(int(math.floor(length * (frame / num_frames))))
    seconds=list(set(seconds))
    seconds.sort()
    print(seconds)
    return seconds

