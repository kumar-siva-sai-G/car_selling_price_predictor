import pandas as pd
import numpy as np 
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import re
from datetime import datetime

current_year=datetime.now().year

df=pd.read_csv("quikr_car.csv")

df=df[df['Price'].str.contains('Ask')==False]
df=df.dropna()

df['Price']=df['Price'].str.replace(',','').astype(int)

df['kms_driven']=df['kms_driven'].apply(lambda x: re.sub(r'[^\d]','',str(x)))
df['kms_driven']=df['kms_driven'].replace('',np.nan).astype(int)

df=df.dropna(subset=['kms_driven'])

df['year']=pd.to_numeric(df['year'],errors='coerce')
df=df.dropna(subset=['year']) 
df['year']=df['year'].astype(int)

df['car_age']=current_year-df['year']

le_fuel=LabelEncoder()
le_company=LabelEncoder()
le_name=LabelEncoder()

df['fuel_type_enc']=le_fuel.fit_transform(df['fuel_type'])
df['company_enc']=le_company.fit_transform(df['company'])
df['name_enc']=le_name.fit_transform(df['name'])

X=df[['name_enc','car_age','fuel_type_enc','kms_driven','company_enc']]
y=df['Price']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

model=RandomForestRegressor()
model.fit(X_train,y_train)

def predict_price(name,bought_year,fuel,kms,company):
    car_age=current_year-bought_year
    input_data=pd.DataFrame([{
        'name_enc':le_name.transform([name])[0] if name in le_name.classes_ else 0,
        'car_age':car_age,
        'fuel_type_enc':le_fuel.transform([fuel])[0] if fuel in le_fuel.classes_ else 0,
        'kms_driven':kms,
        'company_enc':le_company.transform([company])[0] if company in le_company.classes_ else 0
    }])
    return int(model.predict(input_data)[0])
