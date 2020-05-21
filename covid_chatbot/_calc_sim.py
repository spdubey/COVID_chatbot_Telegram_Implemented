from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
from _nlp_ops import *
import os


def create_data(query = '') :
    data_path = os.getcwd()
    data_path = data_path + '\\data\\'
    data_text = pd.read_excel(data_path + 'FAQ.xlsx')
    data_fig = pd.read_excel(data_path +'Data.xlsx')
    data_query = pd.DataFrame({'Question' : [query], 'Answer' : [None]})
    return data_text, data_fig, data_query

def cleaning_text_data(data, col):
    data[col] = data[col].map(lambda row : replace_word_contractions(row))
    data[col] = data[col].map(lambda row : remove_non_alphabet(row))
    data[col] = data[col].map(lambda row : remove_URLs(row))
    data[col] = data[col].map(lambda row : remove_digits(row))
    data[col] = data[col].map(lambda row : remove_stop_words(row))
    data[col] = data[col].map(lambda row : porter_stemmer(row))
    data[col] = data[col].map(lambda row : wordnet_lemmatizer(row))
    return data

def cleaning_fig_data(data, col):
    data[col] = data[col].map(lambda row : row.lower())
    data[col] = data[col].map(lambda row : row.replace('#', ' '))
    return data

def feature_extraction(data, col):
    tf_vect = TfidfVectorizer(lowercase=True,stop_words='english')
    tf_matrix = tf_vect.fit_transform(data[col])
    tf_names = tf_vect.get_feature_names()
    X_tf_vect = pd.DataFrame(tf_matrix.toarray(), columns=tf_names)
    return X_tf_vect, tf_names

def calc_similarity(X_tf_vect):
    similarity_score = []
    target = X_tf_vect.iloc[X_tf_vect.index.stop - 1].values.tolist()
    for i in range(0, len(X_tf_vect)):
        candidate = X_tf_vect.iloc[i].values.tolist()
        similarity_score.append(cosine_similarity([target], [candidate])[0][0])
    X_tf_vect['sim_score'] = similarity_score
    return X_tf_vect

def greeting_check(text):
    text = text.lower()
    text = ''.join(sorted(set(text), key=text.index))
    if np.any([True for each in ['hey', 'hi', 'hello', '/start', 'how are you'] if text.lower() in each]):
        ans = """Hello!! I am a new bot, still learning about corona virus information. I can help answer frequently asked questions about COVID -19 and about it's count in India state or city wise. Not sure what to ask? Try, How does COVID spread?' or 'Count in Odisha' 
                """
        return ans
    elif np.any([True for each in ['bye', 'bye bye', 'thankyou', 'thank you','by'] if text.lower() in each]):
        ans = """Bye Bye!!"""
        return ans
        
    return False


def get_bot_reply(query):
    #query = input()
    #query = 'what is the death in chhattisgarh'
    #print("Inside the get_bot_reply, and the question is {}".format(query))
    text_data, fig_data, query_data = create_data(query)
    cleaned_text_data= cleaning_text_data(text_data, col ='Question')
    cleaned_query_data = cleaning_text_data(query_data, col ='Question')
    cleaned_fig_data = cleaning_fig_data(fig_data, col ='Question')
    data_total = pd.concat([cleaned_text_data, cleaned_fig_data, cleaned_query_data]).reset_index(drop = True)

    # feature exactraction
    X_tf_vect, tf_names = feature_extraction(data_total, col = 'Question')
    X_tf_vect = calc_similarity(X_tf_vect)
    data_total_with_sim = pd.concat([data_total, X_tf_vect['sim_score']], axis = 1)
    ans = data_total.loc[data_total_with_sim.sim_score[: len(data_total) -1].idxmax()][1]
    #print(ans)
    return ans
    #print("\n")
    #print("Any thing else??!!")
    #print("press 'y' to continue")  