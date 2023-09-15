from preprocessing import Preprocessor
import os
import subprocess
import multiprocessing

input_dir = './files'

# mr_job = Preprocessor(args=[input_path])

# with mr_job.make_runner() as runner:
#     runner.run()
#     with open(output_path, 'w') as file:
#         for key, value in mr_job.parse_output(runner.cat_output()):
#             file.write(f"{key}\t{value}\n")

def run_mrjob(input_path, output_path):
    mr_job = Preprocessor(args=[input_path])
    with mr_job.make_runner() as runner:
        runner.run()
        with open(output_path, 'w') as file:
            for key, value in mr_job.parse_output(runner.cat_output()):
                file.write(f"{key}\t{value}\n")

files = [os.path.join(input_dir, file)
            for file in os.listdir(input_dir) if file.endswith('.txt')]

threads = []
output_num = 0
for file in files:
    output_path = "".join(["./output/", str(output_num), ".txt"])
    print(output_path)
    run_mrjob(file, output_path)
    # thread = multiprocessing.Process(target=run_mrjob, args=(file, output_path))
    # threads.append(thread)
    # thread.start()
    output_num += 1

# for thread in threads:
#     thread.start()

# Wait for all threads to finish
# for thread in threads:
#     thread.join()



# Specify the input and output file paths
# input_path = './files/input.txt'
# output_path = 'output.txt'

# cmd = ['python', 'preprocessing.py', input_path, '>', output_path]


# cmd = ' '.join(cmd) 
# subprocess.call(cmd, shell=True)
