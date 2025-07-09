# ai_website_generator/ai/__init__.py

# Expose the public generator functions to the rest of the application
from .generator import (
    ai_generate_master_plan,
    ai_generate_template,
    ai_generate_css,
    ai_write_design_doc,
    ai_fix_template,
)
