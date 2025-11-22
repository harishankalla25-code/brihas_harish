import frappe
from frappe.model.document import Document

class PollingBooth(Document):
    pass

def create_installation_task(doc, method):
    task = frappe.new_doc("Installation Task")
    task.booth = doc.name
    task.scheduled_date = frappe.utils.today()
    task.insert(ignore_permissions=True)

    frappe.msgprint(
        msg=f"Installation Task <b>{task.name}</b> created successfully for Booth <b>{doc.name}</b>.",
        title="Installation Task Created",
        indicator="green"
    )

@frappe.whitelist()
def create_installation_task(name):
    booth = frappe.get_doc("Polling Booth", name)

    task = frappe.new_doc("Installation Task")
    task.booth = booth.name
    task.scheduled_date = frappe.utils.today()
    task.insert(ignore_permissions=True)

    return task.name
