# 3DGenoMikes

Welcome to 3DGenoMikes! This repository showcases the code developed for my Master's thesis "Integrating 3D Chromatin Interactions in the Transcriptional Regulation of Genes that Respond to Chromatin Stresses"

## Versions Used

- Python: 3.10.12
- Jupyter: 6.5.5

## Installation

To run this project, ensure you have at least the Python version 3.10.12 installed on your system. You can download Python from [python.org](https://www.python.org/downloads/release/python-3120/).

## General Structure of the Repository
<table>
  <tr>
    <th>Directory</th>
    <th>Description</th>
    <th>File names</th>
  </tr>
  <tr>
    <td rowspan="2">notebooks</td>
    <td rowspan="2">Code in jupyter notebooks format for the analysis of gene distribution across A/BCompartments, TADs, and frequency of interactions.</td>
    <td><code>Distribution_TAD_Compartments.ipynb</code></td>
  </tr>
  <tr>
    <td><code>Gene_Interactions.ipynb</code></td>
  </tr>
  
  <tr>
    <td rowspan="5">src</td>
    <td rowspan="5">Code for python classes that must be imported in jupyter notebooks (dir:notebooks)</td>
    <td><code>Promoter.py</code></td>
  </tr>

  <tr>
    <td><code>Tad.py</code></td>
  </tr>
  <tr>
    <td><code>Contact.py</code></td>
  </tr>
  

</table>

# Files required as input data

- **Genomic TAD and A/B compartments coordinates (Bonev et al., 2017).** A bedfile with the chromosome, start, end and type (A or B) compartment. It is provided in the supplementary material Table S2 of Bonev et al. 2017
- **Hi-C matrix of contacts.** A file .hic of 2 Gbytes with the contacts in mESCs from Bonev et al. (2017).
- **PC-HiC list of contacts.** A file .csv with the promoter-promoter significant interactions from Schoenfelder et al. (2015).
- **Gene clusters.** A file .bed with the coordinates of the genes that correspond to each cluster of study (not provided for confidentiality).

# How it works and outputs
Following the notebooks provided, from the first part to the last one:
- The distribution of gene promoters across bins of TADs is calculated, so a percentage of promoters in the bins is retrieved as output.
- The distribution of gene promoters across A/B compartments is estimated, so the percentage in each type of compartment is given as output.
- The interaction frequency from the Hi-C data is calculated based on promoter coordinates, so a relative counts of interactions are retrieved for each cluster.
- The significance of the PC-HiC interactions in each cluster is determined, so a value of significance (p-value and z-score) is shown.

## References

- Boyan Bonev, Netta Mendelson Cohen, Quentin Szabo, Lauriane Fritsch, Giorgio L Papadopoulos, Yaniv Lubling, Xiaole Xu, Xiaodan Lv, Jean-Philippe Hugnot, Amos Tanay, et al. Multiscale 3D genome rewiring during mouse neural development. In: Cell 171.3 (2017), pp. 557–572

- Stefan Schoenfelder, Mayra Furlan-Magaril, Borbala Mifsud, Filipe Tavares-Cadete, Robert Sugar, Biola-Maria Javierre, Takashi Nagano, Yulia Katsman, Moorthy Sakthidevi, Steven W Wingett, et al. The pluripotent regulatory circuitry connecting promoters to their long-range interacting elements. In: Genome research 25.4 (2015), pp. 582–597.

## Contributors

Miguel La Iglesia

MSc in Computational Biology

Technical University of Madrid (UPM)

