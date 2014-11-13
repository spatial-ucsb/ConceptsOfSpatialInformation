Core Concepts of Spatial Information - Objects Data
----------------------

Shapefiles used for PV site-suitability analysis for the CalPoly San Luis Obispo campus. Acquired from CalPoly Kennedy Library, January 2014.

The "Rooftops.shp" file was clipped from a building footprint shapefile from SLO County and reprojected (metadata below).

The "ViablePVArea.shp" file was digitized for the site-suitability analysis and represents regions of rooftops that meet structural and insolation requirements.

Metadata included below.

----------------------
Metadata for "Rooftops.shp" (prior to clipping and reprojecting):
----------------------

Identification_Information:

    Citation:

        Citation_Information:

            Originator: Joe Larson, CAL FIRE / San Luis Obispo County Fire
            Publication_Date: 20121018
            Title: Building Footprints
            Geospatial_Data_Presentation_Form: vector digital data

    Description:

        Abstract:
            This data layer is a snapshot extract of OpenStreetMap data, specifically 'ways' with 'building=*' tags from around the San Luis Obispo County area. It was created by digitizing against 2011 aerial imagery (best available resolution - 6 or 12 inch - depending on area) within the JOSM Editor. 
        Purpose:
            This data layer represents polygons of areas showing location of building/structure 'footprints'. 

    Spatial_Domain:

        Bounding_Coordinates:

            West_Bounding_Coordinate: -121.291305
            East_Bounding_Coordinate: -119.934034
            North_Bounding_Coordinate: 35.806691
            South_Bounding_Coordinate: 34.884896

    Keywords:

        Theme:

            Theme_Keyword_Thesaurus: None
            Theme_Keyword: buildings
            Theme_Keyword: footprints
            Theme_Keyword: structures

    Access_Constraints: None
    Use_Constraints:
        You are free to copy, distribute, transmit and adapt our data, as long as you credit OpenStreetMap and its contributors. If you alter or build upon our data, you may distribute the result only under the same licence. OpenStreetMap is open data, licensed under the Open Data Commons Open Database License (ODbL). 
    Data_Set_Credit: © OpenStreetMap contributors
    Native_Data_Set_Environment:
        Microsoft Windows 7 Version 6.1 (Build 7601) Service Pack 1; Esri ArcGIS 10.1.1.3143 

Spatial_Data_Organization_Information:

    Direct_Spatial_Reference_Method: Vector
    Point_and_Vector_Object_Information:

        SDTS_Terms_Description:

            SDTS_Point_and_Vector_Object_Type: GT-polygon composed of chains
            Point_and_Vector_Object_Count: 117392

Spatial_Reference_Information:

    Horizontal_Coordinate_System_Definition:

        Planar:

            Map_Projection:

                Map_Projection_Name: NAD 1983 StatePlane California V FIPS 0405 Feet
                Lambert_Conformal_Conic:

                    Standard_Parallel: 34.03333333333333
                    Standard_Parallel: 35.46666666666667
                    Longitude_of_Central_Meridian: -118.0
                    Latitude_of_Projection_Origin: 33.5
                    False_Easting: 6561666.666666666
                    False_Northing: 1640416.666666667

            Planar_Coordinate_Information:

                Planar_Coordinate_Encoding_Method: coordinate pair
                Coordinate_Representation:

                    Abscissa_Resolution: 0.0003280833333333334
                    Ordinate_Resolution: 0.0003280833333333334

                Planar_Distance_Units: foot_us

        Geodetic_Model:

            Horizontal_Datum_Name: D North American 1983
            Ellipsoid_Name: GRS 1980
            Semi-major_Axis: 6378137.0
            Denominator_of_Flattening_Ratio: 298.257222101

Entity_and_Attribute_Information:

    Detailed_Description:

        Entity_Type:

            Entity_Type_Label: BUILDING_FOOTPRINTS

        Attribute:

            Attribute_Label: OBJECTID
            Attribute_Definition: Internal feature number.
            Attribute_Definition_Source: ESRI
            Attribute_Domain_Values:

                Unrepresentable_Domain:
                    Sequential unique whole numbers that are automatically generated. 

        Attribute:

            Attribute_Label: osm_id

        Attribute:

            Attribute_Label: addr_floor

        Attribute:

            Attribute_Label: addr_postc

        Attribute:

            Attribute_Label: addr_city

        Attribute:

            Attribute_Label: addr_full

        Attribute:

            Attribute_Label: addr_house

        Attribute:

            Attribute_Label: addr_hou_1

        Attribute:

            Attribute_Label: addr_stree

        Attribute:

            Attribute_Label: addr_str_1

        Attribute:

            Attribute_Label: addr_str_2

        Attribute:

            Attribute_Label: addr_str_3

        Attribute:

            Attribute_Label: building

        Attribute:

            Attribute_Label: name

        Attribute:

            Attribute_Label: osm_user

        Attribute:

            Attribute_Label: osm_uid

        Attribute:

            Attribute_Label: osm_versio

        Attribute:

            Attribute_Label: osm_timest

        Attribute:

            Attribute_Label: Shape
            Attribute_Definition: Feature geometry.
            Attribute_Definition_Source: ESRI
            Attribute_Domain_Values:

                Unrepresentable_Domain: Coordinates defining the features.

        Attribute:

            Attribute_Label: Shape_STArea__

        Attribute:

            Attribute_Label: Shape_STLength__

        Attribute:

            Attribute_Label: Shape_Length
            Attribute_Definition: Length of feature in internal units.
            Attribute_Definition_Source: Esri
            Attribute_Domain_Values:

                Unrepresentable_Domain: Positive real numbers that are automatically generated.

        Attribute:

            Attribute_Label: Shape_Area
            Attribute_Definition: Area of feature in internal units squared.
            Attribute_Definition_Source: Esri
            Attribute_Domain_Values:

                Unrepresentable_Domain: Positive real numbers that are automatically generated.

Metadata_Reference_Information:

    Metadata_Date: 20121018
    Metadata_Contact:

        Contact_Information:

            Contact_Organization_Primary:

                Contact_Organization: CAL FIRE / San Luis Obispo County Fire
                Contact_Person: Joe Larson

    Metadata_Standard_Name: FGDC Content Standard for Digital Geospatial Metadata
    Metadata_Standard_Version: FGDC-STD-001-1998
    Metadata_Time_Convention: local time

----------------------
Metadata for "ViablePVArea.shp":
----------------------
<metadata>
  <idinfo>
    <citation>
      <citeinfo>
        <title>ViablePVArea</title>
        <geoform>vector digital data</geoform>
      </citeinfo>
    </citation>
    <spdom>
      <bounding>
        <westbc>-120.680387</westbc>
        <eastbc>-120.655126</eastbc>
        <northbc>35.311844</northbc>
        <southbc>35.297551</southbc>
      </bounding>
    </spdom>
    <accconst>None</accconst>
    <useconst>None</useconst>
    <native> Version 6.2 (Build 9200) ; Esri ArcGIS 10.2.0.3348</native>
  </idinfo>
  <spdoinfo>
    <direct>Vector</direct>
    <ptvctinf>
      <sdtsterm>
        <sdtstype>GT-polygon composed of chains</sdtstype>
        <ptvctcnt>246</ptvctcnt>
      </sdtsterm>
    </ptvctinf>
  </spdoinfo>
  <spref>
    <horizsys>
      <planar>
        <mapproj>
          <mapprojn>NAD 1983 2011 UTM Zone 10N</mapprojn>
          <transmer>
            <sfctrmer>0.9996</sfctrmer>
            <longcm>-123.0</longcm>
            <latprjo>0.0</latprjo>
            <feast>500000.0</feast>
            <fnorth>0.0</fnorth>
          </transmer>
        </mapproj>
        <planci>
          <plance>coordinate pair</plance>
          <coordrep>
            <absres>0.000000002220024164500956</absres>
            <ordres>0.000000002220024164500956</ordres>
          </coordrep>
          <plandu>meter</plandu>
        </planci>
      </planar>
      <geodetic>
        <horizdn>D NAD 1983 2011</horizdn>
        <ellips>GRS 1980</ellips>
        <semiaxis>6378137.0</semiaxis>
        <denflat>298.257222101</denflat>
      </geodetic>
    </horizsys>
  </spref>
  <eainfo>
    <detailed>
      <enttyp>
        <enttypl>ViablePVArea</enttypl>
      </enttyp>
      <attr>
        <attrlabl>FID</attrlabl>
        <attrdef>Internal feature number.</attrdef>
        <attrdefs>Esri</attrdefs>
        <attrdomv>
          <udom>Sequential unique whole numbers that are automatically generated.</udom>
        </attrdomv>
      </attr>
      <attr>
        <attrlabl>Shape</attrlabl>
        <attrdef>Feature geometry.</attrdef>
        <attrdefs>Esri</attrdefs>
        <attrdomv>
          <udom>Coordinates defining the features.</udom>
        </attrdomv>
      </attr>
      <attr>
        <attrlabl>SHAPE_Leng</attrlabl>
      </attr>
      <attr>
        <attrlabl>SHAPE_Area</attrlabl>
        <attrdef>Area of feature in internal units squared.</attrdef>
        <attrdefs>Esri</attrdefs>
        <attrdomv>
          <udom>Positive real numbers that are automatically generated.</udom>
        </attrdomv>
      </attr>
      <attr>
        <attrlabl>BuildingID</attrlabl>
      </attr>
    </detailed>
  </eainfo>
  <metainfo>
    <metd>20141112</metd>
    <metstdn>FGDC Content Standard for Digital Geospatial Metadata</metstdn>
    <metstdv>FGDC-STD-001-1998</metstdv>
    <mettc>local time</mettc>
  </metainfo>
</metadata>
