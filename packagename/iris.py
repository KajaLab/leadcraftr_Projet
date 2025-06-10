import pickle

def my_prediction_function(sepal_length, sepal_width, petal_length, petal_width):
    with open('models/best_model.pkl', 'rb') as file:
        model = pickle.load(file)
    prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
    return prediction.tolist()  # pour le rendre JSON serializable plus tard
