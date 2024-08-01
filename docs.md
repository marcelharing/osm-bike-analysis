# OpenStreetMap Bicycle Quality Analysis

## Basics
This notebook makes use of many different libraries. The most important are the [GeoPandas](https://geopandas.org) and [OSMNX](https://osmnx.readthedocs.io/en/stable/) libraries. GeoPandas stores data in tables, each row one feature object. For the data representation are different types of geometry available. In this notebook, all feature objects are stored as LineStrings. This is a sequence of points that form a line, represented by a list of coordinates. MultiLineStrings are a special form of LineStrings and consists of a collection of LineStrings.

The second library, OSMNX, can be used to generate graphs. Graphs are a mathematical model and are structured as a node-edge model. Roads and paths represent the edges, intersections the nodes. This model can be used to perform many topological analyses.
The datasets to be analysed also use a (different) data model. This will be explained in the following chapters.

The notebook also uses two web APIs. The most important is Overpass, a web API that allows users to retrieve and filter specific OSM object features and download them directly from the OSM servers. Using Overpass and defining queries requires some background information about OSM attributes and the Web API. If you don't want to spend time on this, you don't have to, as three cycling infrastructure classes are predefined already. But if you do, you can edit the type of infrastructure you want to analyse to suit your needs.

### OSM Data Model

The OSM data model consists of three primary elements: nodes, ways, and relations. Nodes represent points, with a unique identifier, latitude, and longitude. Ways are ordered lists of nodes that represent lines or polygons.
The data is made of feature objects (just called feature in this documentation), representing one geometry with random attributes. The attributes describes the feature and what it is representing in real world. All attributes can be choosen arbitrarly. 

### GIP Data Model

The GIP data model is more complex than the OSM data model. It consists of several file types, but for this notebook the GIS dataset in GeoPackage format is used. It contains, among other things, a layer with turn use relations (link relations to all edges at nodes, i.e. junctions) and a layer with individual lanes (called LinearUse). Another layer contains only cycling infrastructure and is derived from the LinearUse layer (called Radvis).

The Radvis LineStrings are edges representing the cycling infrastructure. They are segmented and not directly connected and therefore not routable. The TurnUse LineStrings connect the Radvis LineStrings at intersections. However, if you use them to connect the Radvis LineStrings, you don't get a classic Node Edge Model, because the TurnUse Lines connect at intersections with all multiple possibilities, resulting in no intersecting node point. Therefore, you can create your own Node Edge Model in this notebook.

<img src="https://i.imgur.com/BsPna5b.png" alt="drawing" width="600"/>

The image above shows the data model based on the GIS dataset. As you can see, the red (Radvis layer) and blue (TurnUse layer) layers alone are not routable and form no classical Node Edge Model. The green lines form a classical Node Edge Model.

## Intrinsic Analysis

The first Jupyter Notebook focuses on performing intrinsic analysis on OpenStreetMap (OSM) data. This means that the quality evaluation is based solely on the data and its associated metadata. The goal of these evaluations is to get an overview of the data, make heuristic quality statements, compare different geographic areas and determine the suitability for specific purposes. This approach is in line with previous studies on quality assessment of Volunteered Geographic Information (VGI) data, which are referenced in each section. The notebook classifies OSM line features into three infrastructure classes. In addition, users can define and evaluate any other class they wish. For example, one-way streets where bicycles are allowed to ride against the one-way direction could be scored.

The notebook is divided into four main sections. In the first, the study area is selected (P1), the data is prepared and the data is downloaded using the Overpass API. The second section (E1) gives an overview of the data and calculates some network based metrics. The third section (E2) looks at the history of the OSM features and the final section (E3) looks at how often the features have been edited.

### P1: Data Preparation

OSM Data is loaded with Overpass directly from the OSM servers in this chapter. Overpass has its own query language. So queries in notebook must be passed in [Overpass Query Language](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL). OSM data can be fetched with Overpass also with additional metadata. This metadata shows for every feature the time of the last edit and how often the feature has been already edited. The Overpass querries for the three infrastructure classes are created using the Overpass Turbo Wizard as helpful tool.

You can also analyze your own set of osm attributes (for example, all one-way streets where bicycles can also travel against the one-way traffic flow). In order to do so, you have also to define your own infrastructure class. You can use the Overpass [Turbo Wizard](https://overpass-turbo.eu/) to do this. However, the query output should be in XML format `[out:xml] ` and return also metadata `out meta;` so it should look like this:
```[out:xml][timeout:200];
area(id:{areaId})->.searchArea;
(
  FEATURES SETS HERE
);
(._;>;);
out meta;
```
Note that if you select attributes that are already in the other queries, there may be duplicates when summed up to total bicycle infrastructure.


### E1: First Overview of Study Area and Bicycle Infrastructure

The first chapter gives you an overview of the study area and icycle infrastructure with basic maps. In addition the orientation of the infrastructure is calculated. It shows in which cardinal directions the bicyle infrastructure as a whole is oriented and gives a sense of where the main infrastructure is aligned. For more background information see:
* Boeing, G. (2019). Urban Spatial Order: Street Network Orientation, Configuration, and Entropy. Applied Network Science, 4 (1), 67. https://doi.org/10.1007/s41109-019-0189-1

In this chapter also a topological indicator is measured, the betwenness centrality.
the betweennes centrality can give a sense how important each node or edge in a network is. It is a measure used in graph theory and measures how many  shortest paths flow through the specific edges/nodes.

In the context of bicycle networks it helps to gain an overview of important edges where many others converge. Here  However, due to the often disconnected and fragmented nature of bicycle networks, the validity of the betweenness centrality may be limited.

For more theoretical background information see:
* Porta, S., Crucitti, P., & Latora, V. (2006). The Network Analysis of Urban Streets: A Primal Approach. Environment and Planning B: Planning and Design, 33(5), 705-725. https://doi.org/10.1068/b32045
* [Betweenness centrality on Wikipedia](https://en.wikipedia.org/wiki/Betweenness_centrality)
* [Betweenness centrality on the documentation of the python library](https://docs.momepy.org/en/stable/generated/momepy.betweenness_centrality.html) and the respective paper: Fleischmann, M. (2019) ‘momepy: Urban Morphology Measuring Toolkit’, Journal of Open Source Software, 4(43), p. 1807. https://doi.org/10.21105/joss.01807

For an example study using betweenness with bicycle networks:
* Beck, B., Pettit, C., Winters, M., Nelson, T., Vu, H. L., Nice, K., … Saberi, M. (2024). Association between network characteristics and bicycle ridership across a large metropolitan region. International Journal of Sustainable Transportation, 18(4), 344–355. https://doi.org/10.1080/15568318.2024.2308266

### E2: History Analysis

This evaluation shows the bicycle infrastructure in a time series with [OSHDB](https://github.com/GIScience/oshdb) and OSHOME API. OSHDB stands for OpenStreetMap History Database and allows you to analyse the history of OpenStreetMap feature objects since 2008 for every possible region and time. OSHDB is written in Java, but is accessible with the [OSHOME Web API](https://docs.ohsome.org/ohsome-api/v1/).

<center>
<img src='https://i.imgur.com/cJ1GLrv.png' alt='drawing' width='400'/><br>
<small><i>Scheme of OSHDB from Auer et. al (2018)</i></small>
</center>

Depending on the growth rates, you can estimate how complete the cycling infrastructure is in your study area. This qualitative indicator helps to get a first impression. It is particularly useful when comparing with other areas, different infrastructure classes and their growth rates. For more information on the relationship between time and OSM completeness, see
* Barron, C., Neis, P. and Zipf, A. (2014). A Comprehensive Framework for Intrinsic OpenStreetMap Quality Analysis. Transactions in GIS, 18: 877-895. https://doi.org/10.1111/tgis.12073
* Neis, P., Zielstra, D., and Zipf, A. (2013). "Comparison of Volunteered Geographic Information Data Contributions and Community Development for Selected World Regions" Future Internet 5, no. 2: 282-300. https://doi.org/10.3390/fi5020282

For more information on the OHSOME platform see:
* Auer, M., Eckle, M., Fendrich, S., Kowatsch, F., Loos, L., Marx, S., Raifer, M., Schott, M., Troilo, R., Zipf, A. (2018). Ohsome – eine Plattform zur Analyse raumzeitlicher Entwicklungen von OpenStreetMap-Daten für intrinsische Qualitätsbewertungen. AGIT ‒ Journal für Angewandte Geoinformatik, 4-2018: 162-167. https://doi.org/10.14627/537647020
* Raifer, M., Troilo, R., Kowatsch, F. et al. OSHDB: a framework for spatio-temporal analysis of OpenStreetMap history data. Open geospatial data, softw. stand. 4, 3 (2019). https://doi.org/10.1186/s40965-019-0061-3

If you want to analyse your own infrastructure, you need to define a query again, but this time in the Overpass Turbo Wizard language (because OSHDB only supports this). It's a different query language to the Overpass language, but much simpler. It is the query for Overpass Turbo [Overpass Turbo Wizard language](https://wiki.openstreetmap.org/wiki/Overpass_turbo/Wizard).

### E3: Linus Law: Version of OSM Features

Overpass can return the version of a feature. The version indicates how many times a feature has been edited. Features in OSM are marked as edited if the geometry or attributes have been edited. Linus Law points out that "given enough eyeballs, all errors are shallow". In this context, this means that if more people edit something, there is a chance of higher correctness.

The distribution shows how many features have been edited and how often. The 10% quantile shows that 10% of the features have at least the given version and 90% have a higher version. The distribution is finally shown in a histogramm graphically.

For more background information to the relation of OSM version and correctness see:
* Keßler, C., de Groot, R.T.A. (2013). Trust as a Proxy Measure for the Quality
of Volunteered Geographic Information in the Case of OpenStreetMap. In: Vandenbroucke, D., Bucher, B., Crompvoets, J. (eds) Geographic Information Science at the Heart of Europe. Lecture Notes in Geoinformation and Cartography. Springer, Cham. https://doi.org/10.1007/978-3-319-00615-4_2
* Haklay, M. (2010). How Good is Volunteered Geographical Information? A Comparative Study of OpenStreetMap and Ordnance Survey Datasets. Environment and Planning B: Planning and Design 37 (4), 682–703. https://doi.org/10.1068/b35097.


## Extrinsic Analysis

The second Jupyter Notebook focuses on performing extrinsic analysis on OpenStreetMap (OSM) data and with official bicycle network data from the Austrian GIP data. The goal of these evaluations is to compare the two datasets and evaluate its quality. All evaluations are inspired by previous studies on quality assessment of Volunteered Geographic Information (VGI). Like the first notebook, this notebook also classifies OSM and GIP line features into three infrastructure classes.

The notebook is divided into two main sections. P1 - P4 is for data preparation and setting up the environment. E1 - E7 represents several quality analysis sections.

### P1: Import Libraries

P1 imports all needed libraries. It also sets up the environment file paths and checks if the notebook is executed local or on Google Colab. Also variables like certain basemap providers and colors for the foliom web map are defined.

### P2: Study area and Parameters

In P2 the study area can be choosen. A function from OSMNX library converts the boundary of Othe study area into a GeoDataFrame. The area has to be on OSM with a relation geometry. From that area the center is calculated to have a starting point for the folium web maps.

Secondly, the Coordinate Reference System (CRS) is defined. By default automatically a UTM CRS (i.e. projected CRS) suitable for the styudy area is choosen. But you can also define your own Coordinate Reference System (CRS). Note that the CRS metrics has to be in meters.

Thirdly, you can choose how big the grid for evaluation E7 should be. The bigger the grid, the more fine grained the results are.

### P3: Load and Preprocess OSM Data

In this section the OSM data is loaded and preprocessed.

#### Querry Data and Classify Data

Data is loaded with Overpass directly from the OSM servers. Overpass has its own query language. So queries in notebook must be passed in [Overpass Query Language](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL). OSM data can be fetched with Overpass also with additional metadata. This metadata shows for every feature the time of the last edit and how often the feature has been already edited.

The Overpass querries for the three infrastructure classes are created using the Overpass Turbo Wizard as helpful tool. They are classified in such a way that the classes are the same as the classes from the GIP data. The classes consist of OSM features with the following attributes:

**Cyle Tracks (Radweg bzw. Geh- und Radweg)**
```
highway=cycleway 

OR (highway=path OR highway= footway) AND (bicycle=designated OR bicycle=yes OR bicycle=permissive)

OR (cycleway=track OR cycleway=opposite_track) 
OR (cycleway:right=track OR cycleway:right=opposite_track) 
OR (cycleway:left=track OR cycleway:left=opposite_track) 
OR (cycleway:both=track OR cycleway:both=opposite_track) 
```

**Cycle Lanes (Radfahrstreifen bzw. Mehrzweckstreifen)**
```
(cycleway=lane OR cycleway=opposite_lane) 
OR (cycleway:right=lane OR cycleway:right=opposite_lane)
OR (cycleway:left=lane OR cycleway:left=opposite_lane)
OR (cycleway:both=lane OR cycleway:both=opposite_lane)
```

**Calm Traffic Ways (Verkehrsberuhigter Bereich bzw. Weg)**
```
/* Motorized vehicles with access attribute explicitly limited/prohibited, wheel implicitly allowed (no own access attribute, but default value is assumed as permission) */
( 
(highway=track OR highway=service OR highway=unclassified OR highway=residential)
AND bicycle!=*
AND (motor_vehicle=private OR motor_vehicle=no OR motor_vehicle=customers OR motor_vehicle=agricultural OR motor_vehicle=forestry OR motor_vehicle=destination OR motor_vehicle=delivery)
)
OR
/* Motorized vehicles with access attribute explicitly limited/forbidden, bike with access attribute explicitly allowed */
( 
(highway=track OR highway=service OR highway=unclassified OR highway=residential)
AND ( (motor_vehicle=private OR motor_vehicle=no OR motor_vehicle=customers OR motor_vehicle=agricultural OR motor_vehicle=forestry OR motor_vehicle=destination OR motor_vehicle=delivery) OR (access=private OR access=no OR access=customers OR access=agricultural OR access=forestry OR access=destination OR access=delivery) OR (vehicle=private OR vehicle=no OR vehicle=customers OR vehicle=agricultural OR vehicle=forestry OR vehicle=destination OR vehicle=delivery) )
AND (bicycle=designated OR bicycle=yes OR bicycle=permissive)
)
OR
/* Motorized vehicle implicitly limited/prohibited (no separate access attribute, but dirt tracks/forest tracks are assumed to limit motorized vehicles), bike explicitly allowed with access attribute */
(
highway=track 
AND (bicycle=designated OR bicycle=yes OR bicycle=permissive) AND (motor_vehicle!=* AND access!=* AND vehicle!=*) )
OR
/* Residential street / Meeting zone (Wohnstraße / Begegnungszone) */
(
highway=living_street
)
OR
/* Bicycle road (Fahrradstraße) */
(
bicycle_road=yes
)
OR
/* Pedestrian zone and bike explicitly allowed with access attribute */
(
highway=pedestrian 
AND (bicycle=designated OR bicycle=yes OR bicycle=permissive)
)
```

If you want to analyze your own set of osm attributes (for example, all one-way streets where bicycles can also travel against the one-way traffic flow), you can define and analyse your own infrastructure class. The best way to so is to use the Overpass [Turbo Wizard](https://overpass-turbo.eu/) to do this. However, the query output should be in XML format `[out:xml]` and return also metadata `out meta;` so it should look like this:

```
[out:xml][timeout:200];
area(id:{areaId})->.searchArea;
(
  FEATURES SETS HERE
);
(._;>;);
out meta;
```
Note that you can only analyze LineStrings (in OSM these are all way geometries).
#### Load Data

The raw OSM data is saved in three (due to three infrastructure classes) OSM-XML files. From this files, in a first step OSMNX graphs for all infrastructure classes are made. In a next step GeoDataFrames are made for all three infrastructure classes from the OSM-XML files. Altough OSM-Data can also be fetched from OSM servers directly with OSMNX library, GeoDataFrames have to be directly compiled from the raw OSM-XML files because than more complex querries are possible. Also metadata output is not possible with OSMNX.

All data is then saved in three dictionary, one for each infrastructure class. The dictionary, contains this keys and values:

* 'query': The query statement to retrieve the data from OSM servers.
* 'name': The name of the infrastructure class.
* 'graph': Routable directed OSMNX graph. This graph is routable and represents the infrastructure in both directions (i.e. edges are bidirectional). It is projected and clipped to the study area at the next edge outside the study area. Note that the edge directions are based on regular vehicle traffic (e.g. one way for cars than are only represented as one edge). To analyse bicycle traffic, it is important to convert and use an undirected graph.
* 'gdf_xml': A separate GeoDataFrame directly from the XML file.
This GeoDataFrame includes 'version' and 'timestamp' columns, which are part of the Overpass API's meta output. Note that OSMNX does not provide this metadata. However, the XML-derived GeoDataFrame is not routable and contains the original number of OSM features. The nodes which were used for OSMNX will be excluded to prevent errors, if there are no features a empty GDF is created. It is projected and clipped to the study area directly where the study area polygon intersects the features with a buffer tolerance of 1.5m.

Additionally a dictionary for all infrastructure classes together (total amount of features) is created. It is concatenated/composed from the three GeoDataframes/graphs before and it contains the following keys and values:

* 'name': The name of the infrastructure class.
* 'graph': Routable directed OSMNX graph. This graph is routable and represents the infrastructure in both directions (i.e. edges are bidirectional). Like the other graphs it is projected and clipped to the study area at the next edge outside the study area. Note that the edge directions are based on regular vehicle traffic (e.g. one way for cars than are only represented as one edge). To analyse bicycle traffic, it is important to convert and use an undirected graph.
* 'gdf_xml': A separate GeoDataFrame directly from the XML file. This GeoDataFrame includes 'version' and 'timestamp' columns, which are part of the Overpass API's meta output. Note that osmnx does not provide this metadata. However, the XML-derived GeoDataFrame is not routable and contains the original number of OSM features. The nodes which were used for osmnx will be excluded. To prevent errors, if there are no features a empty GDF is created. Like the other GDFs, it is projected and clipped to the study area directly where the study area polygon intersects the features with a buffer tolerance of 1.5m.
* 'gdf_xml_dt': Same as gdf_xml but with datetime objects; folium can't handle datetime objects so there is a own gdf

The graph is used for topological evaluations. In this notebook these are the Dangling Nodes Analysis (E2), Components Analysis (E3) and Missing Links Analysis. The graphs are in some ways a little bit different than the GeoDataFrames. The graph is directed (so the edges are bidirectional) and it is not directly clipped at the study area (it is clipped at the next edge outside the study area). Therefore for all other analyses, a GeoPandas GeoDataFrame is used.

#### Process Data

In this section, also possible MultiLineStrings and Polygons are converted into LineStrings. To prevent some issues in edge cases, all  geometries other than Linestrings are dropped. MultiPolygons often appear when Linestrings are connected and interpreted as ring, Multilinestrings appear when LineStrings are not directly connected as a line.
In some rare cases there can be duplicates. This is the case when a LineString is classified in more than one infrastructure class (for example because a street is a calm traffic way and has in addition cycle lanes).
This data procession is only made with the GeoDataFrames, because OSMNX loads all features automatically.

After all, the actual infrastructure length is calculated. In OSM, bicycle infrastructure can be mapped with its own geometry or with attributes on main roads. In the CycleOSM image underneath, the cycle track in the park has its own geometry, and the cycle track on the road from west to east is attached to the road geometry.

<img src="https://i.imgur.com/kxSkubZ.png" alt="drawing" width="400"/>

If a main street has two cycle lanes or cycle tracks (one per direction), both uses the same geometry. This means that based on the attributes, the actual cycle infrastructure length can be twice as long than the geometry length. For more info see [cycle lanes](https://wiki.openstreetmap.org/wiki/Tag:cycleway%3Dlane) and [cycle tracks](https://wiki.openstreetmap.org/wiki/Tag:cycleway%3Dtrack) on the OSM wiki.

### P4: Load and Preprocess GIP Data

In this section the GIP data is loaded and preprocessed.

#### Download Data

The GIP data is directly downloaded from the official source.

#### Clip and Reclassification of GIP Data

The GIP data is clipped to your defined area and filtered so that only certain pre-defined values of cycling infrastructure are retained. Classes such as bus lanes or one-way cycle lanes open for bikes are excluded because they are difficult to analyze and cannot be considered as infrastructure primarily for cycling. Also, cases when a feature has different values in the straight ahead and opposite direction are handled. The three infrastructure classes are classified in such a way that the classes are the same as the classes from the OSM data. The classes consist of GIP features with the following attributes:

**Calm Traffic Ways**

* BGZ - Begegnungszone
* FRS - Fahrradstraße
* FUZO - Radfahren in Fußgängerzonen
* FUZO_N - Radfahren in Fußgängerzonen (Nebenfahrbahn)
* VK_BE - Verkehrsberuhigte Bereiche
* WSTR - Radfahren in Wohnstraßen
* WSTR_N - Radfahren in Wohnstraßen (Nebenfahrbahn)
* RVW - Radfahren auf verkehrsarmen Wegen (unbefestigter Weg)

**Cycle tracks**

* GRW_M - Gemischter Geh- und Radweg
* GRW_MO - Gemischter Geh- und Radweg ohne Benützungspflicht
* GRW_T - Getrennter Geh- und Radweg
* GRW_TO - Getrennter Geh- und Radweg ohne Benützungspflicht
* GRW_MV - Gemischter Geh- und Radweg verordnet (nur Visualisierung)
* GRW_MOV - Gemischter Geh- und Radweg ohne Benützungspflicht verordnet (nur Visualisierung)
* RW - Baulicher Radweg
* RWO - Radweg ohne Benützungspflicht
* RFUE - Radfahrerüberfahrt
* SCHUTZWEG_RFUE - Querung Schutzweg und Radfahrüberfahrt
* TRR - Treppe auch für Radfahrer geeignet
* SGT - Singletrail
* MTB - Mountainbikestrecke (Radfahren im Wald)

**Cycle Lanes**

* MZSTR - Mehrzweckstreifen
* RF - Radfahrstreifen

All GIP data is stored in one dictionary. It is reprojected and clipped to the study area with a buffer tolerance of 1.5m and contains these keys and values:

* 'graph': routable undirected OSMNX graph. This graph is routable and represents the infrastructure like the geometrical representation (i.e. edges are not bidirectional). It is created by the selected model stored as 'evaluate_model'.
* 'turnuse': Stores only TurnUse Linestrings.  TurnUse LineStrings are in the GIP model special Linestrings that connects the features (in this case radvis features) representing the edges at intersections (nodes).
* 'radvis': Stores only Radvis LineStrings Radvis LineStrings are edges which represents the bicycle infrastructure. They are segmented and not directly connected. With TurnUse LineStrings you can connect them.
* 'radvise_turnuse': Stores the TurnUse Edge Model, where Radvis features connected with TurnUse features are stored. 
* 'connected_radvis': Stores the Node Edge Model, where Radvis features are connected with each other without original TurnUse Linestrings to get a classical Node Edge Model


#### Topological Models

The GIP data set of the cycling infrastructure is not available as a Node Edge Model. It must first be modelled as such.
In the notebook it's possible to modelle either the original model with edge linestrings and TurnUse linestrings. Or a classical node-edge model, where each edge is connected to the node (and not via TurnUse LineStrings).

Note that the choice of model also affects the length of the cycle network. If you add the TurnUse LineStrings to the network, the length will be overestimated, if you don't add them, the length will be underestimated. So when comparing the length of the network in the following evaluations, be careful because the two different data models from OSM and GIP can't be compared one to one. In the picture underneath there is a comparison of the two models, in grey are the original and new constructed TurnUse LineStrings.
<img src="https://i.imgur.com/AGqxA3j.png" alt="drawing" width="600"/>

#### GIP Data to Graph

The GIP graph is also modelled using OSMNX. However, to create an OSMNX graph from a GeoDataFrame
* Nodes with an id (osmid) and coordinates
* Edges with u (edge start point), v (edge end point), key properties (special network x key for parallel edges).

are required. This is done automatically. The graph is undirected and based on the model previously selected.


### E1: Timestamp of the last Edit (Uptodateness)

Uptodateness shows how up-to-date are feature is. Overpass can return the date a feature was last edited. The GIP data has also a column showing the date of last edit. In this evaluation the timestamp distribution is calculated. It shows how many features were edited at what time.

Note, that in this quality assessment, only the original Linkuse/Radvis data from GIP is assessed, but not the TurnUse Links. This is because Linkuse/Radvis features essentially represent the bicycle infrastructure and TurnUse Links doesn't have a Timestamp as attribute.

For more infos and other case studies of uptodateness analysis of OSM data see:
* Minghini M., Frassinelli F. (2019). OpenStreetMap history for intrinsic quality assessment: Is OSM up-to-date?. Open geospatial data, softw. stand. 4, 9. https://doi.org/10.1186/s40965-019-0067-x
* Barron C., Neis P. and Zipf A. (2014). A Comprehensive Framework for Intrinsic OpenStreetMap Quality Analysis. Transactions in GIS, 18: 877-895. https://doi.org/10.1111/tgis.12073
* Neis P., Zielstra D., and Zipf A. (2013). "Comparison of Volunteered Geographic Information Data Contributions and Community Development for Selected World Regions" Future Internet 5, no. 2: 282-300. https://doi.org/10.3390/fi5020282
* Sehra S.S., Singh J., Rai H.S. (2017). Assessing OpenStreetMap Data Using Intrinsic Quality Indicators: An Extension to the QGIS Processing Toolbox. Future Internet 9, no. 2: 15. https://doi.org/10.3390/fi9020015

### E2: Dangling Nodes

Dangling nodes are nodes in the network that can only be reached from one edge. They therefore represent dead ends in comparison to intersections. Dangling nodes are not wrong per se, but if the number of dangling nodes in a data set differs significantly from the other data set (and they are also approximately the same length), this is an indication of topological errors. So this evaluation is a qualitative one, assessing the fitness for use of the data. 

For further use cases and studies see:
* Neis P., Zielstra D., Zipf A. (2012). The Street Network Evolution of Crowdsourced Maps: OpenStreetMap in Germany 2007–2011. Future Internet. 4(1):1-21. https://doi.org/10.3390/fi4010001
* Vierø A. R., Vybornova A., Szell M. (2023). BikeDNA: A tool for bicycle infrastructure data and network assessment. Environment and Planning B: Urban Analytics and City Science. https://doi.org/10.1177/23998083231184471.

### E3: Components Analysis

Bicycle networks are often disconnected and fragmented, thus they are made of different components. Analysing the components, their length and the distribution of a length can give a sense of the bicycle network and the completness of the data.

For further use cases and studies see:
* Vierø A. R., Vybornova A., Szell M. (2023). BikeDNA: A tool for bicycle infrastructure data and network assessment. Environment and Planning B: Urban Analytics and City Science. https://doi.org/10.1177/23998083231184471.
* Vierø A. R., Vybornova A., Szell M. (2023). How Good Is Open Bicycle Infrastructure Data? A Countrywide Case Study of Denmark. https://doi.org/10.48550/arXiv.2312.02632.

### E4: Missing Links

Missing Links are potential gaps in the network between two close edges. Either because the bicycle network is designed this way in reality or because there are topological error in the dataset.<br>
With a low tolerance limit (about 1 meters or less), an error in the data can generally be assumed because two edges are very close to each other but are not connected.

So note that this evaluation only gives an indication of where missing links might be, but they do not necessarily have to be one (because the infrastructure is the same in real life, or because edges cross or are near other edges on different levels, such as bridges or tunnels).In the picture underneath is an example of a topological error. The LineStrings are not connected with each other and have only a very narrow gap (less than 10cm),

<img src="https://i.imgur.com/4X3ldKY.png" alt="drawing" width="500"/>


For more infos and further studies see:
* Neis P., Zielstra D., Zipf A. (2012). The Street Network Evolution of Crowdsourced Maps: OpenStreetMap in Germany 2007–2011. Future Internet. 4(1):1-21. https://doi.org/10.3390/fi4010001
* Vierø A. R., Vybornova A., Szell M. (2023). BikeDNA: A tool for bicycle infrastructure data and network assessment. Environment and Planning B: Urban Analytics and City Science. https://doi.org/10.1177/23998083231184471.

### E5: Attribute Completness

The evaluation of semantic attributes on geodata is a simple but effective way of determining the quality of geodata. 
The accuracy of the attributes can be evaluated or just the mere presence of attributes. In this case, the presence of the attributes is evaluated; different attributes can be preselected for both data sets. The more features a particular attribute has, the more complete the data set can be considered to be.

For further studies of attribute completness evaluations see:
* Girres J.F., Touya G. (2010). Quality assessment of the French OpenStreetMap dataset. Trans GIS; 14(4) :435–459. https://doi.org/10.1111/j.1467-9671.2010.01203.x
* Barron C., Neis P. and Zipf A. (2014). A Comprehensive Framework for Intrinsic OpenStreetMap Quality Analysis. Transactions in GIS, 18: 877-895. https://doi.org/10.1111/tgis.12073
* Ludwig I., Voss A., Krause-Traudes M. (2011). A Comparison of the Street Networks of Navteq and OSM in Germany. Advancing Geoinformation Science for a Changing World. Lecture Notes in Geoinformation and Cartography(), vol 1. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-19789-5_4

### E6: Length

This section compares the length of the two data sets. This is a quality measure with rather limited informative value because a data set can contain not only errors of ommission but also errors of commission (i.e. an over-recording of infrastructure) and because it provides no information about where exactly the length of the data sets differs.

Nevertheless, it is a frequently and simply used quality measure that can provide an indication of the quality of the data set.

The first studies to analyse the quality of OSM data also evaluated the length. Important papers are:
* Hochmair H., Zielstra D., Neis P. (2015). Assessing the completeness of
bicycle trail and lane features in OpenStreetMap for the United States
Transactions in GIS, 19 , pp. 63-81.
* Haklay M. (2010). How Good is Volunteered Geographical Information? A Comparative Study of OpenStreetMap and Ordnance Survey Datasets. Environment and Planning B: Planning and Design, 37(4), 682-703. https://doi.org/10.1068/b35097

However, it should be noted that in these studies the OSM data was compared with a reference dataset and the length was compared on this basis.

### E7: Grid Based Length (Density of Features)

This evaluation compares the length of the two datasets on a grid basis. This quality measure allows a more in-depth and comprehensive examination of the length of the datasets. The study area is divided into grid cells and the length is calculated for each cell box. This allows you to find hotspots with a lot of cycling infrastructure and also hotspots with large differences in cycling infrastructure length between the two datasets. You can also investigate the grid cell and search for cells with high difference or investigate the overall difference.

The first studies which analyzed the length on grid base are:
* Haklay M. (2010). How Good is Volunteered Geographical Information? A Comparative Study of OpenStreetMap and Ordnance Survey Datasets. Environment and Planning B: Planning and Design, 37(4), 682-703. https://doi.org/10.1068/b35097
* Zielstra D., Zipf A. (2010). A Comparative Study of Proprietary Geodata and Volunteered Geographic Information for Germany. In: M. Painho, M.Y Santos, H. Pundt. AGILE 2010. Proceedings of the 13th international conference on geographic information science, Guimaraes, Portugal. https://agile-gi.eu/images/conferences/2010/documents/shortpapers_pdf/142_doc.pdf 

With regard to bicycle infrastructure, the Vierø study should be mentioned again:
* Vierø A. R., Vybornova A., Szell M. (2023). BikeDNA: A tool for bicycle infrastructure data and network assessment. Environment and Planning B: Urban Analytics and City Science. https://doi.org/10.1177/23998083231184471.


## Feature Matching and Conflation

The first and last Notebook is about feature matching. Feature matching and data conflation is the process of finding matching features and merging two different data sets. This can be done based on criteria such as the geometry, distribution, topology, or attributes of the features. The purpose of data intersection can be to increase and harmonize data coverage, detect errors, or update geodata.

In this Notebook, features from both datasets are matched. On the one hand, the matching results can be used to make statements about the quality of the data, and on the other hand, both data sets can be conflated. The user can flexibly decide for himself/herself how this conflation is carried out in order to ultimately generate a new, qualitatively better and more complete data set.

### P1 - P4: Data Preparation

Datapreparation is the same like in second Notebook Extrinsic Analysis. The only difference is that with GIP data only data model is available, the node-edge model. It demonstrates the most optimal results.

### P5: Feature Matching
The feature matching process checks which bicycle infrastructure occurs in both data sets. 
This makes it possible to make statements about the completeness of the data sets and to obtain a subgroup of features that have been confirmed by the other data set. It should be noted that the feature matching process only evaluates the geometry, not the thematic accuracy or completeness of the attributes of the features in the data sets.

The feature matching of disparate data sets represents a distinct area of research in its own right. The matching algorithm in this notebook was taken from:
* Vierø A. R., Vybornova A., Szell M. (2023). BikeDNA: A tool for bicycle infrastructure data and network assessment. Environment and Planning B: Urban Analytics and City Science. https://doi.org/10.1177/23998083231184471

And the authors of the matching algorithm were inspired by:
* Will, J. (2014). Development of an automated matching algorithm to assess the quality of the OpenStreetMap road network : a case study in Göteborg, Sweden. Student thesis series Ines. https://lup.lub.lu.se/luur/download?fileOId=4466312&func=downloadFile&recordOId=4464336
* Koukoletsos T. , Haklay M.,  Ellu C. (2011). An automated method to assess Data Completeness and Positional Accuracy of OpenStreetMap. GeoComputation 2011. https://www.geog.leeds.ac.uk/groups/geocomp/2011/papers/koukoletsos.pdf

In fact, the matching algorithm works as follows. It starts by dividing the features into segments of the desired segment length. Potentially matching segments are then identified using a buffer. If the above matching criteria are met, a corresponding counterpart is selected from the potentially matching segments in the opposite data set. Finally, the segments are reassembled back into features. 

#### Define Matching Parameters
The feature matching process is based on four parameters that you can define and which influence the results of the matching process.

* Segment length: Before matching, all features are divided into segments. These segments are compared and for each segment the best matching segment in the other dataset is found. The smaller the segments, the longer the matching process.
* Buffer distance: Maximum distance that corresponding matches can be from each other.
* Maximum Hausdorff distance: The Hausdorff distance is a geometric measurement that measures the maximum deviation between two  mathematical subsets. In this case the subsets are LineString features. In contrast to a simple euclidian distance, with Hausdorff distance it's possible to take also the shape of features into account when meassuring the distance to each other. The higher the threshold, the more segments are matched. For more background information, see the related [Wikipedia article](https://en.wikipedia.org/wiki/Hausdorff_distance).
* Angular Threshold: The maximum angle between two potential segments. Segments above this threshold are excluded from the matching process. The higher the threshold, the longer the process takes.

The default settings take into account the width of multi-lane roads (to match also segments modelled in different ways), bicycle networks with more fragmented parts (hence a rather low segment length) and segments, especially GIP segments, which have a wide orientation at intersections compared to the actual road (hence a rather high angular threshold).

At the same time, it is important to approach feature matching as an iterative process, as the matching process is not perfect when comparing two different datasets,
So try using the default settings first, check the results, and then revise the settings if necessary.

### E1: Feature Matching Results
The matching results allow for the formulation of statements regarding the completeness of the datasets. The following diagrams illustrate the proportion of matching segments, indicating the percentage of total segments that were matched.
However, since it must be assumed that both data sets contain errors and do not fully reflect reality, the best statements can be made in combination with each other.

If the first dataset shows a high degree of agreement with the second, but the second does not agree with the first, this may be due to either a lack of infrastructure in dataset one or an excess of infrastructure in dataset two. Either would be an error in completeness (i.e. errors of emmission and commission). On the other side too much features (errors of commission) are perhaps better to proof and less common like errors of emmission.

If the match between the two datasets is low, then both datasets can be considered as bad quality. However, a lower level of agreement in both datsets also increases the potential for conflation in the next chapter, as different characteristics are then combined into one data set.

The following table is from [Koukoletsos et al.](https://www.geog.leeds.ac.uk/groups/geocomp/2011/papers/koukoletsos.pdf) which can also help intepreting the results:
| Percentage OSM Matching | Percentage GIP Matching | Percentage Matching mixed | Meaning                            |
|-------------------------|-------------------- ----|---------------------------|------------------------------------|
| High                    | High                    | High                      | Datasets agree with each other     |
| High                    | Low                     | Low                       | GIP dataset denser                 |
| Low                     | High                    | Low                       | OSM dataset denser                 |
| Low                     | Low                     | Low                       | Datasets contain different data    |

## E2: Conflation

In this last section a new data set is created based on conflation. Conflating the two different data sets from OSM and GIP offers the advantage of creating a qualitatively better and more complete data set.

The conflation works in such a way that all infrastructure that occur in both datasets, as confirmed by feature matching, are  conflated into the new dataset in advance without further checks or processes, because this segments have been proved by the two datasets. <br>However "doubtful" segments, i.e. segments representing infrastructure that only occur in one data set, are less trustworthy. In the following chapter you can decide what to do with this doubtful segments from both GIP and OSM datset.

You now have the following options as to what to do with these “dubious” features:
* Firstly, you can decide what the base data model should be. If you choose the GIP model, the GIP features which are already matched are taken. And vice versa for the OSM option. 
* You can then decide whether the "doubtful" segments should be manually checked at all. If you don't want to check the "doubtful" segments manually, all "doubtful" segments are considered to be conflated. iF you want, you can check and validate each segment. 
* The next option allows you to specify whether the 'Doubtful' segments should be automatically checked and partially proofed based on their attributes. If so, the 'doubtful' segments will be automatically checked and divided into a subset that has passed the automatic attribute check and a subset that hasn't. The passed subset is conflated for sure. The failed subset will only pass if you have chosen to check them manually and they pass the manual check.
* The final fields allow you to select the specific attributes for which the segments should be automatically checked and merged. The minimum date, the minimum version and the minimum number of attributes can be specified here. If an attribute meets all the minimum requirements, it is likely to be trustworthy and will be conflated automatically without manual checking. The idea behind this is that the more attributes a segment has, the more up-to-date a segment is, and the higher the version of a segment, the higher the data quality of that segment tends to be. These high quality segments don't need to be checked manually and can be used immediately.

The decision tree can give you a better overview of the process.

<img src="https://i.imgur.com/alJ3HgC.png" alt="decisiontree" width="600"/>


So in a more practical context that means:
* If you know the study area very well, the most accurate option is to check all segments manually (without automatic attribute checks) and decide if you want to conflate them and transfer them to the new dataset, but this is also the most time consuming one.
* The most straight forward option is to conflate every segment without any automatic attribute check or manual check. However, there is also the risk of having errors of commission, meaning that segments are transfered that may not exist.
* The most pragmatic and recommended option is to check the "doubtful" segments manually, but automatically conflate and transfer a subset of segments. With this option you reduce the amount of segments to check and conflate segments with a minimum of quality (based on their attributes) automatically and unchecked. 

## Aditional Notebooks

### Timeseries Cycle Network
The Timeseries Cycle Network notebook is an additional bonus notebook that allows you to create an animated gif image of the cycle network of any study area over time. It can create attractive animations showing the growth of the cycle network in the OSM data.
<img src="https://i.imgur.com/HB73o3U.gif" alt="drawing" width="600"/>

## Overview Data Usage at different Sections

All data is stored in dictionaries. This is a technical overview of which data is used in which section. If you are only using the notebook, this information is not important.

### Intrinsic Analysis

#### E1: First Overview of Study Area and Bicycle Infrastructure
* dict_cycle_tracks['gdf_xml']
* dict_cycle_lanes['gdf_xml']
* dict_calm_traffic_ways['gdf_xml']
* dict_own['gdf_xml']

* dict_total['graph']
* gs_edges dict_total['graph'] 

#### E2: History Analysis:
* gjson_area (study area in geojson) 
* oshome api

#### E3: Linus Law:
* dict_cycle_tracks['gdf_xml']
* dict_cycle_lanes['gdf_xml']
* dict_calm_traffic_ways['gdf_xml']
* dict_own['gdf_xml']

### Extrinsic Analysis

#### P3: Overview OSM:

* dict_osm_total['edges'], dict_osm_calm_traffic_ways['edges'], dict_osm_cycle_lanes['edges'], dict_osm_cycle_tracks['edges']

#### P4: Compare and Choose Model:

* dict_gip['radvis_turnuse']
* dict_gip['connected_radvise']

#### P4: Overview GIP:

* dict_gip['evaluate_model']

#### E1: Timestamp of last Edit (Uptodateness):

* OSM: dict_osm_total['gdf_xml_dt']
* GIP: dict_gip['radvis']

#### E2: Dangling Nodes:

* OSM: dict_osm_total['edges'] and dict_osm_total['nodes'] from dict_osm_total['graph'] (simplified, undirected)
* GIP: dict_gip['edges'] and dict_gip['nodes'] from dict_gip['graph'] (undirected)

#### E3: Component Analysis

* OSM: dict_osm_total['graph'] (undirected, simplification would dissolve original edges which are important for length)
* GIP: dict_gip['graph'] (undirected)

#### E4: Missing Links:  

* OSM: dict_osm_total['graph'] (undirected), edges from dict_total['graph']
* GIP: dict_gip['graph'] , edges from dict_gip['graph']

#### E5: Attribute Completness:

* OSM: dict_osm_total['gdf_xml']
* GIP: dict_gip['radvis']

#### E6: Length:

* OSM: dict_osm_total['gdf_xml'], dict_osm_calm_traffic_ways['gdf_xml'], dict_osm_cycle_lanes['gdf_xml'], dict_osm_cycle_tracks['gdf_xml']
* GIP: dict_gip['evaluate_model']

#### E7: Grid Based Length:

* OSM: dict_osm_total['gdf_xml']
* GIP: dict_gip['evaluate_model']

### Conflation

#### P5: Feature Matching:

* OSM: dict_osm_total['gdf_xml']
* GIP: dict_gip['connected_radvis']

#### E1: Feature Matching Results:

* OSM: osm_matched_segments, osm_unmatched_segments
* GIP: gip_matched_segments, gip_unmatched_segments

#### E1: Conflation:

* OSM: osm_matched_edges, osm_unmatched_edges
* GIP: gip_matched_edges, gip_unmatched_edges

## Licence Information
* [OpenStreetMap Contributers, ODBL](https://www.openstreetmap.org/copyright)
* [Intermodales Verkehrsreferenzsystem Österreich (GIP.at) Österreich, CC-BY 4.0](https://www.data.gv.at/katalog/dataset/3fefc838-791d-4dde-975b-a4131a54e7c5#resources)