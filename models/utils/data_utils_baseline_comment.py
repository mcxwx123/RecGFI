import pandas as pd

def unfold(df,s):
    df=df[s].values
    lst=[]
    for i in df:
        dic={}
        for j in range(len(i)):
            dic[j]=i[j]
        lst.append(dic)

    return pd.DataFrame(lst)


def load_raw_data(file_path,vectorizer,dataset_index):
    if dataset_index==2:
        df = pd.read_pickle(file_path)
       
        comment_text=pd.DataFrame(vectorizer.get_text_feature( df['comment'].values))

       

        comnum=df[["commentnum","labels"]]
        

        T=pd.concat([comment_text,comnum],axis=1)
        c=[]
        for i in range(comment_text.shape[1]):
            c.append("com"+str(i))
        c+=list(comnum.columns)
        T.columns=c

    return T



def load_train_test_data(file_path1,vectorizer,dataset_index,fold,sorted,crosspro):

    T= load_raw_data(file_path1,vectorizer,dataset_index)
    T.dropna(inplace=True)
    p_train_split1=int((fold/10)*T.shape[0])
    p_train_split2=int((fold/10+0.1)*T.shape[0])


    train_data1=T.iloc[:p_train_split1]
    train_data2=T.iloc[p_train_split2:]
    train_data=pd.concat([train_data1,train_data2],axis=0)

    test_data=T.iloc[p_train_split1:p_train_split2]

    p_train = train_data[train_data.labels == 1]
    p_train = p_train.sample(frac=15000/p_train.shape[0],replace=True,random_state=0)

    n_train = train_data[train_data.labels == 0]
    n_train=n_train.sample(frac=15000/n_train.shape[0],replace=True,random_state=0)

    train_data=pd.concat([p_train,n_train],ignore_index=True)
    train_data=train_data.sample(frac=1, random_state=0)



    y_train=train_data['labels']
    y_test=test_data['labels']

    del train_data['labels']
    del test_data['labels']
    X_train=train_data
    X_test=test_data

    return X_train, X_test, y_train, y_test




