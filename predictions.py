import pandas as pd
from joblib import dump, load
from predictors_transformer import PredictorTransformer as pt

class SalaryPrediction:

    @staticmethod
    def getSalaryPrediction(payload):
        try:
            prediction_dataset = pd.DataFrame([payload])
            prediction_dataset = pt.transform_dataset(prediction_dataset)
            prediction_open = load('Models/tree_reg_model_v3.joblib')
            # prediction_open = load('Models/lin_reg_model_v2.joblib')
            payload_predict = prediction_open.predict(prediction_dataset)
            payload_predict = pd.DataFrame(payload_predict, columns=['prediccion'])
            payload_predict = payload_predict.to_json(orient='records')
            return payload_predict
        except Exception as e:
            return str(e)
