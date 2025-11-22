import frappe
from frappe.model.document import Document

class PollingBooth(Document):
    pass

# Fires automatically on After Insert
def create_installation_task(doc, method=None):
    task = frappe.new_doc("Installation Task")
    task.booth = doc.name
    task.scheduled_date = frappe.utils.today()
    task.insert(ignore_permissions=True)

    frappe.msgprint(
        msg=f"Installation Task <b>{task.name}</b> created successfully for Booth <b>{doc.name}</b>.",
        title="Installation Task Created",
        indicator="green"
    )

# Manual button click
@frappe.whitelist()
def create_installation_task_manual(name):
    booth = frappe.get_doc("Polling Booth", name)

    task = frappe.new_doc("Installation Task")
    task.booth = booth.name
    task.scheduled_date = frappe.utils.today()
    task.insert(ignore_permissions=True)

    return task.name
