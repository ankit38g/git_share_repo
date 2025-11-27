# Product Affinity

### Overview ###
The Product Affinity data product utilizes product affinity analysis to identify potential cross-sell opportunities. By understanding the relationships between products frequently purchased together, businesses can enhance customer recommendations and drive additional sales.
* Version : 0.3

### Use Cases ###

* Cross-Sell Strategy Development: Identify which products to recommend together to boost sales.
* Upsell Tactics: Develop marketing strategies to upsell related products based on customer purchase history.
* Customer Recommendation Enhancement: Improve customer interactions by providing tailored product suggestions.

### Key Features ###

* Affinity API: Offers endpoints to analyze and retrieve customer affinity data, highlighting relationships and preferences among products based on historical interactions.

* Cross Sell API: Provides endpoints to identify potential cross-sell opportunities based on historical purchase behavior.

### Metrics Included ###
* Cross Sell Success Rate: Potential for cross-selling a secondary product to customers based on past purchases.
* Total Spend: Aggregate monetary amount spent by customers across all purchases, reflecting overall expenditure trends.
* Purchase Frequency: How often a customer makes a purchase. Calculated based on the frequency of invoices

## Installation

1. Navigate to the `deployment` and `build` directory.
2. Execute the deployment bundle:
   - [Run Deployment Bundle](https://bitbucket.org/tmdc/product-affinity-training/src/main/deployment/pa-deploy-bundle.yml)

3. Run the data product spec:
   - [Run Data Product Spec](https://bitbucket.org/tmdc/product-affinity-training/src/main/deployment/pa-dp-spec.yml)

4. Finally, run the scanner:
   - [Run Scanner](https://bitbucket.org/tmdc/product-affinity-training/src/main/deployment/pa-dp-scanner.yml)

## Set up Activation Interfaces

### Set-up Data APIs

Run the Service manifest at the following address:
- [API Service](https://bitbucket.org/tmdc/product-affinity-training/src/main/activation/data-apis/service.yml)

**Dependency:** Ensure a secret is created in your environment for this service to function correctly.



# engineering_metrics_pov
# engineering_metrics_pov
