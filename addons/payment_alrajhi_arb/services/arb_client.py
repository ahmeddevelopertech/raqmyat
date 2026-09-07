# -*- coding: utf-8 -*-

import json
import logging
from urllib.parse import quote_plus, unquote_plus

import requests
from odoo.exceptions import UserError




class ARBClient:
    """Minimal ARB REST client + trandata AES encrypt/decrypt utilities.

    Encryption/Decryption rules extracted from:
    "Sample Encryption and Decryption Code For JAVA/JAVASCRIPT" in the provided ARB PDF.
    """

    AES_IV = "PGKEYENCDECIVSPC"
    CURRENCY_CODE_SAR = "682"

    @staticmethod
    def _require_crypto():
        try:
            from Crypto.Cipher import AES  # noqa: F401
            from Crypto.Util.Padding import pad, unpad  # noqa: F401

            return AES, pad, unpad
        except Exception as e:
            raise UserError(
                "Al Rajhi ARB: missing crypto dependency. "
                "Please ensure PyCryptodome is installed in the Odoo environment (%s)." % e
            )

    @classmethod
    def encrypt_trandata(cls, resource_key: str, plain_text: str) -> str:
        """Encrypt plain JSON (URL-encoded before encryption) into ARB encryptedHex."""

        AES, pad, _unpad = cls._require_crypto()
        key_bytes = (resource_key or "").encode("utf-8")
        iv_bytes = cls.AES_IV.encode("utf-8")

        # ARB requires URL Encoder before encrypting.
        encoded = quote_plus(plain_text, safe="")
        data = encoded.encode("utf-8")
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        # ARB sample (Java) returns HEX string uppercase.
        return ciphertext.hex().upper()

    @classmethod
    def decrypt_trandata(cls, resource_key: str, encrypted_hex: str):
        """Decrypt ARB encryptedHex and return decoded JSON (object/list)."""

        AES, _pad, unpad = cls._require_crypto()
        encrypted_hex = unquote_plus(str(encrypted_hex or "").strip())
        ciphertext = bytes.fromhex(encrypted_hex)

        key_bytes = (resource_key or "").encode("utf-8")
        iv_bytes = cls.AES_IV.encode("utf-8")
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        padded = cipher.decrypt(ciphertext)
        plain_encoded = unpad(padded, AES.block_size).decode("utf-8")

        # ARB requires URL Decoder after decryption.
        plain_json = unquote_plus(plain_encoded)
        try:
            return json.loads(plain_json)
        except Exception:
            # Some ARB flows might return a non-JSON string; keep raw.
            return plain_json

    @classmethod
    def get_customer_ip_header(cls) -> str:
        """Return an X-FORWARDED-FOR compatible value for ARB risk checks."""

        # NOTE: This helper assumes it is executed inside an HTTP request context.
        # For background jobs, we fall back to empty string.
        try:
            from odoo.http import request as odoo_request

            headers = odoo_request.httprequest.headers
            xff = headers.get("X-FORWARDED-FOR")
            if xff:
                # ARB needs the customer's IP first.
                return xff.split(",")[0].strip()
            return odoo_request.httprequest.remote_addr or ""
        except Exception:
            return ""

    @classmethod
    def _choose_endpoint(cls, provider) -> str:
        """Pick sandbox/live endpoint based on payment.provider.state."""

        if getattr(provider, "state", None) == "test":
            return provider.arb_endpoint_url_test or ""
        return provider.arb_endpoint_url_prod or ""

    @classmethod
    def create_payment_token(
        cls,
        *,
        provider,
        track_id: str,
        amount: float,
        response_url: str,
        error_url: str,
        action_code: str = "1",
        langid: str = "ar",
    ):
        """Call ARB Payment Token Generation API and return (payment_id, payment_page_url)."""

        endpoint = cls._choose_endpoint(provider)
        if not endpoint:
            raise UserError("Al Rajhi ARB: missing endpoint URL configuration on the provider.")

        plain_trandata = json.dumps(
            [
                {
                    "amt": f"{amount:.2f}",
                    "action": str(action_code),
                    "password": provider.arb_tranportal_password,
                    "id": provider.arb_tranportal_id,
                    "currencyCode": cls.CURRENCY_CODE_SAR,
                    "trackId": str(track_id),
                    "responseURL": response_url,
                    "errorURL": error_url,
                    "langid": langid,
                }
            ],
            separators=(",", ":"),
        )
        encrypted_trandata = cls.encrypt_trandata(provider.arb_resource_key, plain_trandata)

        payload = [
            {
                "id": provider.arb_tranportal_id,
                "trandata": encrypted_trandata,
                "responseURL": response_url,
                "errorURL": error_url,
            }
        ]

        headers = {
            "Content-Type": "application/json",
            # Mandatory header for risk checks.
            "X-FORWARDED-FOR": cls.get_customer_ip_header(),
        }
        _logger = logging.getLogger(__name__)
        _logger.info("Al Rajhi ARB: sending token generation request to %s", endpoint)
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()

        # data = resp.json()
        
        _logger = logging.getLogger(__name__)

        _logger.info("ARB API Status Code: %s", resp.status_code)
        _logger.info("ARB API Response Content: %s", resp.text)

        try:
            data = resp.json()
        except Exception as e:
            _logger.error("Failed to decode JSON. Raw response was: %s", resp.text)
            raise e
        
        
        
        if not isinstance(data, list) or not data:
            raise UserError("Al Rajhi ARB: unexpected token generation response format.")

        first = data[0]
        status = str(first.get("status") or "")
        if status != "1":
            err = first.get("error") or ""
            err_txt = first.get("errorText") or first.get("error_text") or ""
            msg = "Al Rajhi ARB: token generation failed (%s - %s)" % (err, err_txt)
            blob = ("%s %s" % (err, err_txt)).upper()
            if "IPAY0200025" in blob or "TERMINAL" in blob:
                msg += (
                    " - Al Rajhi reports a terminal/configuration problem: re-check Tranportal ID, "
                    "password, and resource key (exactly as in the merchant pack), use the UAT "
                    "token URL only in Test mode (production URL for live), and ask the bank if "
                    "the terminal is active and whether your server outbound IP must be whitelisted."
                )
            raise UserError(msg)

        # result = "<paymentId>:<paymentPageBaseUrl>"
        result = first.get("result")
        if not result:
            raise UserError("Al Rajhi ARB: token generation succeeded but result is missing.")

        payment_id, payment_page_base = str(result).split(":", 1)
        return payment_id, payment_page_base
