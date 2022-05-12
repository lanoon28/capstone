import pandas as pd
import warnings
import re
from konlpy.tag import Okt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import joblib
import time
from sklearn.feature_selection import RFE
start = time.time()

load_model = joblib.load('newDeep.pkl')

warnings.filterwarnings(action = 'ignore')

okt = Okt()

train_df = pd.read_excel('Comments.xlsx')

train_df = train_df[train_df['text'].notnull()]

train_df['text'] = train_df['text'].apply(lambda x : re.sub(r'[^ ㄱ-ㅣ가-힣]+', " ", x))

text = train_df['text']
score = train_df['score']

train_x, test_x, train_y, test_y = train_test_split(text, score , test_size=0.9, random_state=0)

tfv = TfidfVectorizer(tokenizer=okt.morphs, ngram_range=(1,2), min_df=3, max_df=0.9)
tfv.fit(train_x)
tfv_train_x = tfv.transform(train_x)

#joblib.dump(grid_cv,'./newDeep.pkl')

tfv_test_x = tfv.transform(test_x)
test_predict = load_model.best_estimator_.predict(tfv_test_x)


input_text = 'ㅅㅂ 이걸 왜 만드냐'

input_text = re.compile(r'[ㄱ-ㅣ가-힣]+').findall(input_text)
input_text = [" ".join(input_text)]

st_tfidf = tfv.transform(input_text)

st_predict = load_model.best_estimator_.predict(st_tfidf)

print('감성 분류 모델의 정확도 : ',round(accuracy_score(test_y, test_predict), 3))

if(st_predict == 0):
    print('예측 결과: ->> 부정 감성')
else :
    print('예측 결과: ->> 긍정 감성')

stop = time.time()
print(stop - start)