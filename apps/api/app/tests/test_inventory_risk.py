from types import SimpleNamespace

from apps.api.app.services.inventory_risk import calculate_inventory_risk


def test_high_inventory_risk():
    inventory = SimpleNamespace(
        product_id=5,
        current_stock=45,
        daily_demand=15,
        reorder_point=100,
        product=SimpleNamespace(
            sku="SEN-7712",
            name="Pressure Sensor",
            category="Sensors",
        ),
    )

    result = calculate_inventory_risk(inventory)

    assert result.days_of_stock == 3
    assert result.risk_level == "HIGH"
    assert result.explanation == (
        "Pressure Sensor has 3.0 days of stock remaining "
        "at the current daily demand of 15 units. "
        "Current stock of 45 units is below the reorder point of 100 units."
    )


def test_medium_inventory_risk():
    inventory = SimpleNamespace(
        product_id=1,
        current_stock=420,
        daily_demand=58,
        reorder_point=500,
        product=SimpleNamespace(
            sku="MTR-4821",
            name="Industrial Motor 4821",
            category="Motors",
        ),
    )

    result = calculate_inventory_risk(inventory)

    assert round(result.days_of_stock, 1) == 7.2
    assert result.risk_level == "MEDIUM"
    assert result.explanation == (
        "Industrial Motor 4821 has 7.2 days of stock remaining "
        "at the current daily demand of 58 units. "
        "Current stock of 420 units is below the reorder point of 500 units."
    )


def test_low_inventory_risk():
    inventory = SimpleNamespace(
        product_id=2,
        current_stock=850,
        daily_demand=35,
        reorder_point=300,
        product=SimpleNamespace(
            sku="PMP-1042",
            name="Hydraulic Pump",
            category="Hydraulic Equipment",
        ),
    )

    result = calculate_inventory_risk(inventory)

    assert round(result.days_of_stock, 1) == 24.3
    assert result.risk_level == "LOW"
    assert result.explanation == (
        "Hydraulic Pump has 24.3 days of stock remaining "
        "at the current daily demand of 35 units."
    )


def test_zero_demand_is_low_risk():
    inventory = SimpleNamespace(
        product_id=4,
        current_stock=100,
        daily_demand=0,
        reorder_point=50,
        product=SimpleNamespace(
            sku="VAL-2291",
            name="Control Valve",
            category="Industrial Valves",
        ),
    )

    result = calculate_inventory_risk(inventory)

    assert result.days_of_stock == float("inf")
    assert result.risk_level == "LOW"
    assert result.explanation == (
        "Control Valve has inf days of stock remaining "
        "at the current daily demand of 0 units."
    )