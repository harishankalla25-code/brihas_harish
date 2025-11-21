import frappe
from frappe.model.document import Document

class Camera(Document):
    pass

def validate_camera(doc, method=None):
    if doc.installed_booth and doc.health_status == "Faulty":
        frappe.throw("You cannot assign a Faulty camera to a booth.")
