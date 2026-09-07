# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

from ..services.arb_client import ARBClient


class AlRajhiARBController(http.Controller):
    """Handle ARB return callback (bank hosted redirect)."""

    @http.route(
        "/payment/alrajhi_arb/return",
        type="http",
        auth="public",
        methods=["GET"],
        sitemap=False,
    )
    def alrajhi_arb_return(self, **params):
        # ARB redirects with query params like: paymentId, trandata, error, errorText
        payment_id = params.get("paymentId") or params.get("PaymentID") or params.get("PaymentId")
        encrypted_trandata = params.get("trandata") or params.get("Trandata")
        error = params.get("error") or params.get("Error")
        error_text = params.get("errorText") or params.get("ErrorText")

        if not payment_id:
            raise ValidationError("Al Rajhi ARB: missing paymentId on return callback.")

        # Locate the transaction by gateway payment id to retrieve the right resource key.
        tx = request.env["payment.transaction"].sudo().search(
            [
                ("provider_code", "=", "alrajhi_arb"),
                ("provider_reference", "=", str(payment_id)),
            ],
            limit=1,
        )
        if not tx:
            raise ValidationError("Al Rajhi ARB: no transaction found for paymentId=%s" % payment_id)

        notification_data = {
            "payment_id": str(payment_id),
            "error": error,
            "error_text": error_text,
        }

        # Decrypt and extract result when trandata is provided.
        if encrypted_trandata:
            plain = ARBClient.decrypt_trandata(
                resource_key=tx.provider_id.arb_resource_key,
                encrypted_hex=encrypted_trandata,
            )
            # Plain trandata is expected to be a JSON array with a single object.
            if isinstance(plain, list) and plain:
                plain = plain[0]

            notification_data.update(
                {
                    "result": plain.get("result"),
                    "track_id": plain.get("trackId"),
                    "trans_id": plain.get("transId"),
                    "auth_resp_code": plain.get("authRespCode"),
                    "auth_code": plain.get("authCode"),
                    "card_type": plain.get("cardType"),
                }
            )

        request.env["payment.transaction"].sudo()._handle_notification_data(
            "alrajhi_arb",
            notification_data,
        )

        # Redirect the user to the standard Odoo landing route for the payment.
        return request.redirect(tx.landing_route or "/payment/status")

