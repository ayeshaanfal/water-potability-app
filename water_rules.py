def rule_based_check(data):

    violations = []

    # pH
    if data["ph"] < 6.5 or data["ph"] > 8.5:
        violations.append("Unsafe pH")

    # TDS
    if data["TDS"] > 500:
        violations.append("High TDS")

    # Hardness
    if data["Hardness"] > 200:
        violations.append("High Hardness")

    # Nitrate
    if data["Nitrate"] > 45:
        violations.append("High Nitrate")

    # Fluoride
    if data["Fluoride"] < 0.6 or data["Fluoride"] > 1.5:
        violations.append("Unsafe Fluoride")

    # Turbidity
    if data["Turbidity"] > 5:
        violations.append("High Turbidity")

    return violations