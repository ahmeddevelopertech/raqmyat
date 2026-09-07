# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("alrajhi_arb", "Al Rajhi Bank (ARB) - KSA")],
        ondelete={"alrajhi_arb": "set default"},
    )

    arb_tranportal_id = fields.Char(
        string="Tranportal ID",
        required_if_provider="alrajhi_arb",
    )
    arb_tranportal_password = fields.Char(
        string="Tranportal Password",
        required_if_provider="alrajhi_arb",
    )
    arb_resource_key = fields.Char(
        string="Resource Key",
        required_if_provider="alrajhi_arb",
    )

    arb_endpoint_url_test = fields.Char(
        string="Token Generation Endpoint (Test/UAT)",
        default="https://securepayments.alrajhibank.com.sa/pg/payment/tranportal.htm",
    )
    arb_endpoint_url_prod = fields.Char(
        string="Token Generation Endpoint (Production)",
        default="https://digitalpayments.alrajhibank.com.sa/pg/payment/tranportal.htm",
    )

    @api.model
    def _get_default_payment_method_codes(self):
        # ARB supports card payments through its bank-hosted flow.
        return {"card"}

    def _get_redirect_form_view(self, is_validation=False):
        """Resolve the redirect template dynamically instead of storing a DB FK.

        This avoids upgrade issues when Odoo refreshes QWeb views and keeps the
        provider independent from a hard ``redirect_form_view_id`` relation.
        """
        self.ensure_one()
        if self.code != "alrajhi_arb":
            return super()._get_redirect_form_view(is_validation=is_validation)
        return self.env.ref("payment_alrajhi_arb.arb_redirect_form_view")

    def _get_removal_values(self):
        """Clear provider-specific fields cleanly when the module is removed."""
        values = super()._get_removal_values()
        if self.code == "alrajhi_arb":
            values.update(
                {
                    "redirect_form_view_id": False,
                    "arb_tranportal_id": False,
                    "arb_tranportal_password": False,
                    "arb_resource_key": False,
                }
            )
        return values

    def _should_build_inline_form(self, is_validation=False):
        # Bank-hosted ARB integration relies on redirects (payment page), not inline/direct payments.
        return False

