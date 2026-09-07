# Odoo REST API Integration - Testing Guide

This guide explains how to test the new API Integration features (Configuration & Target Models).

## Prerequisites
1.  Restart your Odoo service to load the new code.
2.  Update the `rest_api_odoo` module:
    *   Go to **Apps**.
    *   Search for `rest_api_odoo`.
    *   Click **Upgrade**.

## 1. Test API Configuration (Task #2)

This step verifies that Odoo can connect to an external Odoo instance (or itself) and authenticate using the Bearer Token mechanism.

1.  Navigate to **Rest API** > **Configuration** > **Add Connection**.
2.  Click **New**.
3.  Fill in the connection details:
    *   **Connection Name**: `Localhost Test` (or any name)
    *   **Server URL**: `http://localhost` (or the IP of the target Odoo)
    *   **Server Port**: `8069` (default is 8069)
    *   **Database Name**: `Motabaqah` (Target Database Name)
    *   **Database Username**: `admin`
    *   **Database Password**: `admin` (or your password)
4.  Click the **Test Connection** button.
5.  **Verification**:
    *   Check the **Result** tab.
    *   You should see `Connection Successful` and the JSON response containing the `api-key`.
    *   The **API Key** field on the form should be automatically populated.

## 2. Test Target Models (Task #3 & Core Logic)

This step verifies that Odoo can perform CRUD operations (GET, POST, PUT, DELETE) on the external Odoo instance using the configured connection.

### Test A: GET Request (Fetch Records)
1.  Navigate to **Rest API** > **Target Models** > **Models**.
2.  Click **New**.
3.  Fill in the details:
    *   **Model Name**: `res.users` (or `res.partner`)
    *   **Connection**: Select the `Localhost Test` connection created above.
    *   **Method**: `GET`
    *   **Selected Fields**: `["id", "name", "login"]`
4.  Click **Test Request**.
5.  **Verification**:
    *   Check the **Result** tab.
    *   You should see `Request Successful` and a list of records in JSON format.

### Test B: POST Request (Create Record)
*Note: This creates a real record on the target database.*
1.  Create a new Target Model record.
2.  **Model Name**: `res.partner`
3.  **Connection**: `Localhost Test`
4.  **Method**: `POST`
5.  **Selected Fields**: `["id", "name"]` (Fields to return after creation)
6.  *Note: The current implementation sends the `selected_fields` in the body. Ensure your target API endpoint expects specific values for creation if needed. The current test just triggers the endpoint.*
7.  Click **Test Request**.
8.  **Verification**:
    *   Check the **Result** tab for a success message/created ID.

### Test C: PUT/DELETE
*   Follow similar steps, selecting `PUT` or `DELETE` methods. 
*   *Note: For PUT/DELETE, the API usually requires a specific ID logic which is handled by the `send_request` endpoint logic you provided (using `model` and `id`). The current simple Test button sends a generic request.*
