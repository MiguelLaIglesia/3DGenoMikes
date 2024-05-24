# Promoter.py

class Promoter():
    """
    Class representing a promoter with various attributes and methods to manage them.

    Attributes:
        all_promoters (dict): Dictionary storing all promoter instances by identifier.
        chromosomes (list): List of chromosomes.
        cluster_members (dict): Dictionary storing promoters by their clusters.
        promoter_contacts (dict): Dictionary storing contacts between promoters.
    """

    all_promoters = {}  # identifier : instance
    chromosomes = []
    cluster_members = {}
    promoter_contacts = {}

    def __init__(self, chromosome, start, end, identifier, strand, cluster):
        """
        Initialize a Promoter instance.

        Args:
            chromosome (str): Chromosome where the promoter is located.
            start (int): Start position of the promoter.
            end (int): End position of the promoter.
            identifier (str): Unique identifier for the promoter.
            strand (str): DNA strand (+ or -).
            cluster (str): Cluster to which the promoter belongs.

        Attributes:
            tads (dict): Dictionary storing TADs associated with this promoter.
            index (str): Index of the promoter.
            n_interactions (int): Number of interactions for this promoter.
        """
        self.chromosome = chromosome
        self.start = int(start)
        self.end = int(end)
        self.identifier = identifier
        self.strand = strand
        self.cluster = cluster
        self.tads = {}  # { TAD_instance : [Bin3, Bin4] }

        self.index = ''
        self.n_interactions = 0

        # Record promoter in all_promoters
        if self.identifier not in self.__class__.all_promoters:
            self.__class__.all_promoters[self.identifier] = self
        else:
            print(f'WARNING: there are two elements with the same ID {identifier}')

    @classmethod
    def LoadFromBedfile(cls, bedfile, cluster):
        """
        Load promoters from a BED file and assign them to a cluster.

        Args:
            bedfile (str): Path to the BED file containing promoter data.
            cluster (str): Cluster to which the promoters should be assigned.

        Expected BED file format:
            - Column 0: Chromosome
            - Column 1: Start position
            - Column 2: End position
            - Column 3: Identifier
            - Column 5: Strand (+ or -)

        The method reads the BED file, creates Promoter instances, and adds them to the cluster.
        """
        with open(bedfile, 'r') as file:
            for line in file:
                # Split the line into columns
                columns = line.strip().split('\t')
                feature = cls(
                    chromosome=columns[0],
                    start=columns[1],
                    end=columns[2],
                    identifier=columns[3],
                    strand=columns[5],
                    cluster=cluster
                )
                cls.cluster_members[cluster].append(feature)
                if cluster == 'cluster1A' or cluster == 'cluster1B':
                    cls.cluster_members['cluster1'].append(feature)

    @classmethod
    def RetrieveChrMembers(cls, chr):
        """
        Retrieve all promoter instances for a given chromosome.

        Args:
            chr (str): Chromosome to retrieve promoters from.

        Returns:
            list: List of Promoter instances on the specified chromosome.
        """
        promoters = cls.all_promoters.values()
        chr_instances = [promoter for promoter in promoters if promoter.chromosome == chr]
        return chr_instances

    @classmethod
    def RetrieveClusterMembers(cls, cluster_name, rest='Not'):
        """
        Retrieve all promoter instances for a given cluster.

        Args:
            cluster_name (str): Name of the cluster to retrieve promoters from.
            rest (str): If 'Yes', retrieves promoters not in the specified cluster.

        Returns:
            list: List of Promoter instances in the specified cluster or not in the specified cluster.
        """
        promoters = cls.all_promoters.values()
        if cluster_name == 'all':
            return promoters
        else:
            if rest == 'Yes':
                cluster_instances = [promoter for promoter in promoters if promoter.cluster != cluster_name]
            else:
                cluster_instances = [promoter for promoter in promoters if promoter.cluster == cluster_name]
            return cluster_instances

    @classmethod
    def RestartNInteractions(cls):
        """
        Reset the number of interactions for all promoters to zero.
        """
        for promoter in cls.all_promoters.values():
            promoter.n_interactions = 0

    @classmethod
    def CreateRandomClusters(cls, cluster_sizes):
        """
        Randomly assign promoters to clusters of specified sizes.

        Args:
            cluster_sizes (dict): Dictionary with cluster names as keys and cluster sizes as values.
        """
        promoters_list = [promoter for promoter in Promoter.all_promoters.values()]
        # Shuffle the order of promoters
        random.shuffle(promoters_list)
        i, j = 0, 0
        flag = True
        for cluster, size in cluster_sizes.items():
            if flag:
                i = 0
                j = i + size - 1
                flag = False
            else:
                i = j + 1
                j = i + size - 1
            for promoter in promoters_list[i:j]:
                promoter.cluster = cluster

    @classmethod
    def SetOriginalClusters(cls, option):
        """
        Restore promoters to their original clusters.

        Args:
            option (str): Determines which clusters to restore.
                'cluster1AB' retains 'cluster1A' and 'cluster1B', 'cluster1' removes 'cluster1A' and 'cluster1B'.
        """
        cluster_members = cls.cluster_members.copy()
        if option == 'cluster1AB':
            cluster_members.pop('cluster1')
        else:
            cluster_members.pop('cluster1A')
            cluster_members.pop('cluster1B')

        for cluster, members in cluster_members.items():
            for member in members:
                member.cluster = cluster
    
    def LoadTad(self, tad_instance, bin):
        """
        Load a TAD (Topologically Associating Domain) for this promoter.

        Args:
            tad_instance (str): Identifier for the TAD instance.
            bin (str): Bin associated with the TAD.

        This method updates the tads attribute of the promoter with the given TAD and bin.
        """
        if tad_instance == 'Bin0' and bin == 'Bin0':
            self.tads['Bin0'] = ['Bin0']
        else:
            if tad_instance in self.tads:
                self.tads[tad_instance].append(bin)
            else:
                self.tads[tad_instance] = [bin]

    def DeleteInstance(self):
        """
        Delete this promoter instance from the all_promoters dictionary and itself.
        """
        del Promoter.all_promoters[self.identifier]
        del self
