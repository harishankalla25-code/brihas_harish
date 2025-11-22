import frappe
from frappe.model.document import Document

class InstallationTask(Document):
    pass

def validate_installation_task(doc, method=None):

    booth = frappe.get_doc("Polling Booth", doc.booth)

    # Faulty camera check
    if doc.camera_id:
        cam = frappe.get_doc("Camera", doc.camera_id)
        if cam.health_status == "Faulty":
            frappe.throw(f"Camera {cam.name} is Faulty and cannot be installed.")

    # Completing checks
    if doc.workflow_state == "Completed":
        if not booth.power_available:
            frappe.throw("Cannot complete installation: Power not available.")

        if booth.network_strength == "Poor":
            frappe.throw("Cannot complete installation: Network strength is Poor.")

        if not doc.checklist_passed:
            frappe.throw("Checklist must be passed before marking Installation Task as Completed.")

# NEW: safe workflow move before save
def on_before_save(doc, method=None):

    booth = frappe.get_doc("Polling Booth", doc.booth)

    # Auto move to In Progress when both users assigned
    if doc.supervisor and doc.field_operator and doc.workflow_state == "Draft":
        doc.workflow_state = "In Progress"
        booth.db_set("status", "Surveyed")


def on_submit_installation_task(doc, method=None):

    booth = frappe.get_doc("Polling Booth", doc.booth)

    if not doc.checklist_passed:
        frappe.throw("Checklist must be passed before submitting Installation Task.")

    booth.db_set("status", "Installed")

    if doc.camera_id:
        cam = frappe.get_doc("Camera", doc.camera_id)
        cam.installed_booth = doc.booth
        cam.health_status = "Deployed"
        cam.save(ignore_permissions=True)

    frappe.msgprint("Booth and Cameras updated successfully.")
