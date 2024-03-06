from flask import Flask,render_template,request
import pickle
import numpy as np





popular_df1 = pickle.load(open('popular5.pkl', 'rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))
popular_df15 = pickle.load(open('popular15.pkl', 'rb'))
df1 = pickle.load(open('df1.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))
merged_df2=pickle.load(open('mergeddf2.pkl','rb'))





app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(merged_df2['Book-Title'].values),
                           description=list(merged_df2['Description'].values),

                           author=list(merged_df2['Book-Author'].values),
                           image=list(merged_df2['Image-URL-M'].values),
                           votes=list(merged_df2['num_of_rating'].values),
                           rating=list(merged_df2['avg_rating'].values),
                           price1=list(merged_df2['Price.'].values),
                           rating1=list(merged_df2['Ratings.'].values),
                           price2=list(merged_df2['Price..'].values),
                           rating2=list(merged_df2['Ratings..'].values)


                           )



@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')



@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))

        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)




if __name__=='__main__':
    app.run(debug=True)