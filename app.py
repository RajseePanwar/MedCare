import joblib
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import pandas as pd
import pickle
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

#file_path = 'testcases\diabetes-prediction-rfc-model.pkl'
#with open(file_path, 'rb') as file:
    # Load the object from the file
#    classifier = pickle.load(file)

file_path_diabetes = ('testcases\diabetes_model.sav')
classifier = pickle.load(open(file_path_diabetes, 'rb'))
file_path_cancer = ('testcases\cancer.pkl')
model = pickle.load(open(file_path_cancer, 'rb'))
#model1 = pickle.load(open('model1.pkl', 'rb'))

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# bootstrap = Bootstrap(app)
# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'


# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(15), unique=True)
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(80))


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
#     password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
#     remember = BooleanField('remember me')


# class RegisterForm(FlaskForm):
#     email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
#     username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
#     password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/help')
def help():
    return render_template("help.html")


@app.route('/terms')
def terms():
    return render_template("tc.html")


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             if check_password_hash(user.password, form.password.data):
#                 login_user(user, remember=form.remember.data)
#                 return redirect(url_for('dashboard'))

#         return render_template("login.html", form=form)
#     return render_template("login.html", form=form)


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         hashed_password = generate_password_hash(form.password.data, method='sha')
#         new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()

#         return redirect("/login")
#     return render_template('signup.html', form=form)


@app.route("/dashboard")

def dashboard():
    return render_template("dashboard.html")


@app.route("/disindex")

def disindex():
    return render_template("disindex.html")


@app.route("/cancer")

def cancer():
    return render_template("cancer.html")


@app.route("/diabetes")

def diabetes():
    return render_template("diabetes.html")


@app.route("/heart")

def heart():
    return render_template("heart.html")


@app.route("/kidney")

def kidney():
    return render_template("kidney.html")

def Value(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==13):
        loaded_model = joblib.load('heart_disease_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/predictkidney', methods=["POST"])
def predictkidney():
    result=0
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        if len(to_predict_list) == 13:
            result = Value(to_predict_list, 13)

    if int(result) == 1:
        prediction = "Patient has a high risk of Kidney Disease, please consult your doctor immediately"
    else:
        prediction = "Patient has a low risk of Kidney Disease"
    return render_template("kidney_result.html", prediction_text=prediction)


@app.route("/parkinson")

def parkinson():
    return render_template("parkinson.html")


def ValuePred(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==22):
        loaded_model = joblib.load('parkinsons_model.sav')
        result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/predictpar', methods=["POST"])
def predictpar():
    result=0
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        if len(to_predict_list) == 22:
            result = ValuePred(to_predict_list, 22)

    if int(result) == 1:
        prediction = "Patient has a high risk of Liver Disease, please consult your doctor immediately"
    else:
        prediction = "Patient has a low risk of Kidney Disease"
    return render_template("parkinson_result.html", prediction_text=prediction)


# @app.route('/logout')

# def logout():
#     logout_user()
#     return redirect(url_for('index'))


@app.route('/predict', methods=['POST'])
def predict():
    input_features = [int(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    features_name = ['clump_thickness', 'uniform_cell_size', 'uniform_cell_shape', 'marginal_adhesion',
                     'single_epithelial_size', 'bare_nuclei', 'bland_chromatin', 'normal_nucleoli', 'mitoses']
    df = pd.DataFrame(features_value, columns=features_name)
    output = model.predict(df)
    if output == 4:
        res_val = "a high risk of Breast Cancer"
    else:
        res_val = "a low risk of Breast Cancer"

    return render_template('cancer_result.html', prediction_text='Patient has {}'.format(res_val))


##################################################################################

df1 = pd.read_csv('testcases\diabetes.csv')

# Renaming DiabetesPedigreeFunction as DPF
df1 = df1.rename(columns={'DiabetesPedigreeFunction': 'DPF'})

# Replacing the 0 values from ['Glucose','BloodPressure','SkinThickness','Insulin','BMI'] by NaN
df_copy = df1.copy(deep=True)
df_copy[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']] = df_copy[['Glucose', 'BloodPressure',
                                                                                    'SkinThickness', 'Insulin',
                                                                                    'BMI']].replace(0, np.NaN)

# Replacing NaN value by mean, median depending upon distribution
df_copy['Glucose'].fillna(df_copy['Glucose'].mean(), inplace=True)
df_copy['BloodPressure'].fillna(df_copy['BloodPressure'].mean(), inplace=True)
df_copy['SkinThickness'].fillna(df_copy['SkinThickness'].median(), inplace=True)
df_copy['Insulin'].fillna(df_copy['Insulin'].median(), inplace=True)
df_copy['BMI'].fillna(df_copy['BMI'].median(), inplace=True)

# Model Building

X = df1.drop(columns='Outcome')
y = df1['Outcome']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

# Creating Random Forest Model

classifier = RandomForestClassifier(n_estimators=20)
classifier.fit(X_train, y_train)

# Creating a pickle file for the classifier
# filename = 'diabetes-prediction-rfc-model.pkl'
# pickle.dump(classifier, open(filename, 'wb'))

#####################################################################


@app.route('/predictt', methods=['POST'])
def predictt():
    if request.method == 'POST':
        preg = request.form['pregnancies']
        glucose = request.form['glucose']
        bp = request.form['bloodpressure']
        st = request.form['skinthickness']
        insulin = request.form['insulin']
        bmi = request.form['bmi']
        dpf = request.form['dpf']
        age = request.form['age']

        data = np.array([[preg, glucose, bp, st, insulin, bmi, dpf, age]])
        my_prediction = classifier.predict(data)

        return render_template('diab_result.html', prediction=my_prediction)


############################################################################################################

# @app.route('/predictheart', methods=['POST'])
# def predictheart():
#     input_features = [float(x) for x in request.form.values()]
#     features_value = [np.array(input_features)]

#     features_name = ["age", "sex", "cp", "trestbps", "chol", "fbs",
#                      "restecg", "thalach", "exang", "oldpeak", "slope", "ca",
#                      "thal"]
#     model = joblib.load('heart_disease_model.pkl')
#     df = pd.DataFrame(, columns=features_name)
#     output = model.predict(df)

#     if output == 1:
#         res_val = "a high risk of Heart Disease"
#     else:
#         res_val = "a low risk of Heart Disease"

#     return render_template('heart_result.html', prediction_text='Patient has {}'.format(res_val))


@app.route("/hearts")

def hearts():
    return render_template("heart.html")


def Value(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==13):
        loaded_model = joblib.load('heart_disease_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/predictheart', methods=["POST"])
def predictheart():
    result=0
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        if len(to_predict_list) == 13:
            result = Value(to_predict_list, 13)

    if int(result) == 1:
        prediction = "Patient has a high risk of Heart Disease, please consult your doctor immediately"
    else:
        prediction = "Patient has a low risk of Heart Disease"
    return render_template("heart_result.html", prediction_text=prediction)


############################################################################################################

if __name__ == "__main__":
    app.run(debug=True)

