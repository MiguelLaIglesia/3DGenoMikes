# Tad.py

class Tad():
    """
    Class representing a Topologically Associating Domain (TAD) with various attributes and methods to manage them.

    Attributes:
        chromosomes (list): List of chromosomes.
        bins (list): List of bins.
        all_tads (dict): Dictionary storing all TAD instances by chromosome and identifier.
    """

    chromosomes = []
    bins = []
    all_tads = {}  # { chr : { tad_ID : tad_instance } }

    def __init__(self, chromosome, start, end, compartment):
        """
        Initialize a TAD instance.

        Args:
            chromosome (str): Chromosome where the TAD is located.
            start (int): Start position of the TAD.
            end (int): End position of the TAD.
            compartment (str): Compartment type of the TAD.

        Attributes:
            identifier (str): Unique identifier for the TAD.
            length (float): Length of the TAD in megabases.
            promoters_in_tads (dict): Dictionary storing promoters within the TAD by bins.
            promoters_density (list): Density and category (HD, MD, LD) of promoters in the TAD.
            specificity (dict): Specificity of promoters in the TAD by cluster.
        """
        self.chromosome = chromosome
        self.start = int(start)
        self.end = int(end)
        self.compartment = compartment
        self.identifier = f'TAD{start}-{end}'

        self.length = (self.end - self.start) / 1000000  # mb
        self.promoters_in_tads = {bin: [] for bin in self.bins}  # {'Bin0': [promoter_instances], 'Bin1': [promoter_instances]...}
        self.promoters_density = [0, '']  # density number, category (HD, MD, LD)
        self.specificity = {}

        self.all_tads.setdefault(self.chromosome, {})[self.identifier] = self

    @classmethod
    def LoadFromBedfile(cls, bedfile):
        """
        Load TADs from a BED file.

        Args:
            bedfile (str): Path to the BED file containing TAD data.

        Expected BED file format:
            - Column 0: Chromosome
            - Column 1: Start position
            - Column 2: End position
            - Column 3: Compartment

        The method reads the BED file and creates TAD instances.
        """
        with open(bedfile, 'r') as file:
            for line in file:
                # Split the line into columns
                columns = line.strip().split('\t')
                tad = cls(
                    chromosome=columns[0],
                    start=columns[1],
                    end=columns[2],
                    compartment=columns[3]
                )

    @classmethod
    def RetrieveAllTads(cls):
        """
        Retrieve all TAD instances.

        Returns:
            list: List of all TAD instances.
        """
        all_tads = [value for inner_dict in cls.all_tads.values() for value in inner_dict.values()]
        return all_tads

    @classmethod
    def CategorizeInDensities(cls):
        """
        Categorize TADs into density categories (HD, MD, LD) based on promoter density.
        """
        densities = {}
        all_tads = cls.RetrieveAllTads()
        for instance in all_tads:
            instance.CalculateDensity()
            densities[instance] = instance.promoters_density

        sorted_densities = dict(sorted(densities.items(), key=lambda item: item[1]))
        items = list(sorted_densities.items())
        chunk_size = (len(items) + 2) // 3  # Calculate chunk size rounding up
        density_categories = ['LD', 'MD', 'HD']
        for i in range(3):
            for tad, density_value in items[i * chunk_size:(i + 1) * chunk_size]:
                tad.promoters_density = [density_value[0], density_categories[i]]

    @classmethod
    def CalculateSpecificities(cls, clusters):
        """
        Calculate the specificity of TADs based on the distribution of promoter clusters.

        Args:
            clusters (list): List of cluster names.
        """
        all_tads = cls.RetrieveAllTads()
        for instance in all_tads:
            promoters = instance.RetrievePromoters()
            promoters_clusters = [prom.cluster for prom in promoters]

            specificity = {cluster: promoters_clusters.count(cluster) for cluster in clusters}

            total_sum = sum(specificity.values())

            if total_sum != 0:  # Avoid division by zero
                specificity = {cluster: count / total_sum for cluster, count in specificity.items()}
            else:
                specificity = {cluster: 0 for cluster in clusters}  # Set all to 0 if total_sum is 0

            instance.specificity = specificity

    def LoadPromoter(self, instance, bin):
        """
        Load a promoter into the TAD.

        Args:
            instance (Promoter): Promoter instance to load.
            bin (str): Bin in which the promoter is located.

        This method updates the promoters_in_tads attribute with the given promoter and bin.
        """
        if instance not in self.promoters_in_tads[bin]:
            self.promoters_in_tads[bin].append(instance)

    def RetrievePromoters(self):
        """
        Retrieve all promoter instances within the TAD.

        Returns:
            list: List of unique Promoter instances within the TAD.
        """
        promoters = [promoter for promoters_list in self.promoters_in_tads.values() for promoter in promoters_list]
        promoters = list(set(promoters))
        return promoters

    def CalculateDensity(self):
        """
        Calculate the density of promoters within the TAD.

        The method updates the promoters_density attribute with the number of promoters per megabase.
        """
        all_promoters = self.RetrievePromoters()
        number_promoters = len(all_promoters)
        self.promoters_density[0] = number_promoters / self.length
