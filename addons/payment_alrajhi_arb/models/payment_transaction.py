# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import ValidationError

from ..services.arb_client import ARBClient


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _get_specific_processing_values(self, processing_values):
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != "alrajhi_arb":
            return res

        if self.operation != "online_redirect":
            # For now, implement only bank-hosted redirect payments.
            return res

        # Mark transaction as pending before redirecting customer.
        if self.state == "draft":
            self._set_pending()

        base_url = self._get_base_url()
        callback_url = f"{base_url}/payment/alrajhi_arb/return"

        payment_id, payment_page_base = ARBClient.create_payment_token(
            provider=self.provider_id,
            track_id=str(self.id),  # Numeric Merchant unique reference.
            amount=self.amount,
            response_url=callback_url,
            error_url=callback_url,
            action_code="1",  # Purchase
            langid="ar",
        )

        # Save gateway payment id to reliably locate the transaction on return.
        # Use write() so it is persisted before the user is redirected.
        self.write({"provider_reference": str(payment_id)})

        # The gateway returns a base payment page URL and expects us to append PaymentID.
        payment_url = self._frame_arb_payment_url(payment_id, payment_page_base)
        return {
            **res,
            "arb_payment_url": payment_url,
        }

    def _get_specific_rendering_values(self, processing_values):
        rendering_values = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != "alrajhi_arb":
            return rendering_values

        return {
            **rendering_values,
            "payment_url": processing_values.get("arb_payment_url"),
        }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        if provider_code != "alrajhi_arb":
            return super()._get_tx_from_notification_data(provider_code, notification_data)

        payment_id = notification_data.get("payment_id")
        track_id = notification_data.get("track_id")

        domain = [("provider_code", "=", "alrajhi_arb")]
        if payment_id:
            domain.append(("provider_reference", "=", str(payment_id)))
        elif track_id:
            domain.append(("id", "=", int(track_id)))
        else:
            raise ValidationError("Al Rajhi ARB: missing payment_id/track_id in callback payload.")

        tx = self.search(domain, limit=1)
        if not tx:
            raise ValidationError("Al Rajhi ARB: transaction not found for callback payload.")
        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != "alrajhi_arb":
            return

        result = notification_data.get("result")
        error_text = notification_data.get("error_text") or notification_data.get("error") or ""

        if notification_data.get("payment_id"):
            self.provider_reference = str(notification_data["payment_id"])

        if result in ("CAPTURED", "APPROVED"):
            self._set_done(state_message="ARB result=%s" % result)
        else:
            self._set_error(state_message=error_text or "ARB payment failed (no result).")

    def _get_base_url(self):
        """Compute absolute base URL (web base url preferred)."""
        icp = self.env["ir.config_parameter"].sudo()
        return icp.get_param("web.base.url", default="").rstrip("/")

    @staticmethod
    def _frame_arb_payment_url(payment_id, payment_page_base):
        """Append PaymentID query param to ARB's base payment page URL."""
        if "?" in payment_page_base:
            return f"{payment_page_base}&PaymentID={payment_id}"
        return f"{payment_page_base}?PaymentID={payment_id}"

