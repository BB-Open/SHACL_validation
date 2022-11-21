Problems concerning the data

### dct:accrualPeriodicity 

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

