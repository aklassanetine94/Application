# Application
import pandas as pd 
import streamlit  as st
from sklearn.ensemble import RandomForestClassifier

from PIL import Image


####
from PIL import Image 
img1 = Image.open("Arriere_plan (1).jpg") 
img2 = Image.open("GUSTAVE EIFFEL.png") 

st.image(img2, width=400)
st.image(img1, width=400)


#####



#logo= Image.open("Arriere_plan (1).jpg")



tabase=pd.read_csv(r"C:/Users/Acer/Downloads/Maladies_cardiaques (1).csv")  

mabase = pd.read_csv(r"C:/Users/Acer/Downloads/Maladies_cardiaques (1).csv")

#st.image(logo,width=200,use_column_width=True) # attach de notre logo

st.write('''# Bienvenue dans l'APPLICATION 
## PREDICTION DE LA MALADIE DU COEUR ''')

st.sidebar.header("Les paramètres d'entrées")



#####
 
####


#
def user_input():# les données a saisir
    # age= st.sidebar.slider('Donner l Age du patient ')
    age = st.sidebar.number_input("Entrer l'âge du patient",25,100)
    while (not(age in range(25,100,1))):
        st.warning("Warning:Lâge doit etre comprise entre 25 et 99 ans")
        break

    sexee=st.sidebar.selectbox('Entrer  le sexe du patient',('Homme' , 'Femme'))
    if (sexee=='Homme'):
        sexe=1
    else:
        sexe=0
        
    chestPaintypee=st.sidebar.selectbox('Entrer le type de douleur thoracique',('TA : angine typique', 'ATA : angine atypique', 'NAP : douleur non angineuse', 'ASY : asymptomatique'))
    if (chestPaintypee=='TA : angine typique'):
        chestPaintype=0
        
    if (chestPaintypee=='TA : angine atypique'):
        chestPaintype=1
        
    if (chestPaintypee=='NAP : douleur non angineuse'):
        chestPaintype=2
    else:
        chestPaintype=3
        
        
    restingBP=st.sidebar.number_input('Entrer la pression artérielle au repos  en mm Hg ',90.0,190.1)
    cholesterol=st.sidebar.number_input('Entrer le taux cholestérol sérique en mm/dl',60.0,410.9)

    
    fastingBSS=st.sidebar.selectbox('Entrer le taux de glycémie à jeun',( 'Superieur à 120 mg/dl', 'Inférieur à 120 mg/dl'))
    if (fastingBSS=='Superieur à 120 mg/dl'):
        fastingBS=1
     # Votre valeur de glucose de 120 mg / dL est trop élevée. Un bon glucose se situe généralement entre 65 et 99 mg / dL.
    else:
        fastingBS=0
        

    restingECGG=st.sidebar.selectbox("Entrer les résultats de l'électrocardiogramme au repos",(
                                    'Normal',
                                    "Anomalie de l'onde ST-T",
                                    'Hypertrophie ventriculaire gauche'
                                    ))
    
    if (restingECGG=='Normal'):
        restingECG=0
    if (restingECGG=="Anomalie de l'onde ST-T"):
        restingECG=1
    else:
        restingECG=2


    MaxHR=st.sidebar.number_input('Entrer la fréquence cardiaque maximale atteinte',60.1, 202.1)


    exercicese_anginaa=st.sidebar.selectbox("Entrer la douleur induite par l'exercice physique du patient",('Absence de douleur' ,'presence de douleur'))
    if (exercicese_anginaa=='Absence de douleur'):
        exercicese_angina=1
    else:
        exercicese_angina=0
        
        
    oldpeak=st.sidebar.number_input('Entrer la valeur numérique de la dépression ECG',-3.1,4.1)

    ST_slopee=st.sidebar.selectbox("Entrer la pente du segment ST d'exercice de pointe",('segment ascendant' ,'segment plat' ,'segment descendant '))
    
    if (ST_slopee=='segment ascendant'):
        ST_slope=0
    if (ST_slopee=='segment plat'):
        ST_slope=1
    else:
        ST_slope =2
    
    data={'age':age ,
          'sexe':sexe ,
          'chestPaintype':chestPaintype,
          'restingBP':restingBP ,
          'cholesterol':cholesterol ,
          'fastingBS':fastingBS ,
          'restingECG':restingECG,
          'MaxHR':MaxHR, 
          'exercicese_angina':exercicese_angina  ,
          'oldpeak':oldpeak ,
          'ST_slope':ST_slope }# Creation d'une dictionnaire qui vas contenir le nom des colonnes
    
    patient_parametre=pd.DataFrame(data, index=[0])# cresation dun tableau
    
    return  patient_parametre


dff=user_input()


 


# encodage de nos variable cathégorielle
def prep(tabase):
    code={'M':0 , 'F':1,
         'ATA':0, 'NAP':1 ,'ASY':2 ,'TA':3,
          'Normal':0, 'ST':1, 'LVH':2,
         'N':0 ,'Y':1,
         'Up':0 ,'Flat':1 ,'Down':3}
    for col in tabase.select_dtypes('object'):
        tabase[col]=tabase[col].map(code)
    #mabase=renome(mabase)    
    x=tabase.drop('HeartDisease',axis=1)
    y=tabase['HeartDisease']
    return x,y



from sklearn.model_selection import train_test_split 
# x_train, y_train=prep(trainset)
#x_test, y_test=prep(testset)

x,y=prep(tabase)


model= RandomForestClassifier()
from sklearn.linear_model import LogisticRegression

#model=LogisticRegression(random_state=0)
model.fit(x ,y)
import colorama
from colorama import Fore


ypred=model.predict(dff)

proba=model.predict_proba(dff)#prediction de la probabilité

#st.write("La probabilité pour que le patient soit malade est de: ")
#st.write(proba[0,1])
print(Fore.RED + 'This text is red in color')

if st.button("Predict"):
    resultat=proba[0,1]
    st.success("La probabilité pour que le patient soit atteint de la maladie du coeur est de {}".format(resultat))
    if resultat<  0.5:
        st.write(" Le patient n'est pas à risque")
    else:
        st.write("Le patient doit être pris en charge")
#commentaire sur l'application
st.markdown("Cette application utilise un modèle machine Learning déployée sur github dans le but d'aider le service soignant dans leur prise de décision." \
               "Elle donne la probabilité qu'un patient ait une insuffisance cardiaque (p>0.50) ou non (p<0.50).") 
