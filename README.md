# Semantic Analysis Web Service
Project purpose is analysis and comparision education content in online courses with labour market requirements. This Web Service parses data from various sources and analyzes it using machine learning algorithm. Project was developed using Django Framework and Scikit-Learn Library. The Web Service logic's presented on the following diagramm:


![website_logic](https://user-images.githubusercontent.com/114514667/205454960-78720897-e976-4541-91c0-23966726c6d5.png)

## Parsers
List of sources:
1. https://skillbox.ru/
2. https://hh.ru/
3. https://skillbox.ru/

In cases, where data execution can be possible just from Html code, parsers was developed using Beautiful Soup 4 library. In other cases, Requests library, for HttpRequests.

## Data Processing
### Linguistic preprocessing
Linguistic processing used to prepare data before semantic alanysis and includes the following steps:
1. Convert all uppercase characters to lowercase ( "Germany" -> "germany" ).
2. Remove all punctuation characters.
3. Tokenize an entire text ( "I love you" -> ["I", "love", "you"] ).
4. Lemmatizate text( "leafs" -> "leaf", "went" -> "go" ).

All steps of linguistic preprocessing was implemented using NLTK library for Python.

### Semantic Analysis
Our problem mean that web service should analyze relationships between a set of documents and the terms they contain. So, the best way to calculate that, it's using Latent Semantic Analysis (LSA) methods. To evaluate the word in dictionary, was used TF-IDF (Term Frequency - Inverse Document Frequency) method. This is the most optimal for our problem, because it takes into account rare professional words. The formula for finding TF-IDF vector is given as:

![1_V3qfsHl0t-bV5kA0mlnsjQ](https://user-images.githubusercontent.com/114514667/205488658-cfa45c74-a38d-4d5b-9029-b583292076f0.png)
![image](https://user-images.githubusercontent.com/114514667/205496654-04decbb1-dafe-4bb0-ab45-3d15e14cbc22.png)

### Machine Learning
To splitting data by profession, the most appropriate method is K-means clustering algorithm. This is unsupervised machine learning algorithm, that takes the unlabeled dataset as input, divides the dataset into k-number of clusters, and repeats the process until it does not find the best clusters. The value of k should be predetermined in this algorithm. So, for our problem, the value of k should be equal to the number of professions.
The below diagram explains the working of the K-means Clustering Algorithm:

![k-means-clustering-algorithm-in-machine-learning](https://user-images.githubusercontent.com/114514667/205493379-da9c3150-2d93-46ab-af8f-9cae7980ddb1.png)

TF-IDF convertation method and K-Means clustering algorithm was provided by Scikit-Learn Library.

P.S. I also tried to use Affinity Propagation algorithm, due it doesn't require the number of clusters. But as a result I got either a small, or large count of clusters. Using MatPlotLib library, I printed my results on the following diagram, where the black circles is a centroids of clusters:

![affinity](https://user-images.githubusercontent.com/114514667/205495964-a2e248fe-abb7-4ab4-9e13-41b937f6337d.jpg)

For comaparison, here are the results of K-Means algorithm:

![image](https://user-images.githubusercontent.com/114514667/205496244-7a2a1396-3660-483a-9785-b08c22064f89.png)

## Database
The below diagram explains scheme of database:

![diagram_web_service](https://user-images.githubusercontent.com/114514667/205507740-d7c32e4b-6b5f-4c35-ba99-7db9f99375fe.jpg)

The field "Cluster" contains the number of cluster.

## Other developing tools

For providing background data processing, web service was developed with Celery Library.






