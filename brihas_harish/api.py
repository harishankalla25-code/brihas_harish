import frappe

@frappe.whitelist(allow_guest=False)
def ready_booths(district=None, lac=None):
    filters = {}

    if district:
        filters["district"] = district

    if lac:
        filters["lac"] = lac

    booths = frappe.get_all(
        "Polling Booth",
        filters=filters,
        fields=[
            "name",
            "booth_id",
            "booth_name",
            "district",
            "lac",
            "power_available",
            "network_strength",
            "status",
            "address"
        ],
        order_by="booth_id asc"
    )

    return {
        "success": True,
        "count": len(booths),
        "data": booths
    }
