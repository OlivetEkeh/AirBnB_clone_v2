from models.place import Place, place_amenity
from models.amenity import Amenity
from models.review import Review
from models.engine.db_storage import DBStorage

# Create an instance of DBStorage
db_storage = DBStorage()

# Call the all method with no class specified
print("All objects:")
all_objects = db_storage.all()
for obj_key, obj in all_objects.items():
    print(obj_key, obj)

# Call the all method with a specific class (e.g., Amenity)
print("Amenity objects:")
amenity_objects = db_storage.all(Amenity)
for obj_key, obj in amenity_objects.items():
    print(obj_key, obj)
