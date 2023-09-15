import os
import random 
import numpy as np 
import re

from preprocessing import Preprocessor


class TextMining:
    
    def __init__(self):
        self.random_reviews = [] 
        
    def random_review(self):
        #random reviews
        reviews = []        
        reviews = os.listdir("./text/reviews")

        self.random_reviews = random.sample(reviews, 100)
    
        return self.random_reviews
    
    #funcion calculos
    def calculations(self):
        tf = []
        df = []
        idf = []
        tf_idf = []

        words_set = set()
        
        for i in self.random_reviews:
            with open ("./text/reviews/"+i, 'rt', encoding='utf-8')  as file:
                
                word_counts = {}
                sum_values = 0
                
                for line in file:
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    key, value = parts
                    
                    if key in self.result:
                        self.result[key] += int(value)
                    else:
                        self.result[key] = int(value)
                
                    sum_values += int(value)
                                        
                    # Almacena el conteo para esta palabra
                    word_counts[word] = int(value)

                    # Divide cada valor por el total de valores
                    for word in word_counts:
                        aux = word_counts[word] / sum_values                        
                        word_counts[word] = aux 
                        tf.append(word_counts[word])
                         
                    print(tf)
                
        #print(corpus)
        print(i)
        
        #print("Wordset: ", words_set)
        print('Number of words in the corpus:', len(words_set))
        
        print("Words len:", len(words))
            
        #print('The words in the corpus: \n', words_set) 
    
    #print top 10 words
    
if __name__ == '__main__':
    t = TextMining()
    
    p = Preprocessor()    
    
    review_len = t.random_review()
    #print(len(review_len))
    print(review_len)
    
    t.calculations()
    
    #p.mapper()
    #print(p.mapper())
    
    #p.reducer()
