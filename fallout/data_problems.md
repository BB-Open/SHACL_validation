# Problems concerning the data

# Violation

### dct:accrualPeriodicity 

#### 1538 errors

```  
sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://geobasis-bb.de#dcat_Dataset_cc0c9b60-c433-4fab-bcc1-95e214e8d341> ;
                 sh:resultMessage              "dcat:Dataset: dct:accrualPeriodicity MUSS eine IRI aus diesem Vokabular verwenden: https://www.dcat-ap.de/def/dcatde/2.0/spec/#kv-frequency"@de ;
                 sh:resultPath                 dct:accrualPeriodicity ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:NodeConstraintComponent ;
                 sh:sourceShape                dcatde:Dataset_dct_accrualPeriodicity_v_List ;
                 sh:value                      <http://inspire.ec.europa.eu/metadata-codelist/MaintenanceFrequencyCode/notPlanned>
               ] ;
```

We need a mapping from inspire frequencies to http://publications.europa.eu/resource/authority/frequency/

Responsible for action: Inqbus, Iso2Dcat 

---

### adms:identifier

#### 8947 Errors

```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://geobasis-bb.de#dcat_Dataset_b55874a3-b480-4a32-8951-1ea649f4d0c7> ;
                 sh:resultMessage              "dcat:Dataset: adms:identifier MUSS auf einen adms:Identifier verweisen."@de ;
                 sh:resultPath                 adms:identifier ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:ClassConstraintComponent ;
                 sh:sourceShape                dcatde:Dataset_adms_identifier_v_Class ;
                 sh:value                      "b55874a3-b480-4a32-8951-1ea649f4d0c7"
               ] ;
```

We have to use a real adms:Identifier structure.

Responsible for action: Inqbus, Iso2Dcat

---


### dcat:theme

#### 5621 Errors

```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://geobasis-bb.de#dcat_Dataset_9fdfaf31-d4b0-42a2-bb95-9b088fffc06a> ;
                 sh:resultMessage              "dcat:Dataset: dcat:theme MUSS eine IRI aus diesem Vokabular verwenden: https://www.dcat-ap.de/def/dcatde/2.0/spec/#kv-data-theme"@de ;
                 sh:resultPath                 dcat:theme ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:NodeConstraintComponent ;
                 sh:sourceShape                dcatde:Dataset_dcat_theme_v_List ;
                 sh:value                      <http://inspire.ec.europa.eu/theme/lc>
               ] ;
```

There is a ToDo on the shape file which will fix this in the future

Responsible for action: GovData, fix shapes

---

### dct:issued, dct:modified

#### 8916 + 8936 errors

```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://geobasis-bb.de#dcat_Dataset_93ffb51f-4a21-4843-8f3e-b86f65dea86e> ;
                 sh:resultMessage              "dcat:Dataset: dct:issued MUSS ein als xsd:date, xsd:dateTime, xsd:gYear oder xsd:gYearMonth getyptes Literal sein. Es DARF maximal einmal vorhanden sein."@de ;
                 sh:resultPath                 dct:issued ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:NodeConstraintComponent ;
                 sh:sourceShape                dcatap:Dataset_Property_dct_issued ;
                 sh:value                      "2022-11-17T09:42:12.214313"^^xsd:dateTimeStamp
               ] ;
```

xsd:dateTimeStamp problem 

Responsible for action: GovData/EU, fix shapes

---

### dcat:dataset

#### 180 errors

```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://geobasis-bb.de#dcat_Catalog> ;
                 sh:resultMessage              "dcat:Catalog: dcat:dataset MUSS auf ein dcat:Dataset verweisen."@de ;
                 sh:resultPath                 dcat:dataset ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:ClassConstraintComponent ;
                 sh:sourceShape                dcatde:Catalog_dcat_dataset_v_Class ;
                 sh:value                      <https://geobasis-bb.de#dcat_DataService_a6dfdfe2-9f6c-442e-9256-cadf8d8cf5e0>
               ] ;
```

This is an issue with the GovData shapes. They know nothing about dcat:DataService 

Responsible for action: GovData/EU, fix shapes

---

### dcat:servesDataset
#### 41 errors

```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://gl.berlin-brandenburg.de#dcat_DataService_16aa5330-99bb-43b6-9f3a-69866f4b8a57> ;
                 sh:resultMessage              "dcat:DataService: dcat:servesDataset MUSS auf ein dcat:Dataset verweisen."@de ;
                 sh:resultPath                 dcat:servesDataset ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:ClassConstraintComponent ;
                 sh:sourceShape                dcatde:DataService_dcat_servesDataset_v_Class ;
                 sh:value                      <http://lgb.de#dcat_Dataset_054fe546-0e93-4f88-aa8a-01e90248329d>
               ] ;
```

Inconsistent Data. Dataset is linked, but not created in store.

Responsible for action: Inqbus, fix dataset creation

---

### dcat:downloadURL, dcat:accessURL


#### 90 + 91 errors

```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://service.brandenburg.de/service/de/adressen/kommunalverzeichnis/tierfunde_pflegestationen.csv> ;
                 sh:resultMessage              "dcat:Distribution: dcat:downloadURL MUSS eine IRI oder BlankNode sein."@de ;
                 sh:resultPath                 dcat:downloadURL ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:NodeKindConstraintComponent ;
                 sh:sourceShape                dcatap:Distribution_Property_dcat_downloadURL ;
                 sh:value                      "https://service.brandenburg.de/service/de/adressen/kommunalverzeichnis/tierfunde_pflegestationen.csv"
               ] ;
```
URI in quotes ... Educate BBG

Responsible for action: BBG, fix data

<https://service.brandenburg.de/service/de/adressen/kommunalverzeichnis/tierfunde_pflegestationen.csv>
<http://www.w3.org/ns/dcat#downloadURL>
"https://service.brandenburg.de/service/de/adressen/kommunalverzeichnis/tierfunde_pflegestationen.csv"

to

<https://service.brandenburg.de/service/de/adressen/kommunalverzeichnis/tierfunde_pflegestationen.csv>
<http://www.w3.org/ns/dcat#downloadURL>
<https://service.brandenburg.de/service/de/adressen/kommunalverzeichnis/tierfunde_pflegestationen.csv>

---

### dct:format

#### 90 errors

```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://service.brandenburg.de/service/de/adressen/kommunalverzeichnis/frauenhaeuser.csv> ;
                 sh:resultMessage              "dcat:Distribution: dct:format MUSS eine IRI aus diesem Vokabular verwenden: https://www.dcat-ap.de/def/dcatde/2.0/spec/#kv-file-type"@de ;
                 sh:resultPath                 dct:format ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:NodeConstraintComponent ;
                 sh:sourceShape                dcatde:Distribution_dct_format_v_List ;
                 sh:value                      "text/csv"@de
               ] ;
```

Needs to be from vocabulary.

Responsible for action: BBG, fix data

---

### dct:identifier
#### 67 errors

```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://service.brandenburg.de/service/de/adressen/weitere-verzeichnisse/verzeichnisliste/~forstwirtschaft-sachverstaendige> ;
                 sh:resultMessage              "dcat:Dataset: dct:identifier MUSS ein Literal sein."@de ;
                 sh:resultPath                 dct:identifier ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:NodeKindConstraintComponent ;
                 sh:sourceShape                dcatap:Dataset_Property_dct_identifier ;
                 sh:value                      <https://service.brandenburg.de/service/de/adressen/weitere-verzeichnisse/verzeichnisliste/~forstwirtschaft-sachverstaendige>
               ] ;
```

Identifier is not an IRI.

Responsible for action: BBG, fix data

### dcat:Datase dct:description
#### 12 errors

---

```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://backend.datenadler.de/harvester-intern/service-brandenburg/metadaten/dcat_catalog/behoerdenverzeichnis> ;
                 sh:resultMessage              "dcat:Dataset: dct:description MUSS vorhanden und ein Literal sein."@de ;
                 sh:resultPath                 dct:description ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:MinCountConstraintComponent ;
                 sh:sourceShape                dcatap:Dataset_Property_dct_description
               ] ;
```

Missing description

Responsible for action: BBG, fix data and Inqbus, make description required (easy fix)

---

### dcatde:Catalog_dcat_themeTaxonomy_v_Fixed

#### 13 errors

```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://lbgr.brandenburg.de#dcat_Catalog> ;
                 sh:resultMessage              "dcat:Catalog: dcat:themeTaxonomy MUSS, wenn sie verwendet wird, einmal auf http://publications.europa.eu/resource/authority/data-theme zeigen."@de ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:OrConstraintComponent ;
                 sh:sourceShape                dcatde:Catalog_dcat_themeTaxonomy_v_Fixed ;
                 sh:value                      <https://lbgr.brandenburg.de#dcat_Catalog>
               ] ;
```

Responsible for action: data provider, fix data


### dcatde:Distribution_dct_license_w_List

#### 4 errors

```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://opendata.bbnavi.de/barshare/car/gbfs.json> ;
                 sh:resultMessage              "dcat:Distribution: dct:license SOLL folgendes Vokabular benutzten: https://www.dcat-ap.de/def/licenses/"@de ;
                 sh:resultPath                 dct:license ;
                 sh:resultSeverity             sh:Warning ;
                 sh:sourceConstraintComponent  sh:NodeConstraintComponent ;
                 sh:sourceShape                dcatde:Distribution_dct_license_w_List ;
                 sh:value                      <https://creativecommons.org/publicdomain/zero/1.0/>
               ] ;
```

License mismatch

Responsible for action: data provider, fix data

---


### dcatde:Dataset_dct_language_v_List

#### 1 error

```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://backend.datenadler.de/harvester-intern/afs/metadaten/dcat_catalog> ;
                 sh:resultMessage              "dcat:Dataset: dct:language MUSS eine IRI aus diesem Vokabular verwenden: https://www.dcat-ap.de/def/dcatde/2.0/spec/#kv-languages"@de ;
                 sh:resultPath                 dct:language ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:NodeConstraintComponent ;
                 sh:sourceShape                dcatde:Dataset_dct_language_v_List ;
                 sh:value                      "de"
               ] ;
```

Wrong lang information. Literal instead of URI.

Responsible for action: Inqbus, fix backend
<https://backend.datenadler.de/harvester-intern/afs/metadaten/dcat_catalog>
<http://purl.org/dc/terms/language>
"de"

to

<https://backend.datenadler.de/harvester-intern/afs/metadaten/dcat_catalog>
<http://purl.org/dc/terms/language>
<http://publications.europa.eu/resource/authority/language/DEU>


---

# Warning

### dct:Location

#### 9094 Warnings


```
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://geobasis-bb.de#dct_Location_d10b04c6-80e3-4a84-8099-fde187cb15cd> ;
                 sh:resultMessage              "dct:Location: SOLL eine der folgenden Eigenschaften nutzen: dcat:bbox, dcat:centroid, locn:geometry. Wenn Sie eine davon abweichende Eigenschaften nutzen, können Sie den Fehler ignorieren."@de ;
                 sh:resultSeverity             sh:Warning ;
                 sh:sourceConstraintComponent  sh:OrConstraintComponent ;
                 sh:sourceShape                dcatde:Location_locations_v_Min ;
                 sh:value                      <https://geobasis-bb.de#dct_Location_d10b04c6-80e3-4a84-8099-fde187cb15cd>
               ] ;
```

We point to a dct:Location. This is IMHO correct

Responsible for action: GovData/EU, fix shapes