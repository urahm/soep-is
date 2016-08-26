library("r2ddi")

dir2xml(
  path_in = "/home/soepdist/ddionrails/soep-is/v2013/en/",
  path_out = "r2ddi/v2013/en",
  missing_codes = -9:-1,
  my_cores = 30)

dir2xml(
  path_in = "/home/soepdist/ddionrails/soep-is/v2013/de/",
  path_out = "r2ddi/v2013/de/",
  missing_codes = -9:-1,
  my_cores = 30)
