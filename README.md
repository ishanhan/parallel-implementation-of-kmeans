# Parallel Implementation Of kmeans
Parallel implementation of k-means clustering using MPI and PyCUDA. The main objective is to compare the performance of sequential k-means with its parallel implementation.

## Dataset

The dataset being used for this project is [Video Game Sales](https://www.kaggle.com/gregorut/videogamesales) obtained from Kaggle.
The dataset contains 11 features out of which 3 were removed using pre_processing.py (that is ``` Rank, Name and Publisher ```) and rest were transformed accordingly.

## Checklist

- [ ] Sequential K-means
- [ ] Parallel K-means using MPI
- [ ] Paralllel K-means using PyCuda
- [ ] Graphs
