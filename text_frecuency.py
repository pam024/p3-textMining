import os
import numpy as np 
import pandas as pd
import math
import re

class TextMining:
    
    def __init__(self, path_files):        
        # self.random_reviews = os.listdir(path_files)[1:]
        self.random_reviews = os.listdir(path_files)
        self.tf = []
        self.df = []
        self.idf = []
        self.tf_idf_list = []
        self.dir = path_files
        self.tf_idf_norm = []
        self.idf_dict = {}
        # self.process_query = process_query
    
    def preprocess(self):
        # documents = self.random_reviews if self.process_query else self.random_reviews 
        for output_review in self.random_reviews:
            with open (self.dir + "/" + output_review, 'rt', encoding='utf-8')  as file:
            
                word_counts = {}
                sum_values = 0
                
                for line in file:
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    key, value = parts
                 
                    sum_values += int(value)
                                        
                    # Almacena el conteo para esta palabra
                    word_counts[key] = int(value)

                # Divide cada valor por el total de valores
                for word in word_counts:
                    aux = word_counts[word] / sum_values                        
                    word_counts[word] = aux 
                    
                self.tf.append(word_counts)
        
    
    def tf_function(self, frequency_list):
        dt_tf = pd.DataFrame(frequency_list)
        dt_tf = dt_tf.fillna(0)
        
        dict_tf = dict(dt_tf)
        print("TF: \n", dt_tf)
        return dt_tf
        
    def df_function(self, dt_tf):
        doc_set = set(dt_tf.columns)
        word_df = {word: 0 for word in doc_set}     
        for i in self.tf: 
            for j in doc_set:
                if j in i:
                    word_df[j] += 1

        aux = sorted(word_df.items(), key=lambda item:item[1])
        aux.reverse()
        sorted_dict = dict(aux)
        df = pd.DataFrame(aux)
        print("DF: \n", df) 
        return sorted_dict
    
    def top_ten_reviews(self, sorted_dict):
        
        top_ten_words = dict(list(sorted_dict.items())[:10])
        # top_10 = dict(sorted(sorted_dict.items(), key=lambda item: item[1], reverse=True)[:10])
        for key, value in sorted_dict.items():
            print("{:<8} {:<15}".format(key, value))
        return top_ten_words

    def idf_function(self, sorted_dict):
        self.idf_dict = {}
        for word, value in sorted_dict.items():
            idf_value = math.log(len(self.random_reviews)/value, 10) 
            self.idf_dict[word] = idf_value 
        
        self.idf.append(self.idf_dict)
        df_idf = pd.DataFrame(self.idf) 
        print("IDF: \n", df_idf)
        return self.idf_dict
        

    def tf_idf_function(self, dt_tf, idf_dict):
        lista = dt_tf.to_dict(orient='records')
        
        for i in lista:
            tf_idf = {}
            for key,value in i.items():
                tf_idf[key] = i[key]*idf_dict[key]
            
            self.tf_idf_list.append(tf_idf)
        
        df_tf_idf = pd.DataFrame(self.tf_idf_list)
        print("TF-IDF: \n", df_tf_idf)
        return df_tf_idf
    
    def tf_idf_normalized_function(self, df_tf_idf):
        norm = np.linalg.norm(df_tf_idf.values,axis=1)
        self.tf_idf_norm = (df_tf_idf.T/norm).T
            
        print("NORM: \n", self.tf_idf_norm)
        return self.tf_idf_norm

    def tf_idf_query_normalized_function(self, query):
        
        query_vector = self.tf_idf_norm.T.iloc[:,0]
        
        for word, value in query_vector.items():
            query_vector.at[word] = 0

        sum_values = 0
        w_frequency = {}
        for word in query.split():
            word = word.lower()
            word = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", word)
            sum_values += 1

            if word not in w_frequency:
                w_frequency[word] = 0
            w_frequency[word] += 1
        # Divide cada valor por el total de valores
        for word in w_frequency:
            aux = w_frequency[word] / sum_values                        
            w_frequency[word] = aux

        for key, value in w_frequency.items():
            if key in query_vector:
                query_vector.at[key] = value * self.idf_dict[key]


        # Calculate the magnitude (length) of the vector
        magnitude = np.linalg.norm(query_vector)

        # Normalize the vector
        norm_query_vector = query_vector / magnitude

        print (norm_query_vector)
        return norm_query_vector


    def cosine_similarity(self, document_vector):
        dot_product = self.tf_idf_norm.dot(document_vector)
        print(dot_product)
        return dot_product



    def run(self):

        self.preprocess()
        tf = self.tf_function(self.tf)
        df = self.df_function(tf)
        # top_ten = self.top_ten_reviews(df)
        idf = self.idf_function(df)
        tf_idf = self.tf_idf_function(tf, idf)
        tf_idf_normalized = self.tf_idf_normalized_function(tf_idf)
        query = self.tf_idf_query_normalized_function("betty character atmosphere cannot color")
        # self.cosine_similarity(query)
    
        self.cosine_similarity(tf_idf_normalized.T)
        


    
    
