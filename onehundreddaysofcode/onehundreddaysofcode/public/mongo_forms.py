from flask_mongoengine.wtf import model_form
from onehundreddaysofcode.public.mongo_models import RandomData

RandomForm = model_form(RandomData)
