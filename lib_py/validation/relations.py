from pprint import pprint

from datapackage import Package
from tableschema.exceptions import RelationError

package = Package('metadata/datapackage.json')

dataset_resource = package.get_resource('datasets')
variable_resource = package.get_resource('variables')

# pprint(dataset_resource.read(keyed=True, relations=True))

analysis_units = package.get_resource('analysis_units').read(keyed=True)
# pprint(analysis_units)

result = dataset_resource.check_relations()
result = variable_resource.check_relations()
