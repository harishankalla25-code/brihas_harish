import frappe
from frappe.model.document import Document
from frappe.model.workflow import apply_workflow

class InstallationTask(Document):
    pass


def validate_installation_task(doc, method=None):

    booth = frappe.get_doc("Polling Booth", doc.booth)

    # 1) Block faulty cameras
    if doc.camera_id:
        cam = frappe.get_doc("Camera", doc.camera_id)
        if cam.health_status == "Faulty":
            frappe.throw(f"Camera {cam.name} is Faulty and cannot be installed.")

    # 2) Auto move to In Progress when Supervisor + Field Operator set
    if doc.supervisor and doc.field_operator:
        if doc.workflow_state == "Draft":
            # Trigger Workflow Transition
            apply_workflow(doc, "Start Installation")

            # Update Booth Status → Surveyed
            booth.db_set("status", "Surveyed")

    # 3) Validate before completing Installation
    if doc.workflow_state == "Completed":

        # booth must have power
        if not booth.power_available:
            frappe.throw("Cannot complete installation: Power not available.")

        # booth must have at least fair/good network
        if booth.network_strength == "Poor":
            frappe.throw("Cannot complete installation: Network strength is Poor.")

        # checklist must be passed
        if not doc.checklist_passed:
            frappe.throw("Checklist must be passed before marking Installation Task as Completed.")
            


def on_submit_installation_task(doc, method=None):

    booth = frappe.get_doc("Polling Booth", doc.booth)

    if not doc.checklist_passed:
        frappe.throw("Checklist must be passed before submitting Installation Task.")

    # Booth becomes Installed
    booth.db_set("status", "Installed")

    # Update the camera mentioned in the task
    if doc.camera_id:
        cam = frappe.get_doc("Camera", doc.camera_id)
        cam.installed_booth = doc.booth
        cam.health_status = "Deployed"
        cam.save(ignore_permissions=True)

    frappe.msgprint("Booth and Cameras updated successfully.")
