from app.models.base_model import BaseModel
import time

obj = BaseModel()

print("ID:", obj.id)
print("Created at:", obj.created_at)
print("Updated at:", obj.updated_at)

time.sleep(1)
obj.update({"test_attr": "value"})  # n'existe pas → ignoré
print("Updated at after update:", obj.updated_at)
