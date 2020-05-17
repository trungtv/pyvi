from pyvi import ViTokenizer
import pickle
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV

tokenized_X_train = open('tokenized_X_train.pkl', 'rb') 
tokenized_X_test = open('tokenized_X_test.pkl', 'rb') 
tokenized_y_train = open('tokenized_y_train.pkl', 'rb')
tokenized_y_test = open('tokenized_y_test.pkl', 'rb') 

X_train = pickle.load(tokenized_X_train)                      
X_test = pickle.load(tokenized_X_test)

y_train = pickle.load(tokenized_y_train)
y_test = pickle.load(tokenized_y_test)
                      
tokenized_X_train.close() 
tokenized_X_test.close()
tokenized_y_train.close() 
tokenized_y_test.close() 

labels = ['B_W', 'I_W']
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    max_iterations=100,
    all_possible_transitions=True
)
params_space = {
    'c1': scipy.stats.expon(scale=0.5),
    'c2': scipy.stats.expon(scale=0.05),
}

# use the same metric for evaluation
f1_scorer = make_scorer(metrics.flat_f1_score,
                        average='weighted', labels=labels)

# search
rs = RandomizedSearchCV(crf, params_space,
                        cv=5,
                        verbose=1,
                        n_jobs=12,
                        n_iter=50,
                        scoring=f1_scorer)
rs.fit(X_train, y_train)

print('best params:', rs.best_params_)
print('best CV score:', rs.best_score_)
#print('model size: {:0.2f}M'.format(rs.best_estimator_.size_ / 1000000))
tokenizer_model = open('tokenizer_model.pkl', 'wb') 
pickle.dump(rs.best_estimator_, tokenizer_model, protocol=2)
tokenizer_model.close()

tokenizer_model_py3 = open('tokenizer_model_py3.pkl', 'wb') 
pickle.dump(rs.best_estimator_, tokenizer_model_py3)
tokenizer_model_py3.close()

