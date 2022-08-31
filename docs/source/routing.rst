routing
=======

.. code-block:: json

    {
        "terminal": true,
        "condition": {
            "address:to": "1111@example.dot"
        },
        "actions": [
            {
                "data": {
                    "email": "someuser@example.dot"
                },
                "action": "forward"
            }
        ],
        "scope": {
            "direction": "inbound"
        }
    }
