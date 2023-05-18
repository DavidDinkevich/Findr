import subprocess
import time

if __name__ == '__main__':
    cmd = ['python', './child_proc_test.py']
    child_proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        encoding='utf8'
    )

    while True:
        print(f'Parent: sending message: message')
        child_proc.stdin.write('message\n')
        child_proc.stdin.flush()

        print('Parent: waiting for response')
        response = child_proc.stdout.readline().strip()
        print(f'Parent: got response: {response}')


        # time.sleep(1)










    # # Reconstruct intervals for original video
    # for model_name in query_dict['models']:
    #     # Skip procs that failed
    #     if procs[model_name].returncode != 0:
    #         continue
    #     if 'clip_' in model_name:
    #         model_type = 'clip_'
    #     elif 'yolo' in model_name:
    #         model_type = 'yolo'
    #     else:
    #         raise NotImplementedError("Haven't implemented models other than yolo and clip_")
    #
    #     output_file = f'{model_name}_results.json'
    #     reconstruct_and_write_original_intervals(model_type, output_file, reconstruction_map)
    #
    #     with open(output_file, 'r') as f:
    #         response[model_name] = json.load(f)









