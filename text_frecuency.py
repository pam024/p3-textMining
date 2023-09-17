import os
import numpy as np 
import pandas as pd
import math
import re
import matplotlib.pyplot as plt

class TextMining:
    
    def __init__(self, path_files):        

        self.random_reviews = os.listdir(path_files)
        self.tf = []
        self.df = []
        self.idf = []
        self.tf_idf_list = []
        self.dir = path_files
        self.tf_idf_norm = []
        self.idf_dict = {}
    
    def preprocess(self):
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
        dt_tf.index = self.random_reviews
        dt_tf.to_csv('./tables/dt_tf_table.csv', sep=',', index=True, encoding='utf-8')

        
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
        df.to_csv('./tables/dt_table.csv', sep=',', index=True, encoding='utf-8')
        print("DF: \n", df) 
        return sorted_dict
    
    def top_ten_reviews(self, sorted_dict):
        
        top_ten_words = dict(list(sorted_dict.items())[:10])
        print("Top Ten Words from Dataset")
        for key, value in top_ten_words.items():
            print("{:<8} {:<15}".format(key, value))
        print()
        return top_ten_words

    def idf_function(self, sorted_dict):
        self.idf_dict = {}
        for word, value in sorted_dict.items():
            idf_value = math.log(len(self.random_reviews)/value, 10) 
            self.idf_dict[word] = idf_value 
        
        self.idf.append(self.idf_dict)
        df_idf = pd.DataFrame(self.idf)
        df_idf.to_csv('./tables/df_idf_table.csv', sep=',', index=True, encoding='utf-8')
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
        df_tf_idf.index = self.random_reviews
        print("TF-IDF: \n", df_tf_idf)
        return df_tf_idf
    
    def tf_idf_normalized_function(self, df_tf_idf):
        norm = np.linalg.norm(df_tf_idf.values,axis=1)
        self.tf_idf_norm = (df_tf_idf.T/norm).T
        self.tf_idf_norm.index = self.random_reviews
        self.tf_idf_norm.to_csv('./tables/tf_idf_norm_table.csv', sep=',', index=True, encoding='utf-8')
        print("NORM: \n", self.tf_idf_norm)
        return self.tf_idf_norm

    def tf_idf_query_normalized_function(self, query):
        
        query_vector = self.tf_idf_norm.T.iloc[:,0].copy(deep=True)
        
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

        # print (norm_query_vector)
        return norm_query_vector


    def cosine_similarity(self, document_vector):
        dot_product = self.tf_idf_norm.dot(document_vector)
        # print(dot_product)
        return dot_product
        # cosine_sim_matrix = cosine_similarity(self.tf_idf_norm, document_vector)
        # print(cosine_sim_matrix)
        # return cosine_sim_matrix
    
    def top_ten_recommendations(self, cosine_similarity_vector):
        top_ten_vector = cosine_similarity_vector.sort_values(ascending=False)
        top_ten_vector = top_ten_vector[:10]
        print(top_ten_vector)
        return top_ten_vector


    def run(self):

        self.preprocess()
        tf = self.tf_function(self.tf)
        df = self.df_function(tf)
        top_ten = self.top_ten_reviews(df)
        idf = self.idf_function(df)
        tf_idf = self.tf_idf_function(tf, idf)
        tf_idf_normalized = self.tf_idf_normalized_function(tf_idf)
        
        #------------------------------ Matrix
        similarity_matrix = self.cosine_similarity(tf_idf_normalized.T)
        plt.matshow(similarity_matrix)
        plt.set_cmap('Blues')
        plt.colorbar()
        plt.show()
        
        
        #------------------------------ Query
        while True:
            print("\n Write your query to search for a movie: ")
            raw_query = input()
            query = self.tf_idf_query_normalized_function(raw_query)
            cosine_similarity_vector = self.cosine_similarity(query)
            self.top_ten_recommendations(cosine_similarity_vector)
        



    
    
