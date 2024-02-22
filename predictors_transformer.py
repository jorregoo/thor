from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
# from pickle import dump
# from pickle import load
from joblib import dump, load

class PredictorTransformer:
    def set_fit_full_pipeline(dataset, num_attribs_list, cat_attribs_list) :
        num_pipeline_total = Pipeline([
            ('imputer', SimpleImputer(strategy="median")),
            # ('std_scaler', StandardScaler()), #Feature scaling
        ])

        num_attribs = num_attribs_list
        cat_attribs = cat_attribs_list

        full_pipeline = ColumnTransformer([
                ("num", num_pipeline_total, num_attribs),
                ("cat", OneHotEncoder(), cat_attribs),
            ])
        
        dataset_prepared = full_pipeline.fit(dataset)
        # dump(dataset_prepared, open('dataset_prepared.pkl', 'wb')
        dump(dataset_prepared, 'dataset_prepared.joblib') 
        return dataset_prepared
    
    def transform_dataset(dataset):
        try:
            # load the scaler
            # full_ppl = load(open('dataset_prepared.pkl', 'rb'))
            full_ppl = load('dataset_prepared_v2.joblib')
            new_dataset = full_ppl.transform(dataset)
            return new_dataset
        except Exception as e:
            return e