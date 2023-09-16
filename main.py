from preprocessing import Preprocessor
from text_frecuency import TextMining
import os
import random 

input_dir = './text/reviews'

def run_mrjob(input_path, output_path):
    mr_job = Preprocessor(args=[input_path])
    with mr_job.make_runner() as runner:
        runner.run()
        with open(output_path, 'w') as file:
            for key, value in mr_job.parse_output(runner.cat_output()):
                file.write(f"{key}\t{value}\n")

if __name__ == '__main__':
    
    files = [os.path.join(input_dir, file)
                for file in os.listdir(input_dir) if file.endswith('.txt')]

    sample_reviews = random.sample(files,100)
    print(sample_reviews)

    for file in sample_reviews:
        output_path = "".join(["./output/", file[-10:-4], "_output", ".txt"])
        run_mrjob(file, output_path)

