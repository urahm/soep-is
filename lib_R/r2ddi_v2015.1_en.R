library("r2ddi")

dir2xml(
  path_in = "/home/soepdist/ddionrails/soep-is/v2015.1/en/",
  path_out = "r2ddi/v2015.1/en",
  missing_codes = -9:-1,
  my_cores = 30)
