# OpenStreetMap Bike Analysis
**This programme allows you to easily perform quality checks on bicycle networks and automatically merge two different datasets. It is focused on Austria, but with OpenStreetMap data it can be used worldwide.**

**To use the notebooks, simply launch them with Google Colab or Binder. This will allow you to use the notebooks in your browser.**

<img src="https://i.imgur.com/ML4PBFf.jpeg" alt="drawing" width="430"/><img src="https://i.imgur.com/HB73o3U.gif" alt="drawing" width="385"/>

Google Colab is more powerful than Binder, but you need your Google account to run the notebook. For more information and a dcumentation, please refer to the [Wiki](https://github.com/marcelharing/osm-bike-analysis/wiki).

| Notebook | Description | Google Colab | Binder |
| -------- | ----------- | ------------ | ------ |
| Intrinsic Analysis | Intrinsic quality analysis with only OSM data | <a target="_blank" href="https://colab.research.google.com/github/marcelharing/osm-bike-analysis/blob/master/Intrinsic_Analysis.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcelharing/osm-bike-analysis/HEAD) |
| Extrinsic Analysis | Extrinsic quality analysis comparing OSM data and Austrian Open Government Data | <a target="_blank" href="https://colab.research.google.com/github/marcelharing/osm-bike-analysis/blob/master/Extrinsic_Analysis.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcelharing/osm-bike-analysis/HEAD) |
| Conflation | Feature matching and conflating both datasets to a new dataset | <a target="_blank" href="https://colab.research.google.com/github/marcelharing/osm-bike-analysis/blob/master/Conflation.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a> | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcelharing/osm-bike-analysis/HEAD) |
| Timeseries Cycle Network| Bonus Notebook to create a timeseries animation|<a target="_blank" href="https://colab.research.google.com/github/marcelharing/osm-bike-analysis/blob/master/Time_Series_Cycle_Network.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>| [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcelharing/osm-bike-analysis/HEAD) |
| Extrinsic Analysis worldwide | Same as Extrinsic Analysis, but only analyses OSM data and therefore usable not only in Austria, but worldwide|<a target="_blank" href="https://colab.research.google.com/github/marcelharing/osm-bike-analysis/blob/master/Extrinsic_Analysis_worldwide.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>| [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcelharing/osm-bike-analysis/HEAD) |

## Installation
It is recommended to load the notebooks using Google Colab or Binder. This approach allows for server-side execution, simplifying the process by eliminating the need for complex installations.

The specific requirements can be found in the ``environment_local.yml`` file. If  [Anaconda](https://anaconda.com/download) is already installed, open the Anaconda Prompt and navigate to the repository (which can be cloned via Git or downloaded directly from GitHub) using the ``cd`` command. Inside the repository, ``the environment.yml`` file contains all necessary dependencies.

To create the environment, run the following command:

```
conda env create -f environment_local.yml
```

The environment is called ``osmanalysis`` and can be used with JupyterLab or other editors like VS Code. 
