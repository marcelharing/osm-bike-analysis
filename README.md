# OpenStreetMap Bike Analysis
<img src="https://i.imgur.com/ML4PBFf.jpeg" alt="drawing" width="430"/><img src="https://i.imgur.com/HB73o3U.gif" alt="drawing" width="385"/>

To start using the notebooks, just launch them with Google Colab or Binder. With this approach you can use the notebooks server-side.


| Notebook | Description | Google Colab | Binder |
| -------- | ----------- | ------------ | ------ |
| Intrinsic Analysis | Intrinsic quality analysis with only OSM data | <a target="_blank" href="https://colab.research.google.com/github/marcelharing/osm-bike-analysis/blob/master/Intrinsic_Analysis.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcelharing/osm-bike-analysis/HEAD) |
| Extrinsic Analysis | Extrinsic quality analysis comparing OSM data and open government data | <a target="_blank" href="https://colab.research.google.com/github/marcelharing/osm-bike-analysis/blob/master/Extrinsic_Analysis.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcelharing/osm-bike-analysis/HEAD) |
| Conflation | Feature matching and conflating both datasets to a new dataset | <a target="_blank" href="https://colab.research.google.com/github/marcelharing/osm-bike-analysis/blob/master/Conflation.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcelharing/osm-bike-analysis/HEAD) |


## Installation
It is recommended to load the notebooks using Google Colab or Binder. This approach allows for server-side execution, simplifying the process by eliminating the need for complex installations.

The specific requirements can be found in the environment.yml file. If Anaconda is already installed, open the Anaconda Prompt and navigate to the repository (which can be cloned via Git or downloaded directly from GitHub) using the ``cd`` command. Inside the repository, the environment.yml file contains all necessary dependencies.

To create the environment, run the following command:

``conda env create -f environment.yml``

The environment can then be used with JupyterLab or other editors like VS Code. For more detailed information, please refer to the documentation in the [Wiki](https://github.com/marcelharing/osm-bike-analysis/wiki).
