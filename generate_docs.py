import os
import random

products = [
    "Chai", "Chang", "Aniseed Syrup",
    "Chef Anton Cajun Seasoning",
    "Grandma Boysenberry Spread"
]

features = [
    "high customer demand",
    "premium quality ingredients",
    "strong market presence",
    "excellent flavor profile",
    "high profit margins"
]

markets = [
    "European markets",
    "Asian markets",
    "North American markets",
    "global markets"
]

folder = "data/company_docs"
os.makedirs(folder, exist_ok=True)

for i in range(50):

    product = random.choice(products)
    feature = random.choice(features)
    market = random.choice(markets)

    content = f"""
Product Report: {product}

Key Features:
- {feature}
- trusted by customers worldwide
- strong brand reputation

Market Performance:
The product has shown strong growth in {market}.
"""

    filename = f"{folder}/doc_{i}.txt"

    with open(filename, "w") as f:
        f.write(content)

print("50 documents generated successfully!")