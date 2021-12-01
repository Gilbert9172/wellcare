from flask import request
from flask_restx import Resource, Api, Namespace, fields
Root = Namespace(
    name="Root",
    description="Root API"
)

# API import
from . import save_Fatigue
from . import save_Common
from . import save_Agree
from . import save_Nutrition
from . import save_Cognitive
from . import save_Mental
from . import save_Stress
from . import save_Stomach
from . import save_Sleep
from . import save_Samkim
from . import info
from . import upload
from . import all_check
from . import checklist
from . import modified_checklist
from . import checklist_check