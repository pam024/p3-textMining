import nltk
from mrjob.job import MRJob
import re

class Preprocessor(MRJob):

    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']
    
    # def configure_args(self):
    #     super(MRJob, self).configure_args()
    #     self.add_passthru_arg('--output-dir', default='output')

    def mapper(self, _, line):
        for word in line.split():
            word = word.lower()
            word = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", word)
            if word not in self.stopwords and len(word) > 2:
                yield(word, 1)

    def reducer(self, word, counts):
        yield(word, sum(counts))

    # def reducer(self, word, counts):
    #     total_count = sum(counts)
    #     with open("./files/output.txt", 'w', encoding='utf-8') as file:
    #         file.write(f'{word}\t{total_count}\n')

    # def save_mapped_data_to_txt(self):

    #     with open("output.txt" % self.identifier, 'w', encoding='utf-8') as file:
    #         file.write(f"{key}\t{value}\n")
