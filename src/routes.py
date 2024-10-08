from src import api
from src.resourse.actors import ActorListApi
from src.resourse.aggregations import AggregationApi
from src.resourse.auth import AuthRegister, AuthLogin
from src.resourse.films import FilmListApi
from src.resourse.smoke import Smoke
from src.resourse.stuntmen import StuntmenApi


api.add_resource(Smoke, '/smoke', strict_slashes=False)
api.add_resource(FilmListApi, '/films', '/films/<uuid>',  strict_slashes=False)
api.add_resource(ActorListApi, '/actors', '/actors/<uuid>', strict_slashes=False)
api.add_resource(AggregationApi, '/aggregation', strict_slashes=False)
api.add_resource(StuntmenApi, '/stuntmen', strict_slashes=False)

api.add_resource(AuthRegister, '/register_it', strict_slashes=False)
print("AuthRegister resource registered.")

api.add_resource(AuthLogin, '/login_it', strict_slashes=False)
print("AuthLogin resource registered.")



