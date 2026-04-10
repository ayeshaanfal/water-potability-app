def rule_based_check(data):
    violations = []

    if data['ph'] < 6.5 or data['ph'] > 8.5:
        violations.append("Unsafe pH")

    if data['Solids'] > 500:
        violations.append("High TDS")

    if data['Chloramines'] > 4:
        violations.append("High Chloramines")

    if data['Organic_carbon'] > 5:
        violations.append("High Organic Carbon")

    if data['Turbidity'] > 1:
        violations.append("High Turbidity")

    return violations