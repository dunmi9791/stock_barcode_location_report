{
    "name": "Product Stock by Location Report",
    "version": "18.0.1.0.0",
    "summary": "Menu + printable report showing each product's barcode, "
                "quantity per storage location, and total quantity on hand.",
    "description": """
Adds a "Stock by Location" report under Inventory > Reporting.

The report is backed by a SQL view aggregating stock.quant by product and
internal location, so it opens instantly (no runtime computation) and works
out of the box with Odoo's Pivot view (Product rows x Location columns,
with automatic Total row/column) and List view. A "Print" report is also
available from the list view to produce a PDF grouped by product, showing
barcode, quantity per location, and the total quantity.
""",
    "category": "Inventory/Inventory",
    "author": "Custom",
    "license": "LGPL-3",
    "depends": ["stock", "product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_stock_by_location_views.xml",
        "report/product_stock_by_location_report.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
