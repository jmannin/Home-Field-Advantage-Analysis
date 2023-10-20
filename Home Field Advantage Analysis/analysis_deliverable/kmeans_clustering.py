import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as  cm
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import pandas as pd
import numpy as np

def get_dataset():
    final_data = pd.read_csv(
        '../data_deliverable/Data/full_data/full_city_final_data.csv',
        usecols=['team_id', 'elevation', 'median_regional_income'],
        low_memory=True
    )

    team_win_percentage = pd.read_csv(
        '../data_deliverable/Data/full_data/team_win_percentage.csv',
        usecols=['team_id', 'home_win_pct'],
        low_memory=True
    )

    df = pd.merge(left=final_data, right=team_win_percentage, on='team_id')
    return df[['elevation', 'median_regional_income', 'home_win_pct']]


def kmeans_clustering_with_optimal_silhouette(df):
    # Create a range of k values to try
    k_values = range(2, 6)

    # Initialize lists to store silhouette scores
    silhouette_scores = []
    kmeans_models = []

    # Iterate over the k values and calculate silhouette score for each k
    for k in k_values:
        # Create a KMeans clustering model
        kmeans = KMeans(n_clusters=k)

        # Fit the model to the data
        kmeans.fit(df)

        # Calculate the silhouette score
        silhouette_scores.append(silhouette_score(df, kmeans.labels_))

        kmeans_models.append(kmeans)
    
    # Find the maximum silhouette score
    max_silhouette_score = max(silhouette_scores)

    # Find index of max silhouette score
    max_silhouette_index = silhouette_scores.index(max_silhouette_score)
    
    # Find the optimal number of clusters with the maximum silhouette score
    optimal_k = k_values[max_silhouette_index]

    # Find the optimal KMeans model
    optimal_model = kmeans_models[max_silhouette_index]

    # Get the cluster labels for each data point
    return df, optimal_model, optimal_k, max_silhouette_score

def plot_silhouette_and_clusters(df, kmeans, k, silhouette_score):
    # Get the cluster labels for each data point
    labels = kmeans.labels_

    # Get the clusters centers
    centers = kmeans.cluster_centers_

    # Create subplots for silhouette score and cluster scatter plot
    fig = plt.figure(figsize=(12,6))
    # fig = plt.subplots(1, 2, figsize=(12, 6))

    # Plot the silhouette score
    # axs[0].plot(k_values, silhouette_scores, 'bo-')
    ax1 = fig.add_subplot(121)
    ax1.set_xlim([-0.1, 1])
    ax1.set_ylim([0, len(df) + (k + 1) * 10])
    ax1.set_xlabel('Silhouette Coefficient Value')
    ax1.set_ylabel('Cluster Label')
    ax1.set_title('Silhouette Plot for Various Clusters')

    sample_silhouette_values = silhouette_samples(df, labels)

    y_lower = 10
    for i in range(k):
        cluster_silhouette_values = sample_silhouette_values[labels == i]

        cluster_silhouette_values.sort()

        size_cluster_i = cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / k)

        ax1.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            cluster_silhouette_values,
            facecolor=color,
            edgecolor=color,
            alpha=0.7
        )

        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        y_lower = y_upper + 10


    # Geneates vertical line for average silhouette score if all the values
    ax1.axvline(
        x=silhouette_score,
        color='red',
        linestyle='--'
    )
    ax1.set_yticks([])
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # Add the cluster labels to the team data
    df['cluster'] = labels

    # Plot the cluster scatter plot
    colors = cm.nipy_spectral(labels.astype(float) / k)

    ax2 = fig.add_subplot(122, projection='3d')

    ax2.scatter(
        df['elevation'], 
        df['median_regional_income'],
        df['home_win_pct'],
        marker='.',
        s=30,
        lw=0,
        alpha=0.7, 
        c=colors, 
        edgecolor='k'
    )

    # axs[1].scatter(
    #     centers[:, 0],
    #     centers[:, 1],
    #     centers[:, 2],
    #     marker='o',
    #     c='white',
    #     alpha=1,
    #     s=200,
    #     edgecolor='k'
    # )

    # for i,c in enumerate(centers):
    #     axs[1].scatter(c[0], c[1],c[2], marker='$%d$' % i, alpha=1, s=50, edgecolor='k')

    ax2.set_xlabel('Elevation (ft)')
    ax2.set_ylabel('Median Income ($USD)')
    ax2.set_zlabel('Home Win Percentage (%)')
    ax2.set_title('Visualization of Clusters')

    plt.suptitle('Silhouette Analysis of Major U.S Sports Teams based on Environmental Factors', fontweight='bold')

    plt.savefig('./visualizations/kmeans_clustering.png')
    plt.show()

def main():
    df = get_dataset()
    df, model, k_clusters, max_silhouette_score = kmeans_clustering_with_optimal_silhouette(df)
    plot_silhouette_and_clusters(df, model, k_clusters, max_silhouette_score)

if __name__ == '__main__':
    main()