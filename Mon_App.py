# Application
import pandas as pd 
import streamlit  as st
from sklearn import datasets
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



tabase=pd.read_csv(r"C:\Users\Etudiant\Downloads\Maladies_cardiaques.csv")  

mabase = pd.read_csv(r"C:\Users\Etudiant\Downloads\Maladies_cardiaques.csv")

#st.image(logo,width=200,use_column_width=True) # attach de notre logo

st.write('''# Bienvenu dans l'APPLICATION 
## PREDICTION DE LA MALADIE DU COEUR ''')

st.sidebar.header("Les paramètres d'entrés")



#####
 
####


#
def user_input():# les données a saisir
    # age= st.sidebar.slider('Donner l Age du patient ')
    age = st.sidebar.number_input("Age du Patient",25,100)
    while (not(age in range(25,100,1))):
        st.warning("Warning:L'age doit etre comprise entre 25 et 99 ans")
        break

    sexee=st.sidebar.selectbox('Donner  le sexe du patient  en mettant O si cest une femme et 1 si cest un homme',('Homme' , 'Femme'))
    if (sexee=='Homme'):
        sexe=1
    else:
        sexe=0
        
    chestPaintypee=st.sidebar.selectbox('Donner le type de douleur thoracique',('TA : angine typique', 'ATA : angine atypique', 'NAP : douleur non angineuse', 'ASY : asymptomatique'))
    if (chestPaintypee=='TA : angine typique'):
        chestPaintype=0
        
    if (chestPaintypee=='TA : angine atypique'):
        chestPaintype=1
        
    if (chestPaintypee=='NAP : douleur non angineuse'):
        chestPaintype=2
    else:
        chestPaintype=3
        
        
    restingBP=st.sidebar.number_input('Donner la pression artérielle au repos  en mm Hg ',90.0,190.1)
    cholesterol=st.sidebar.number_input('Donner le taux cholestérol sérique en mm/dl du patient ',60.0,410.9)

    
    fastingBSS=st.sidebar.selectbox(' glycémie à jeun',( 'Taux de glycémie à jeun superieu a 120 mg/dl', 'Taux de glycémie à jeun inférieu a 120 mg/dl'))
    if (fastingBSS=='Taux de glycémie à jeun superieu a 120 mg/dl'):
        fastingBS=1
     # Votre valeur de glucose de 120 mg / dL est trop élevée. Un bon glucose se situe généralement entre 65 et 99 mg / dL.
    else:
        fastingBS=0
        

    restingECGG=st.sidebar.selectbox('Donner les résultats de l électrocardiogramme au repos ',(
                                    ' Normal',
                                    'présentant une anomalie de l onde ST-T',
                                    'montrant une hypertrophie ventriculaire gauche'
                                    ))
    
    if (restingECGG=='Normal'):
        restingECG=0
    if (restingECGG=='présentant une anomalie de l onde ST-T'):
        restingECG=1
    else:
        restingECG=2


    MaxHR=st.sidebar.number_input('Donner la fréquence cardiaque maximale atteinte Valeur numérique entre 60 et 202 ',60.1, 202.1)


    exercicese_anginaa=st.sidebar.selectbox('Donner la douleur induite par l exercice physique du patient ',('Absence de douleur' ,'presence de douleur'))
    if (exercicese_anginaa=='Absence de douleur'):
        exercicese_angina=1
    else:
        exercicese_angina=0
        
        
    oldpeak=st.sidebar.number_input('Donner Valeur numérique mesurée en dépression du patient ',-3.1,4.1)

    ST_slopee=st.sidebar.selectbox('Donner la pente du segment ST d exercice de pointe',('segment ascendant' ,'segment plat' ,'segment descendant '))
    
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
model.fit(x ,y)



ypred=model.predict(dff)

proba=model.predict_proba(dff)#prediction de la probabilité

st.write("La probabilité pour que le patient soit malade est de: ")
#st.write(proba[0,1])

if st.button("Predict"):
    resultat=proba[0,1]
    st.success("La probabilité pour que le patient soit atteint de la malidie du coeur est de {}".format(resultat))
    
#commentaire sur l'application
st.markdown("Cette application utilise un modèle Machine Learning déployé sur github dans le but d'aider les cardialogues dans leur travail." \
               "Elle prédit la probabilité pour qu'un patient soit positif (classe 1) ou non négatif  (classe 0 ) à la maladie du coeur.") 
