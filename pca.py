#this code from : https://github.com/mGalarnyk/Python_Tutorials/blob/master/Sklearn/PCA/PCA_Data_Visualization_Iris_Dataset_Blog.ipynb
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
import urllib.request



url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
# loading dataset into Pandas DataFrame
df = pd.read_csv( url, names=['sepal length','sepal width','petal length','petal width','target'])
print(df.head())

#Standardize Data : Although, all features in the Iris dataset were measured in centimeters, let us continue with the transformation of the data onto unit scale (mean=0 and variance=1), which is a requirement for the optimal performance of many machine learning algorithms.
features = ['sepal length', 'sepal width', 'petal length', 'petal width']
x = df.loc[:, features].values #取出feature 的值，轉換df<class 'pandas.core.frame.DataFrame'> 成<class 'numpy.ndarray'>
y = df.loc[:,['target']].values

x = StandardScaler().fit_transform(x)#scale (mean=0 and variance=1)
pd.DataFrame(data = x, columns = features).head()

#PCA Projection to 2D
pca = PCA(n_components=2)#the code projects the original data which is 4 dimensional into 2 dimensions.
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
principalDf.head(5)
df[['target']].head()
finalDf = pd.concat([principalDf, df[['target']]], axis = 1)#Concatenating DataFrame along axis = 1. finalDf is the final DataFrame before plotting the data.
finalDf.head(5)

#Visualize 2D Projection
#This section is just plotting 2 dimensional data. Notice on the graph below that the classes seem well separated from each other.
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 Component PCA', fontsize = 20)


targets = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
colors = ['r', 'g', 'b']
for target, color in zip(targets,colors):
        indicesToKeep = finalDf['target'] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1'], 
                   finalDf.loc[indicesToKeep, 'principal component 2'],
                   c = color,
                   s = 50
                  )
ax.legend(targets)
ax.grid()

#Explained Variance
pca.explained_variance_ratio_
#the first principal component contains 72.77% of the variance and the second principal component contains 23.03% of the variance. 

#------------------------------
 
