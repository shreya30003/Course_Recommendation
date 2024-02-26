import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from IPython.display import display

df = pd.read_excel(r'Dataset.xlsx')

df.drop('What is your name?', axis=1, inplace=True)
df.drop('What is your gender?', axis=1, inplace=True)
df.drop('What was your course in UG?', axis=1, inplace=True)
df.drop('What was the average CGPA or Percentage obtained in under graduation?', axis=1, inplace=True)

df.rename(columns={df.columns[0]: 'UG_Course', df.columns[1]: 'Interests', df.columns[2]: 'Skills',
                   df.columns[3]: 'Certifications', df.columns[4]: 'Certification_Name',
                   df.columns[5]: 'Working', df.columns[6]: 'Job_Title', df.columns[7]: 'Masters'},
          inplace=True)

df["Skills"] = df["Skills"].astype(str)

def recommend_course(d):
    global df
    d = pd.DataFrame([d])
    df = pd.concat([df, d], axis=0, ignore_index=True)
    
    df['Interests'] = df['Interests'].astype(str)
    df['Skills'] = df['Skills'].astype(str)
    df['Factors'] = df[['Interests', 'Skills']].apply("-".join, axis=1)
    
    for i in range(len(df)):
        has_certification = str(df.Certifications[i])
        certification_name = str(df.Certification_Name[i])
        if has_certification.startswith('Y') == True:
            df.loc[i, 'Factors'] = df.loc[i, 'Factors'] + '-' + certification_name
        i = i + 1

    for i in range(len(df)):
        is_working = str(df.Working[i])
        job_title = str(df.Job_Title[i])
        if is_working.startswith('Y') == True:
            df.loc[i, 'Factors'] = df.loc[i, 'Factors'] + '-' + job_title
        i = i + 1

    for i in range(len(df)):
        pursuing_masters = str(df.Masters[i])
        if pursuing_masters.startswith('N') == True:
            continue
        else:
            df.loc[i, 'Factors'] = df.loc[i, 'Factors'] + '-' + pursuing_masters
        i = i + 1

    df_f = df.Factors
    df_f.replace("[^a-zA-Z]", " ", regex=True, inplace=True)
    df_f = df_f.to_frame()
    df_f.columns = ['Factors']

    tf_idf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tf_idf.fit_transform(df_f["Factors"])
    tf_idf_matrix_df = pd.DataFrame.sparse.from_spmatrix(tfidf_matrix)
    df_final = tf_idf_matrix_df

    y = df_final.iloc[:-1, :]

    similarity_matrix = cosine_similarity(df_final.iloc[[-1], :], y)
    similarity_matrix_df = pd.DataFrame(similarity_matrix)

    sim_scores = list(enumerate(similarity_matrix[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    similarity_idx, similarity_scores = [i[0] for i in sim_scores], [i[1] for i in sim_scores]

    recommended_courses = pd.DataFrame(columns=["UG_Course", "Score"])
    recommended_courses["UG_Course"] = df.loc[similarity_idx, "UG_Course"]

    recommended_courses["Score"] = similarity_scores

    recommended_courses = recommended_courses.loc[(recommended_courses.UG_Course != '')]
    recommended_courses = recommended_courses.drop_duplicates(subset='UG_Course', keep="first")

    course_recommendations = recommended_courses.iloc[0:5, :]
    course_recommendations.reset_index(inplace=True)
    course_recommendation = course_recommendations['UG_Course'].values.tolist()

    return course_recommendation