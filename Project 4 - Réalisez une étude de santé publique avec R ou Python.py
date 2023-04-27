#!/usr/bin/env python
# coding: utf-8

# # Project 4 : Réalisez une étude de santé publique avec R ou Python

# ## 2 Objectifs
# 
# ### 1. Les questions de Marc entournant des information principales sur des donées de 2017
# ### 2. Les questions de Mélanie a besoin d'une étude un peu plus fine pour chacun des pays.

# ### Question 1 : La proportion de personnes en état de sous-nutrition 

# In[1]:


#importation des pandas librairies
import pandas as pd
pd.set_option("display.max_columns",None)


# In[2]:


#importation de fichier CSV

population = pd.read_csv('population.csv')
aide_alimentaire = pd.read_csv("aide_alimentaire.csv")
dispo_alimentaire = pd.read_csv("dispo_alimentaire.csv")
sous_nutrition = pd.read_csv("sous_nutrition.csv")

population


# In[3]:


#vérifier l'ensemble de données importées
population.info()


# In[4]:


population.head()


# In[5]:


population.describe()


# In[6]:


sous_nutrition


# In[7]:


sous_nutrition.info()


# In[8]:


#renommer les colonnes de deux data frames
sous_nutrition.rename(columns={"Valeur":"sous_nutrition"},inplace=True)
population.rename(columns={"Valeur":"population"},inplace=True)


# In[9]:


#vérifier pour des valeurs manquantes
population[population["population"].isna()]


# In[10]:


sous_nutrition


# In[11]:


sous_nutrition.dtypes


# In[12]:


sous_nutrition["sous_nutrition"]=pd.to_numeric(sous_nutrition["sous_nutrition"], errors='coerce')


# In[13]:


sous_nutrition.fillna(0,inplace=True)
sous_nutrition.tail()


# In[14]:


#Les données d'origine sont exprimées en millions d'habitants:
sous_nutrition["sous_nutrition"]*=1000000


# In[15]:


#Vérifier les données au milieu de data frame population
population.iloc[1213:,:]


# In[16]:


#Convertir NaN au 0
population["population"]=pd.to_numeric(population["population"], errors='coerce')
population.fillna(0,inplace=True)
#Multiplier par 1000 car la population est exprimée en milliers d'habitants
population["population"]*=1000


# In[17]:


#Extraire la population 2017
population_2017= population.loc[population["Année"]==2017,["Zone","population"]]
population_2017


# In[18]:


#Dans sous_nutrition fichier, remplacer les périodes par les années
sous_nutrition["Année"]=sous_nutrition["Année"].replace(["2012-2014","2013-2015","2014-2016","2015-2017","2016-2018","2017-2019"],
                                             ["2013","2014","2015","2016","2017","2018"])
sous_nutrition.head()


# In[19]:


#Sélectionner l'année 2017
ss_nut_2017 = sous_nutrition.loc[sous_nutrition["Année"]=="2017", ["Zone","sous_nutrition"]]
ss_nut_2017


# In[20]:


#Additioner le total de la population sous alimenté
total_ss_nut=round(ss_nut_2017["sous_nutrition"].sum(),)
total_ss_nut


# In[21]:


#Fusionner le deux data frames
pop_sn=pd.merge(population_2017,ss_nut_2017, on="Zone", how="left")
pop_sn


# In[22]:


#Calculer le total population in 2017
total_pop_2017=round(population_2017["population"].sum(),)
total_pop_2017


# In[23]:


#Calculer le total de personnes en état sous-nutrition en 2017
pers_sous_alimenté_2017 =round(ss_nut_2017["sous_nutrition"].sum(),)
pers_sous_alimenté_2017


# In[24]:


#Calculer la proportion de personnes en état de sous-nutrition
prop_pers_sous_alimenté = round((pers_sous_alimenté_2017/total_pop_2017)*100,2)
prop_pers_sous_alimenté


# In[25]:


#Afficher le résultat
print(f'En 2017, on comptait {prop_pers_sous_alimenté}% de la population était sous nutrition')


# In[26]:


#Changer le type de données
population["Année"]=population["Année"].astype(str)
sous_nutrition["Année"]=sous_nutrition["Année"].astype(str)


# In[27]:


#Joindre le data frame de population (pop) et le data frame de sous_nutrition(sn)
df_popsn=pd.merge(population,sous_nutrition,on=['Zone','Année'],how = 'outer')
df_popsn


# In[28]:


df_popsn.dtypes


# ### Question 2 : Le nombre théorique de personnes qui pourraient être nourries à partir de la disponibilité alimentaire mondiale

# In[29]:


#Vérifier la bonne importation de data frame aide alimentaire
aide_alimentaire = pd.read_csv("aide_alimentaire.csv")
aide_alimentaire.head()


# In[30]:


aide_alimentaire.tail()


# In[31]:


dispo_alimentaire = pd.read_csv("dispo_alimentaire.csv")
dispo_alimentaire.head()


# In[32]:


#Vérifier les types de données
dispo_alimentaire.dtypes


# In[33]:


dispo_alimentaire.shape


# In[34]:


dispo_alimentaire.head()


# In[35]:


#Remplacer NaN avec 0
dispo_alimentaire.fillna(0,inplace=True)


# In[36]:


#Convertir les colonnes des tonnes aux Kg
colonnes_tonnes_tokg = ['Aliments pour animaux', 'Disponibilité intérieure', 'Exportations - Quantité',
                        'Importations - Quantité', 'Nourriture', 'Pertes', 'Production',
                        'Semences', 'Traitement', 'Variation de stock', 'Autres Utilisations']

for elt in colonnes_tonnes_tokg:
    dispo_alimentaire[elt] *= 1000000


# In[37]:


#Fusionner la disponibilité alimentaire avec la population 2017
dispo_aliment= dispo_alimentaire.merge(population.loc[population['Année'] == "2017",["Zone", "population"]],
                                            on='Zone')


# In[38]:


dispo_aliment.head()


# In[39]:


#Ctréer une colonne de total disponibilité alimentaire en 2017 pour chaque pays
dispo_aliment["dispo_Kcal"]=dispo_aliment["Disponibilité alimentaire (Kcal/personne/jour)"]*dispo_aliment["population"]*365


# In[40]:


dispo_aliment.head()


# In[41]:


#Calculer le total de disponibilité alimentaire en 2017
dispo_aliment["dispo_Kcal"].sum()


# In[42]:


#Calculer le total de disponibilité alimentaire par un adulte en 2017
total_dispo_Kcal=round(dispo_aliment["dispo_Kcal"].sum()/(2600*365),1)
#Calculer la proportion de disponibilité alimentaire en 2017
proportion=round (total_dispo_Kcal*100/population[population["Année"]=="2017"]["population"].sum(),1)
print(total_dispo_Kcal)
print(proportion)


# In[43]:


#Afficher le résultat
print(f'La disponibilité alimentaire total de 2017 pourrait nourrir {total_dispo_Kcal} de personnes soit 1.1 fois la population total')


# ### Question 3: Le nombre théorique de personnes qui pourraient être nourries pour la disponibilité alimentaire des produits végétaux 

# In[44]:


#Vérifier les données de dispo alimentaire fusionnée
dispo_aliment.head()


# In[45]:


#Créer une colonne pour le total disponibilité alimentaire pour chaque pays per jour(Kcal/population/jour)
dispo_aliment["dispo_Kcal_jour"]=dispo_aliment["Disponibilité alimentaire (Kcal/personne/jour)"]*dispo_aliment["population"]
dispo_aliment["dispo_Kcal_jour"]


# In[46]:


#Filtrer les alimentaires d'origine vegetale
dispo_aliment_veg = dispo_aliment.loc[dispo_aliment["Origine"]=="vegetale",:]
dispo_aliment_veg


# In[47]:


#Calculer le total de disponibilité alimentaire d'origine vegetale per jour
dispo_aliment_veg["dispo_Kcal_jour"].sum()


# In[48]:


#Le total de disponibilité alimentaire d'origine vegetale
dispo_aliment_veg["dispo_Kcal"].sum()


# In[49]:


#Vérifier le résultat
dispo_aliment_veg["dispo_Kcal"].sum()/365


# In[50]:


#Calculer la totale population nourrie par des aliments d'origin vegetale en 2017
total_pop_veg = population[population["Année"]=="2017"]['population'].sum()
total_pop_veg


# In[51]:


#Calculer le nombre de personnes qui pourraient être nourries; un adulte a besoin de 350g/jour équivalent à 2600Kcal/jour
total_pers_nourri=round(dispo_aliment_veg["dispo_Kcal_jour"].sum()/2600,1)
total_pers_nourri


# In[52]:


#proportion de total personnes nourries
prop_pers_nourri = total_pers_nourri*100/total_pop_veg
prop_pers_nourri


# In[53]:


#Afficher le résultat
print(f'La disponibilité alimentaire des produits vegetaux de 2017 pourrait nourrir {total_pers_nourri} de personnes soit {round (prop_pers_nourri)}% de la population total')


# ### Question 4 : L’utilisation de la disponibilité intérieure, en particulier la part qui est attribuée à l’alimentation animale, celle qui est perdue et celle qui est concrètement utilisée pour l'alimentation humaine. Je crois que Julien avait trouvé un moyen de facilement calculer ces proportions.
# 
# #### 4.1 : La disponibilité intérieure = La disponibilité alimentaire
# #### L’alimentation humaine =  Nourriture 
# #### La disponilibité intérieur =  L'aliments pour animaux + Autres Utilisations + Nourriture + Pertes + Semences + Traitement
# 

# In[54]:


dispo_aliment["dispo_Kcal_jour"]=dispo_aliment["Disponibilité alimentaire (Kcal/personne/jour)"]*dispo_aliment["population"]
dispo_aliment.head()


# In[55]:


#Le total de Disponibilité intérieur
total_dispo_int=dispo_aliment["Disponibilité intérieure"].sum()
total_dispo_int


# In[56]:


#L’utilisation de la disponibilité intérieure, en particulier la part qui est attribuée à l’alimentation animale.
prop_alim_animaux = round(dispo_aliment["Aliments pour animaux"].sum()*100/(total_dispo_int),2)
prop_alim_animaux 


# In[57]:


#L’utilisation de la disponibilité intérieure, celle qui est perdue
prop_perdues =round(dispo_aliment["Pertes"].sum()*100/total_dispo_int,2)
prop_perdues


# In[58]:


#L’utilisation de la disponibilité intérieure, celle qui est concrètement utilisée pour l'alimentation humaine
prop_nourriture=round(dispo_aliment["Nourriture"].sum()*100/total_dispo_int,2)
prop_nourriture


# In[59]:


#La proportion de la disponibilité intérieur pour des autres utilisations
prop_autres_utilise=round(dispo_aliment["Autres Utilisations"].sum()*100/total_dispo_int,2)
prop_autres_utilise


# In[60]:


#La proportion de la disponibilité intérieur pour des semences
prop_semences=round(dispo_aliment["Semences"].sum()*100/total_dispo_int,2)
prop_semences


# In[61]:


#La proportion de la disponibilité intérieur pour des traitement
prop_traitement=round(dispo_aliment["Traitement"].sum()*100/total_dispo_int,2)
prop_traitement


# In[62]:


#Créer un data frame pour la représentation de repartition de disponibilité intérieur
df=pd.DataFrame({"Proportion%":[prop_alim_animaux,prop_perdues,prop_nourriture,prop_autres_utilise,prop_semences,prop_traitement]},
                  index=["Aliments pour animaux","pertes","nourriture","autres utilisations","semences","Traitement"])
df.sort_values(by='Proportion%', ascending=False)


# In[63]:


import matplotlib.pyplot as plt


# In[64]:


#La représentation de repartition de disponibilité intérieur en diagramme circulaire
#Créer le data frame pour le diagramme circulaire
data=pd.DataFrame({"Proportion":[prop_alim_animaux,prop_perdues,prop_nourriture,prop_autres_utilise,prop_semences,prop_traitement]},
                  index=["Aliments pour animaux","pertes","nourriture","autres utilisations","semences","Traitement"])
plot=data.plot.pie(y="Proportion",figsize=(10,5),autopct='%.2f%%')
plt.title("La repartition de disponibilité intérieur 2017", fontname='Arial',fontsize=18)
#Ajouter une légende
plt.legend(bbox_to_anchor=(1.5,1),loc='upper left',borderaxespad=0)
plt.show()


# In[65]:


dispo_int=dispo_aliment.loc[:,['Aliments pour animaux','Autres Utilisations','Nourriture','Pertes','Semences','Traitement']].copy()
dispo_int


# ### Les questions de Mélanie, une étude un peu plus fine pour chacun des pays 
# 
# #### Question 1 : Les pays pour lesquels la proportion de personnes sous-alimentées est la plus forte en 2017

# In[66]:


#Fusionner les data frames de la population en 2017 et la sous nutrition 2017
pop_sn_2017=pd.merge(population_2017,ss_nut_2017, on="Zone", how="left")
pop_sn_2017


# In[67]:


#Créer les nouvelles colonnes : proportion de personnes sous alimentés
pop_sn_2017["prop_pers_sous_aliment%"]=round((pop_sn["sous_nutrition"]*100/pop_sn["population"]),2)


# In[68]:


#Vérifier le noveau data frame
pop_sn_2017.head()


# In[69]:


pop_sn_2017.groupby("Zone")["prop_pers_sous_aliment%"].sum().reset_index()


# In[70]:


#Faire un classement de la proportion par ordre décroissant et afficher les 10 premiers résultats
tableau=pop_sn_2017.sort_values(by='prop_pers_sous_aliment%',ascending=False).head(10)
tableau


# In[71]:


#Afficher le résultat
print(f'Le pays pour lesquels la proportion de personnes sous_alimentées est la plus forte en 2017 est Haïti, {48.26}%')


# In[72]:


#Illustre les résultat avec un diagramme à barres 
top10_pop_sn_2017=tableau.sort_values(by='prop_pers_sous_aliment%',ascending=True)
plt.figure(figsize=(20,5))
x=top10_pop_sn_2017["Zone"]
y=top10_pop_sn_2017["prop_pers_sous_aliment%"]
plt.barh(x,y)
plt.title('Les pays pour lesquels la proportion de personnes sous-alimentées la plus forte en 2017',fontname='Arial',fontsize=18)
plt.show()


# #### Question 2 : Les pays qui ont le plus bénéficié d’aide depuis 2013
# 

# In[73]:


aide_alimentaire = pd.read_csv("aide_alimentaire.csv")
aide_alimentaire


# In[74]:


#Vérifier les données importées
aide_alimentaire.head()


# In[75]:


aide_alimentaire.describe(include='all')


# In[76]:


aide_alimentaire.isna().sum()


# In[77]:


#Remplacer les valeurs NaN avec 0
aide_alimentaire.fillna(0,inplace=True)


# In[78]:


aide_alimentaire.info()


# In[79]:


aide_alimentaire.describe(include="all")


# In[80]:


aide_alimentaire["Pays bénéficiaire"].value_counts()


# In[81]:


aide_alimentaire.info()


# In[82]:


population["Année"].astype(object)


# In[83]:


population.info()


# In[84]:


aide_alimentaire.info()


# In[85]:


#Changer le type de donées
aide_alimentaire["Année"]=aide_alimentaire["Année"].astype(int)


# In[86]:


#Changer le type de donées
population["Année"]=population["Année"].astype(int)


# In[87]:


#Renommer la colonne Pays bénéficiare au Zone
aide_alimentaire.rename(columns={"Pays bénéficiaire":"Zone"},inplace=True)


# In[88]:


#Renommer la colonne Valeur au aide tonnes
aide_alimentaire.rename(columns={"Valeur":"aide_tonnes"},inplace=True)


# In[89]:


aide_alimentaire.head()


# In[90]:


#Appliquer la fonction d'aggrégation
aide=aide_alimentaire[["Zone","aide_tonnes"]].groupby("Zone").sum()
#La quantité d'aide alimentaire a été donné en tonnes
aide.sort_values(by='aide_tonnes',ascending=False).head(10)


# #### Question 3 : Les pays ayant le plus/le moins de disponibilité par habitant 
# 

# In[91]:


#Vérification des données
dispo_alimentaire.head()


# In[92]:


dispo_alimentaire.tail()


# In[93]:


#Covertir les colonnes de Kg aux Tonnes
colonnes_kg_totonnes = ['Aliments pour animaux', 'Disponibilité intérieure', 'Exportations - Quantité',
                        'Importations - Quantité', 'Nourriture', 'Pertes', 'Production',
                        'Semences', 'Traitement', 'Variation de stock', 'Autres Utilisations']

for elt in colonnes_kg_totonnes:
    dispo_alimentaire[elt] /= 1000


# In[94]:


dispo_alimentaire.head()


# In[95]:


#Fusionner les data frame population et disponibilité" alimentaire
dispo_aliment_merge= pd.merge(population,dispo_alimentaire, on="Zone", how='left')
dispo_aliment_merge


# In[96]:


#Calculer disponibilité alimentaire par un habitant
dispo_aliment_merge["dispo_aliment_hab (Kcal/personne/jour)"]=round(((dispo_aliment_merge["Disponibilité intérieure"]*dispo_aliment_merge['Disponibilité alimentaire (Kcal/personne/jour)'])/dispo_aliment_merge["population"]),2)


# In[97]:


#Filtrer les pays selon les disponibilités intérieurs
pays_dispo_aliment=dispo_aliment_merge.groupby("Zone")["Disponibilité alimentaire (Kcal/personne/jour)"].sum().reset_index()
pays_dispo_aliment


# In[98]:


#Classer la proportion de disponibilité intérieur par ordre décroissant et afficher les 10 premiers résultats
tableau=pays_dispo_aliment.sort_values(by="Disponibilité alimentaire (Kcal/personne/jour)",ascending=False).reset_index()
tableau


# In[99]:


print(f'Le pays ayant le plus de disponibilité par habitant est Autriche, {22620} Kcal/personne/jour')


# In[100]:


tableau.iloc[170:180,:]


# In[101]:


#Filtrer les pays ayant le plus et le moins de disponibilité par habitant
tableau.loc[tableau['Disponibilité alimentaire (Kcal/personne/jour)']>0,:]


# In[102]:


#Afficher le résultat
print(f'Le pays ayant le moins de disponibilité par habitant est République centrafricaine, 11274 Kcal/personne/jour')


# #### Question 4 : Toutes les infos que tu trouverais utiles pour mettre en relief les pays qui semblent être le plus en difficulté, au niveau alimentaire.
# 
# #### L’utilisation des céréales, notamment la répartition entre l’alimentation humaine (colonne Nourriture) et l’alimentation pour animaux.

# In[103]:


#Vérifier les données
dispo_alimentaire.head()


# In[104]:


#Afficher une liste de produit
dispo_alimentaire['Produit'].unique()


# In[105]:


#Appliquer la fonction d'aggrégation les produits selon les origines
df=dispo_alimentaire.groupby(['Origine','Produit']).agg({
    'Aliments pour animaux':'sum',
    'Nourriture':'sum'
}).reset_index()
df


# In[106]:


#Creér une liste ne contient que des céréales et produits
liste_cereales = ["Blé et produits", "Riz et produits", "Orge et produits", "Maïs et produits", "Seigle et produits",
                  "Avoine", "Millet et produits", "Sorgho et produits", "Céréales, Autres"]


# In[107]:


#Création d'une table ne contenant que les informations des céréales et produits
cereales = dispo_alimentaire.loc[dispo_alimentaire['Produit'].isin(liste_cereales),:] 
cereales


# In[108]:


#Calculer la proportion de céréales et produits utilisé pour l'alimentation animale
prop_aliment_animale= round((cereales['Aliments pour animaux'].sum()*100/cereales['Disponibilité intérieure'].sum()),2)
prop_aliment_animale


# In[109]:


#Calculer la proportion de céréales et produits utilisé pour l'alimentation animale
prop_aliment_humaine= round((cereales['Nourriture'].sum()*100/cereales['Disponibilité intérieure'].sum()),2)
prop_aliment_humaine


# In[110]:


#Afficher le résultat
print("Proportion d'alimentation animale :", "{:.2f}".format(cereales['Aliments pour animaux'].sum()*100/cereales['Disponibilité intérieure'].sum()), "%")
print("Proportion d'alimentation humaine :", "{:.2f}".format(cereales['Nourriture'].sum()*100/cereales['Disponibilité intérieure'].sum()), "%")


# #### L' utilisation du manioc par la Thaïlande aux égards de la proportion de personnes en sous-nutrition. De mémoire ça concernait l’exportation par rapport à la production... Peux-tu jeter un coup d’œil et nous faire un retour ?

# In[111]:


#Fusionner les data frames population en 2017 et sous nutrition en 2017
pop_sous_nutrition = pd.merge(population.loc[population['Année'] == 2017,["Zone", "population"]],
                               sous_nutrition.loc[sous_nutrition['Année'] == '2017',["Zone", "sous_nutrition"]],
                               on='Zone')


# In[112]:


pop_sous_nutrition


# In[113]:


pop_sous_nutrition.info()


# In[114]:


#Filtrer les données de Thaïland avec une condition sur le ligne
thai = pop_sous_nutrition.loc[pop_sous_nutrition['Zone'] == 'Thaïlande',:].reset_index()
thai


# In[115]:


#Calculer la proportion de population sous alimenté
prop_sous_nutrition= round((thai['sous_nutrition'].iloc[0]*100/thai['population'].iloc[0]),2)
prop_sous_nutrition


# In[116]:


#Affichier le résultat
print('Proportion en sous nutrition en Thaïlande :', "{:.2f}".format(thai['sous_nutrition'].iloc[0]*100/thai['population'].iloc[0]), "%")


# In[117]:


dispo_alimentaire.head()


# In[118]:


dispo_alimentaire.loc[dispo_alimentaire["Zone"]=="Thaïlande",:]


# In[119]:


#Filtrer le manioc pour Thaïlande
df=dispo_alimentaire.loc[dispo_alimentaire["Produit"]=="Manioc",:]
df


# In[120]:


#Filtrer le Zone Thaïlande
data=df.loc[df["Zone"]=="Thaïlande"].reset_index()
data


# In[121]:


#Disponibilité alimentaire = Production + importations - exportation + variation des stocks
thai_dispo_int = data["Production"].iloc[0] + data["Importations - Quantité"].iloc[0] - data["Exportations - Quantité"].iloc[0] - data["Variation de stock"].iloc[0] 
thai_dispo_int


# In[122]:


#Le total de disponibilité intérieur par jour
thai_dispo_int_total= data["Disponibilité intérieure"]*data["Disponibilité alimentaire (Kcal/personne/jour)"]
thai_dispo_int_total


# In[123]:


#Calculer la proportion de population de Thaïlande qui pourrait être nourri
thai_dispo_int_prop= thai_dispo_int_total*100/2600/thai["population"]
thai_dispo_int_prop


# In[ ]:




