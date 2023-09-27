## MGM Evaluation

This repository contains various Python scripts to run MGM evaluation tests, which typically take the MGM output associated with a media file and compare it with the ground-truth associated with the same media. Various criteria specific to each category of MGMs are used to calculate the performance metrics. In addition to performance metrics, the scripts provide output comparisons between the ground-truth and MGM output that allow a user to scan to see differences.

Upon request from the user in the AMP UI, the MGM evaluation tests are run by AMP REST backend. Test results are returned in JSON format and the results are presented in the AMP UI in the form of bar charts and data tables to facilitate evaluation.

Further information on how to install, config, run, as well as contribute to the AMP project can be found at [AMP Bootstrap](https://github.com/AudiovisualMetadataPlatform/amp_bootstrap)
