"""
generate_postman_collection.py
Generates AegisDesk_API_Collection.json — a Postman Collection v2.1 file
covering all AegisDesk REST API endpoints.

Run from the project root with the virtual environment activated:
    python generate_postman_collection.py
"""

import json
import uuid
import os

OUTPUT_FILE = "AegisDesk_API_Collection.json"


def build_collection() -> dict:
    """Build and return the Postman Collection v2.1 dict."""

    collection = {
        "info": {
            "name": "AegisDesk API Collection",
            "_postman_id": str(uuid.uuid4()),
            "description": "Pre-configured requests for all AegisDesk REST API endpoints.",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "variable": [
            {
                "key": "base_url",
                "value": "http://127.0.0.1:8000",
                "type": "string"
            },
            {
                "key": "access_token",
                "value": "",
                "type": "string"
            }
        ],
        "item": [
            _obtain_token_item(),
            _refresh_token_item(),
            _log_incident_authenticated_item(),
            _log_incident_unauthenticated_item(),
            _log_incident_missing_title_item(),
        ]
    }

    return collection


def _obtain_token_item() -> dict:
    """POST /incidents/api/token/ — obtain JWT access + refresh tokens."""
    return {
        "name": "Obtain JWT Token",
        "event": [
            {
                "listen": "test",
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        "var json = pm.response.json();",
                        "pm.collectionVars.set('access_token', json.access);"
                    ]
                }
            }
        ],
        "request": {
            "method": "POST",
            "header": [
                {"key": "Content-Type", "value": "application/json"}
            ],
            "body": {
                "mode": "raw",
                "raw": json.dumps({"username": "admin", "password": "password"})
            },
            "url": {
                "raw": "{{base_url}}/incidents/api/token/",
                "host": ["{{base_url}}"],
                "path": ["incidents", "api", "token", ""]
            },
            "description": "Obtain a JWT access and refresh token pair. The test script automatically stores the access token in the {{access_token}} collection variable."
        }
    }


def _refresh_token_item() -> dict:
    """POST /incidents/api/token/refresh/ — renew access token."""
    return {
        "name": "Refresh JWT Token",
        "request": {
            "method": "POST",
            "header": [
                {"key": "Content-Type", "value": "application/json"}
            ],
            "body": {
                "mode": "raw",
                "raw": json.dumps({"refresh": "{{refresh_token}}"})
            },
            "url": {
                "raw": "{{base_url}}/incidents/api/token/refresh/",
                "host": ["{{base_url}}"],
                "path": ["incidents", "api", "token", "refresh", ""]
            },
            "description": "Renew an access token using a valid refresh token."
        }
    }


def _log_incident_authenticated_item() -> dict:
    """POST /incidents/api/v1/log-incident/ — authenticated, valid payload (201)."""
    payload = {
        "title": "Test Incident",
        "description": "A test incident submitted via the API.",
        "severity": "medium",
        "affected_asset": "Web Server",
        "nist_stage": "detection"
    }
    return {
        "name": "Log Incident (Authenticated)",
        "request": {
            "method": "POST",
            "header": [
                {"key": "Authorization", "value": "Bearer {{access_token}}"},
                {"key": "Content-Type", "value": "application/json"}
            ],
            "body": {
                "mode": "raw",
                "raw": json.dumps(payload)
            },
            "url": {
                "raw": "{{base_url}}/incidents/api/v1/log-incident/",
                "host": ["{{base_url}}"],
                "path": ["incidents", "api", "v1", "log-incident", ""]
            },
            "description": "Submit a valid authenticated incident — expects 201 Created."
        }
    }


def _log_incident_unauthenticated_item() -> dict:
    """POST /incidents/api/v1/log-incident/ — no auth header (401)."""
    payload = {
        "title": "Unauthenticated Test",
        "description": "This request has no Authorization header.",
        "severity": "low",
        "affected_asset": "Unknown",
        "nist_stage": "detection"
    }
    return {
        "name": "Log Incident (Unauthenticated — expects 401)",
        "request": {
            "method": "POST",
            "header": [
                {"key": "Content-Type", "value": "application/json"}
            ],
            "body": {
                "mode": "raw",
                "raw": json.dumps(payload)
            },
            "url": {
                "raw": "{{base_url}}/incidents/api/v1/log-incident/",
                "host": ["{{base_url}}"],
                "path": ["incidents", "api", "v1", "log-incident", ""]
            },
            "description": "No Authorization header — expects 401 Unauthorized."
        }
    }


def _log_incident_missing_title_item() -> dict:
    """POST /incidents/api/v1/log-incident/ — missing required 'title' field (400)."""
    payload = {
        "description": "This payload is missing the required title field.",
        "severity": "high",
        "affected_asset": "Database",
        "nist_stage": "containment"
    }
    return {
        "name": "Log Incident (Missing title — expects 400)",
        "request": {
            "method": "POST",
            "header": [
                {"key": "Authorization", "value": "Bearer {{access_token}}"},
                {"key": "Content-Type", "value": "application/json"}
            ],
            "body": {
                "mode": "raw",
                "raw": json.dumps(payload)
            },
            "url": {
                "raw": "{{base_url}}/incidents/api/v1/log-incident/",
                "host": ["{{base_url}}"],
                "path": ["incidents", "api", "v1", "log-incident", ""]
            },
            "description": "Authenticated but missing the required 'title' field — expects 400 Bad Request."
        }
    }


def main():
    collection = build_collection()
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT_FILE)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2)
    print(f"Postman collection written to: {output_path}")


if __name__ == "__main__":
    main()
