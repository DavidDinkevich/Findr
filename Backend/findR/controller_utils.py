import ast
import json
import math

model_names=['clip','yolov5','efficientnet','resnet','inceptionv3']
def process_results(json_string):
    try:
        data = json.loads(json_string)
        first_items =[]
        processed_results= {}
        num_frames= data['num_frames']
        for key in data:
            if key in model_names:
                model_dict = {}
                intervals = []
                accuracies = []
                if key == 'clip':
                    for result in data[key]:
                            for interval in result['intervals']:
                                intervals.append(interval)
                                accuracies.append(int(result['accuracy'])*3)
                                if (float(result['accuracy']) > 27):
                                    first_items.append(interval[0])
                else:
                    for item in data[key]:
                        intervals.append(item["interval"])
                        accuracies.append(float(item['accuracy']))
                        if (float(item['accuracy'])>80):
                            first_items.append(item["interval"][0])
                intervals, accuracies = sort_and_unzip_lists(key,intervals, accuracies)
                model_dict['intervals']=intervals
                model_dict['accuracies']=accuracies
                model_dict['num_frames']=num_frames
                processed_results[key]=model_dict
        first_items = list(set(first_items))
        return first_items, processed_results


    except json.JSONDecodeError:
        print("Invalid JSON string")
        return []
def frames_to_seconds(first_items, num_frames, length):
    seconds=[]
    for frame in first_items:
        seconds.append(int(math.floor(length * (frame / num_frames))))
    seconds=list(set(seconds))
    seconds.sort()
    return seconds

def sort_and_unzip_lists(key,intervals, accuracies):
    # Zip the intervals and accuracies together
    if len(intervals) > 1:
        zipped_data = list(zip(intervals, accuracies))
        # Sort the zipped data based on the intervals
        sorted_data = sorted(zipped_data, key=lambda x: x[0])

        # Unzip the sorted data into separate lists
        sorted_intervals, sorted_accuracies = zip(*sorted_data)

        return list(sorted_intervals), list(sorted_accuracies)
    return intervals, accuracies


def overall_results(processed_results):
    pass


