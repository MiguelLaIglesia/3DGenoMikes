# Contact.py

class Contact:
    """
    Class representing a contact between features with various attributes and methods to manage them.

    Attributes:
        all_contacts (list): List storing all contact instances.
        bin_interval (str): Interval for binning scores.
        max_score (str): Maximum score for the contacts.
        min_score (str): Minimum score for the contacts.
        bins (str): Binning strategy for scores.
        clusters_comparisons (str): Comparisons between clusters.
        unique_clusters (str): Unique clusters involved in the contacts.
        counts_df (str): DataFrame to store interaction counts.
    """

    all_contacts = []

    bin_interval = ''
    max_score = ''
    min_score = ''

    bins = ''
    clusters_comparisons = ''
    unique_clusters = ''
    counts_df = ''

    def __init__(self, features_1, features_2, score):
        """
        Initialize a Contact instance.

        Args:
            features_1 (list): List of features for the first contact.
            features_2 (list): List of features for the second contact.
            score (float): Interaction score between the features.

        Attributes:
            features1_counts (dict): Dictionary storing counts of features in the first contact by cluster.
            features2_counts (dict): Dictionary storing counts of features in the second contact by cluster.
        """
        self.features_1 = features_1
        self.features_2 = features_2
        self.score = score
        Contact.all_contacts.append(self)
        self.features1_counts = {}
        self.features2_counts = {}

    @classmethod
    def CalculateClusterFeatures(cls):
        """
        Calculate the number of features in each cluster for all contacts.

        The method updates the features1_counts and features2_counts attributes for each contact.
        """
        for contact in cls.all_contacts:
            contact.features1_counts = {cluster: sum(1 for feature in contact.features_1 if feature.cluster == cluster) for cluster in cls.unique_clusters}
            contact.features2_counts = {cluster: sum(1 for feature in contact.features_2 if feature.cluster == cluster) for cluster in cls.unique_clusters}

    @classmethod
    def CreateGroupsByScore(cls):
        """
        Group contacts by score bins.

        Returns:
            dict: Dictionary where keys are score bins and values are lists of contacts in those bins.
        """
        grouped_contacts = {}

        for bin_index, bin_ in enumerate(cls.bins[:-1]):
            next_bin = cls.bins[bin_index + 1]
            bin_contacts = [contact for contact in cls.all_contacts if bin_ < contact.score < next_bin]
            grouped_contacts[bin_] = bin_contacts

        # Include contacts with scores greater than the last bin
        grouped_contacts[cls.bins[-1]] = [contact for contact in cls.all_contacts if contact.score >= cls.bins[-1]]

        return grouped_contacts

    @classmethod
    def CountInteractions(cls):
        """
        Count the interactions between clusters within each score bin and update counts_df.

        The method iterates over cluster comparisons and score bins, updating the counts_df DataFrame.
        """
        contacts_by_score = cls.CreateGroupsByScore()

        for clusterA, clusterB in cls.clusters_comparisons:
            for bin_score, contacts in contacts_by_score.items():

                # Mask for the specific score bin and cluster comparison
                mask = (cls.counts_df['Score'] == bin_score) & (cls.counts_df['ClusterA'] == clusterA) & (cls.counts_df['ClusterB'] == clusterB)
                counts_to_sum = 0

                for contact in contacts:

                    if clusterA == 'all' and clusterB == 'all':
                        counts_to_sum += len(contact.features_1) * len(contact.features_2)
                    else:
                        if clusterB == 'rest':
                            # features 1 bin
                            features1 = contact.features1_counts[clusterA]
                            features2 = len(contact.features_1) - features1

                            # features 2 bin
                            features3 = contact.features2_counts[clusterA]
                            features4 = len(contact.features_2) - features3

                            counts_to_sum += (features1 * features4) + (features2 * features3)

                        elif clusterA == clusterB:
                            features1 = contact.features1_counts[clusterA]
                            features2 = contact.features2_counts[clusterA]                   

                            counts_to_sum += (features1 * features2)

                        else:  # clusterA != clusterB
                            # features 1 bin
                            features1 = contact.features1_counts[clusterA]
                            features2 = contact.features1_counts[clusterB]
                            # features 2 bin
                            features3 = contact.features2_counts[clusterA]
                            features4 = contact.features2_counts[clusterB]

                            counts_to_sum += (features1 * features4) + (features2 * features3)

                # Add counts to the DataFrame
                cls.counts_df.loc[mask, 'Counts'] += counts_to_sum

    @classmethod
    def reset_instances(cls):
        """
        Reset all contact instances.

        This method deletes all current contact instances and clears the all_contacts list.
        """
        for instance in cls.all_contacts:
            del instance
        cls.all_contacts = []