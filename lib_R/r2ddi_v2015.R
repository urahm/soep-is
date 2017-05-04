library("r2ddi")

dir2xml(
  path_in = "/home/soepdist/ddionrails/soep-is/v2015/en/",
  path_out = "r2ddi/v2015/en",
  missing_codes = -9:-1,
  my_cores = 30)

dir2xml(
  path_in = "/home/soepdist/ddionrails/soep-is/v2015/de/",
  path_out = "r2ddi/v2015/de/",
  missing_codes = -9:-1,
  my_cores = 30)
