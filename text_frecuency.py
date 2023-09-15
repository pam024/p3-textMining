import os
import numpy as np 
import pandas as pd
import math

class TextMining:
    
    def __init__(self, path_files):        
        self.random_reviews = os.listdir(path_files)
    
    #funcion calculos
    def calculations(self):
        tf = []
        df = []
        idf = []
        tf_idf_list = []
        
        for i in self.random_reviews:
            with open ("./output/"+i, 'rt', encoding='utf-8')  as file:
                
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
                    
                tf.append(word_counts)
        
        #print top 10 words from all reviews    
        dt_tf = pd.DataFrame(tf)
        dt_tf = dt_tf.fillna(0)
        
        dict_tf = dict(dt_tf)
        #print("TF: \n", dt_tf)
        
        doc_set = set(dt_tf.columns)
     
        word_df = {word: 0 for word in doc_set}     
        for i in tf: 
            for j in doc_set:
                if j in i:
                    word_df[j] += 1

        aux = sorted(word_df.items(), key=lambda item:item[1])
        aux.reverse()
        
        #df
        sorted_dict = dict(aux)                      
        #print("DF: \n", sorted_dict) 
        
        #idf
        idf_dict = {}
        
        for word, value in sorted_dict.items():
            idf_value = math.log(len(self.random_reviews)/value) #logaritmo natural
            idf_dict[word] = idf_value 
        
        idf.append(idf_dict)
        df_idf = pd.DataFrame(idf)        
        #print("IDF: \n", df_idf)

        #tf_idf 
        lista = dt_tf.to_dict(orient='records')
        
        for i in lista:
            tf_idf = {}
            for key,value in i.items():
                tf_idf[key] = i[key]*idf_dict[key]
            
            tf_idf_list.append(tf_idf)
        
        df_tf_idf = pd.DataFrame(tf_idf_list)
        print("TF-IDF: \n", df_tf_idf)
        
        #Normalize TF-IDF
        norm = np.linalg.norm(df_tf_idf.values,axis=1)
        tf_idf_norm = (df_tf_idf.T/norm).T
            
        print("NORM: \n", tf_idf_norm)
        #df.iloc[fila_index].sum()
            #normalized_df_tf_idf = dt_tf_idf
        
        
        
        #("TF-IDF Normalize: \n", normalized_df_tf_idf)
        
    
if __name__ == '__main__':
    t = TextMining("./output") 
    
    t.calculations()
