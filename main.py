from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import objectid
import numpy as np
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
app=Flask(__name__)
uri="mongodb+srv://Shreyas:Shreyas123@skillswapcluster.mqgvhg8.mongodb.net/?retryWrites=true&w=majority&appName=skillswapcluster"
client = MongoClient(uri)
db = client['SkillSwap']
collection = db['User']




        
@app.route("/",methods=['GET', 'POST'])  
def shreyas():
    if request.method == 'POST':
        data = request.get_json()
        idvalue=data.get("id")
        products=pd.read_csv('Skills.csv', encoding='latin-1')
        #converting the data into the strings
        products["Learn"]=products["Learn"].astype(str)
        products["Teach_Category"]=products["Teach_Category"].astype(str)
        products["Learn_Category"]=products["Learn_Category"].astype(str)
        products["Learn_Sub_Category"]=products["Learn_Sub_Category"].astype(str)
        products["Teach_Subcategory"]=products["Teach_Subcategory"].astype(str)
        products["Teach "]=products["Teach "].astype(str)
      #converting the data into the list 
        products["Learn_Sub_Category"]=products["Learn_Sub_Category"].apply(lambda x: x.split())
        products["Learn"]=products["Learn"].apply(lambda x: x.split())
        products["Learn_Category"]=products["Learn_Category"].apply(lambda x: x.split())
        products["Teach "]=products["Teach "].apply(lambda x: x.split())
        products["Teach_Category"]=products["Teach_Category"].apply(lambda x: x.split())
        products["Teach_Subcategory"]=products["Teach_Subcategory"].apply(lambda x: x.split())
        #creating the new columns after merging two three columns of the table
        products["LearnSkill"]=products["Learn"]+products["Learn_Category"]+products["Learn_Sub_Category"]
        products['TeachSkill']=products['Teach ']+products['Teach_Category']+products['Teach_Subcategory']
        #creating a new table called Table which will store only id,teachskill,learnskill and skills

        Table=products[['ID','TeachSkill','LearnSkill','Learn','Teach ']]

        #joining the table and converting the list into the string
        Table["Teach "]=Table["Teach "].apply(lambda x:" ".join(x))
        Table["Learn"]=Table["Learn"].apply(lambda x:" ".join(x))
        Table["TeachSkill"]=Table["TeachSkill"].apply(lambda x:" ".join(x))
        Table["LearnSkill"]=Table["LearnSkill"].apply(lambda x:" ".join(x))

        #converting the two columns which we are comparing with are converting in lower case 
        Table["TeachSkill"]=Table["TeachSkill"].apply(lambda x:x.lower())
        Table["LearnSkill"]=Table["LearnSkill"].apply(lambda x:x.lower())

        #import the skit library for the cosine similarity
        from sklearn.feature_extraction.text import CountVectorizer
        cv=CountVectorizer(max_features=5000,stop_words='english')
        combined_text = pd.concat([Table["LearnSkill"], Table["TeachSkill"]])
        cv.fit(combined_text)
         
        # Transform each column using the same fitted vectorizer
        Learnvector = cv.transform(Table["LearnSkill"]).toarray()
        Teachvector = cv.transform(Table["TeachSkill"]).toarray()

        from sklearn.metrics.pairwise import cosine_similarity
        similarity=cosine_similarity(Learnvector,Teachvector)
        print(Table["LearnSkill"])
        print(Table["TeachSkill"])

        # Create skills dictionary
        
        my_dict = {}

        # Store similarity scores for each ID
        for i in range(0,15):
            my_dict[Table.loc[i]["ID"]] = similarity[i].tolist()

        # Create tuples of (ID, similarity_score)
        for key in my_dict:
            my_dict[key] = list(zip(Table["ID"].tolist(), my_dict[key]))

        #print(my_dict)    

        # Define recommendation function
        def recommended(movieID):
            listofskills=[]
            distances = sorted(my_dict[movieID], reverse=True, key=lambda x: x[1])
            #print(distances)
            for i in distances[0:5]:
                lists = Table.loc[Table['ID'] == i[0], 'Teach '].values
                print(lists[0])
                listofskills.append(lists[0])
            return listofskills

        #print(recommended(1))
        #print()
        return jsonify({'list of Recommeded teaching Skills': recommended(idvalue)})
    #user get request 
    elif request.method == 'GET':
        datas=[]
        data=list(collection.find())
        for i in data:
            i['_id'] = str(i['_id'])  # convert ObjectId to string
            datas.append(i)
        return jsonify({"user found":datas})
        
    else:
        return "Unsupported request method", 405

@app.route("/data",methods=['GET', 'POST'])
def data():
    print("hello")
    if request.method == 'GET':
        datas=[]
        data=list(collection.find())
        for i in data:
            i['_id'] = str(i['_id'])
            datas.append(i)
        fieldnames = set()
        for doc in datas:
            fieldnames.update(doc.keys())
        fieldnames = list(fieldnames)
        with open('mongo_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(datas)
        products=pd.read_csv('mongo_data.csv', encoding='latin-1')
        #Here the operation of the csv file starts
        print(products)
        #converting the data into the strings
        products["learnSkillcategory"]=products["learnSkillcategory"].astype(str)
        products["learnSkill"]=products["learnSkill"].astype(str)
        products["learnSkillsubcategory"]=products["learnSkillsubcategory"].astype(str)
        products["teachSkillsubcategory"]=products["teachSkillsubcategory"].astype(str)
        products["teachSkillcategory"]=products["teachSkillcategory"].astype(str)
        products["teachSkill"]=products["teachSkill"].astype(str)

        #converting the data into the list
        products["learnSkillcategory"]=products["learnSkillcategory"].apply(lambda x: x.split())
        products["learnSkill"]=products["learnSkill"].apply(lambda x: x.split())
        products["learnSkillsubcategory"]=products["learnSkillsubcategory"].apply(lambda x: x.split())
        products["teachSkillsubcategory"]=products["teachSkillsubcategory"].apply(lambda x: x.split())
        products["teachSkillcategory"]=products["teachSkillcategory"].apply(lambda x: x.split())
        products["teachSkill"]=products["teachSkill"].apply(lambda x: x.split())

        print(products)

        #creating the new columns after merging two three columns of the table
        products["LearnSkill"]=products["learnSkill"]+products["learnSkillcategory"]+products["learnSkillsubcategory"]
        products['TeachSkill']=products['teachSkill']+products['teachSkillcategory']+products['teachSkillsubcategory']
        print(products["LearnSkill"])


        #removing the space from the words
        def remove_space(word):
            l=[]
            for i in word:
                l.append(i.replace("",""))
            return l
        products["LearnSkill"]=products["LearnSkill"].apply(lambda x:remove_space(x))
        products['TeachSkill']=products['TeachSkill'].apply(lambda x:remove_space(x))
        print(products["LearnSkill"])

        #creating a new table called Table which will store only id,teachskill,learnskill and skills
        Table=products[['id','learnSkill','teachSkill','LearnSkill','TeachSkill']]
        print(Table)


        products["user"]=products["learnSkill"].apply(lambda x:" ".join(x))


        #converting the all the colummns into normal form 
        Table["teachSkill"]=Table["teachSkill"].apply(lambda x:" ".join(x))
        Table["learnSkill"]=Table["learnSkill"].apply(lambda x:" ".join(x))
        Table["TeachSkill"]=Table["TeachSkill"].apply(lambda x:" ".join(x))
        Table["LearnSkill"]=Table["LearnSkill"].apply(lambda x:" ".join(x))
        products["teachSkill"]=products["teachSkill"].apply(lambda x:" ".join(x))
        products["learnSkill"]=products["learnSkill"].apply(lambda x:" ".join(x))

        print(Table)

        #converting the two columns which we are comparing with are converting in lower case
        Table["TeachSkill"]=Table["TeachSkill"].apply(lambda x:x.lower())
        Table["LearnSkill"]=Table["LearnSkill"].apply(lambda x:x.lower())
        print(Table)


        #Now the Actual Similarity Operation Begins 

        #import the skit library for the cosine similarity
        from sklearn.feature_extraction.text import CountVectorizer
        cv=CountVectorizer(max_features=5000,stop_words='english')
        combined_text = pd.concat([Table["LearnSkill"], Table["TeachSkill"]])
        cv.fit(combined_text)

        # Transform each column using the same fitted vectorizer
        Learnvector = cv.transform(Table["LearnSkill"]).toarray()
        Teachvector = cv.transform(Table["TeachSkill"]).toarray()

        from sklearn.metrics.pairwise import cosine_similarity
        similarity=cosine_similarity(Learnvector,Teachvector)
        print(Table["LearnSkill"])
        print(Table["TeachSkill"])

        # Create skills dictionary
        
        my_dict = {}

        # Store similarity scores for each ID
        for i in range(0,len(data)):
            my_dict[Table.loc[i]["id"]] = similarity[i].tolist()

        # Create tuples of (ID, similarity_score)
        for key in my_dict:
            my_dict[key] = list(zip(Table["id"].tolist(), my_dict[key]))



        # Define recommendation function
        def recommendingskill(skillID):
            listofskills=[]
            distances = sorted(my_dict[skillID], reverse=True, key=lambda x: x[1])
            #print(distances)
            for i in distances[0:len(data)]:
                lists = products.loc[products['id'] == i[0], ['teachSkill','id','username','email']].values
                print(lists[0])
                listofskills.append(lists[0].tolist())
            print(listofskills[1][2])
            return listofskills

        return jsonify({"csv file created":recommendingskill(0)})
    
if __name__ == '__main__':
    app.run(debug=True, threaded=False)