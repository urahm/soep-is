#!/usr/bin/Rscript

# this is for running on server stone

library("r2ddi")

dir2xml(
  path_in = "/rdc-prod/distribution/soep-is/doi10.5684/soep.is.2017/additional_and_unzipped_files/soep-is.2017_stata_de/",
  path_out = "r2ddi/v2017.0/en",
  missing_codes = -9:-1,
  my_cores = 30)
