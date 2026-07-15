from odoo import fields, models, tools


class ProductStockByLocationReport(models.Model):
    """Read-only reporting model backed by a SQL view: one row per
    product / internal location with the on-hand quantity. Lots/packages
    at the same product+location are summed. Meant to be browsed via the
    Pivot view (Product rows x Location columns) which gives per-location
    quantities *and* automatic row/column totals for free.
    """

    _name = "product.stock.by.location.report"
    _description = "Product Stock by Location"
    _auto = False
    _order = "product_id, location_id"

    product_id = fields.Many2one("product.product", string="Product", readonly=True)
    product_tmpl_id = fields.Many2one("product.template", string="Product Template", readonly=True)
    barcode = fields.Char(string="Barcode", readonly=True)
    default_code = fields.Char(string="Internal Reference", readonly=True)
    location_id = fields.Many2one("stock.location", string="Location", readonly=True)
    warehouse_id = fields.Many2one("stock.warehouse", string="Warehouse", readonly=True)
    quantity = fields.Float(string="Quantity", readonly=True)
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure", readonly=True)
    company_id = fields.Many2one("res.company", string="Company", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    row_number() OVER (ORDER BY grouped.product_id, grouped.location_id) AS id,
                    grouped.*
                FROM (
                    SELECT
                        sq.product_id AS product_id,
                        pp.product_tmpl_id AS product_tmpl_id,
                        pp.barcode AS barcode,
                        pp.default_code AS default_code,
                        sq.location_id AS location_id,
                        sl.warehouse_id AS warehouse_id,
                        SUM(sq.quantity) AS quantity,
                        pt.uom_id AS uom_id,
                        sq.company_id AS company_id
                    FROM stock_quant sq
                    JOIN product_product pp ON pp.id = sq.product_id
                    JOIN product_template pt ON pt.id = pp.product_tmpl_id
                    JOIN stock_location sl ON sl.id = sq.location_id
                    WHERE sl.usage = 'internal'
                      AND pt.is_storable = true
                    GROUP BY
                        sq.product_id, pp.product_tmpl_id, pp.barcode, pp.default_code,
                        sq.location_id, sl.warehouse_id, pt.uom_id, sq.company_id
                    HAVING SUM(sq.quantity) != 0
                ) grouped
            )
        """ % self._table)
