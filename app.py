import pandas as pd 
import streamlit as st 
import pulp 
from pulp import * 

st.header("Can You Beat the KFC Unlimited Buffet?")
st.image('/Users/kelvinfoo/Desktop/Side Projects/KFC-Flatlay-poster-jpg.webp')
st.text('This app calculates the optimal amount of each food item that you need to consume at')
st.text('the KFC unlimited buffet in order to make your money worth.')
st.text('However, there is an extra condition: to not exceed the recommended daily')
st.text('calories intake.')

st.subheader('What is your threshold?')
st.text('Select how much of each food item you are willing to consume.')

cols = st.columns(2)
with cols[0]: 
    y1 = st.slider('How many original recipe chicken do you want to consume?', 
                   0, 30, (3, 7))
with cols[1]: 
    y2 = st.slider('How many hot and crispy chicken do you want to consume?', 
                   0, 30, (3, 7))

cols = st.columns(2)
with cols[0]: 
    y3 = st.slider('How many tender do you want to consume?', 
                   0, 30, (3, 6))
with cols[1]: 
    y4 = st.slider('How many popcorn chicken do you want to consume?', 
                   0, 30, (1, 2))
    
cols = st.columns(2)
with cols[0]: 
    y5 = st.slider('How many whipped potato do you want to consume?', 
                   0, 30, (1, 3))
with cols[1]: 
    y6 = st.slider('How many coleslaw do you want to consume?', 
                   0, 30, (1, 3))

y7 = st.slider('How many portugese egg tart do you want to consume?', 
               0, 30, (2, 5))

cols = st.columns(2)
with cols[0]: 
    y8 = st.slider('How many cups of coke (original taste less sugar) do you want to consume?', 
                   0, 10, (1, 3))
with cols[1]: 
    y9 = st.slider('How many cups of Heaven & Earth ice lemon tea do you want to drink?', 
                   0, 10, (1, 3))

cols = st.columns(2)
with cols[0]: 
    y10 = st.slider('How many cups of sprite do you want to drink?', 
                   0, 10, (1, 3))
with cols[1]: 
    y11 = st.slider('How many cups of Fanta Grape do you want to drink?', 
                   0, 10, (1, 3))

st.subheader('Assumptions made')
st.text('New items are not included in the calculation (eg. Carrot cake).')
st.text('The calorie and sodium intake for chicken is based on that for chicken thigh.')
st.text('Bundle deals were not considered (eg. 3 piece chicken meal).')

st.subheader('Your recommended food intake at the KFC Unlimited Buffet')

# Linear Programming 
prob = LpProblem('KFC Buffet', LpMaximize)
x1 = LpVariable('Original Chicken', y1[0], y2[0])
x2 = LpVariable('Crispy Chicken', y2[0], y2[1])
x3 = LpVariable('Tender', y3[0], y3[1])
x4 = LpVariable('Popcorn Chicken', y4[0], y4[1])
x5 = LpVariable('Whipped Potato', y5[0], y5[1])
x6 = LpVariable('Coleslaw', y6[0], y6[1])
x7 = LpVariable('Egg Tart', y7[0], y7[1])
x8 = LpVariable('Coke', y8[0], y8[1])
x9 = LpVariable('Lemon Tea', y9[0], y9[1])
x10 = LpVariable('Sprite', y10[0], y10[1])
x11 = LpVariable('Fanta Grape', y11[0], y11[1])

prob += 4.35 * x1 + 4.35 * x2 + (6.35/3) * x3 + 5.60 * x4 + 4.35 * x5 + 3.15 * x6 + 2 * x7 + 3.30 * (x8 + x10 + x11) + 3.30 * x9 
prob += 329 * x1 + 399 * x2 + 119 * x3 + 446 * x4 + 51 * x5 + 98 * x6 + 166 * x7 + 105 * x8 + 67 * x11 + 105 * x9 + 67 * x10 <= 2200 
prob += 4.35 * x1 + 4.35 * x2 + (6.35/3) * x3 + 5.60 * x4 + 4.35 * x5 + 3.15 * x6 + 2 * x7 + 3.30 * (x8 + x10 + x11) + 3.30 * x9 >= 23.95


prob.solve()
if LpStatus[prob.status] == 'Infeasible': 
    st.write('Do not waste your money. The buffet is not worth it for you!')

else: 
    data = []
    for v in prob.variables():
        data.append([v.name, round(v.varValue, 0)])
    df = pd.DataFrame(data, columns=['Food Item', 'Quantity'])
    st.write(df)
    st.write("Total cost of all food items consumed = ", round(value(prob.objective),2))







