## Architecture Description
To view the [architecture diagram](additional/taxi_architecture.excalidraw), open the excalidraw file: additional/taxi_architecture.excalidraw in the website https://excalidraw.com/. 
The diagram is a high-level overview of the architecture and its components.

Following Assumptions were made during the design of the architecture:
- Taxi sends trip details at end of the trip to the API to receive a receipt. 
- API only handles transactions and cannot be polled by the taxi for any live updates.
- Taxi pushes live location while in duty for allowing the company to track its current location
- Taxis can subscribe to APIs by polling so that it can get live updates from company. Polling because the taxi driver might be out of duty.
- Live Dashboard is also expected to display the current status of the taxis and its trip details
- Dynamic Data needs to be batched for analytics
- Cloud platform is Azure, and therefore the tooling are mostly Azure native.

## Data Analysis Task
Following assumptions were made during the design of the data analysis:
- Caching could not be enabled as severless databricks computer does not allow persistence.
- Data is stored in Databricks Unity Catalog and accessible only to Databricks
- Data was downloaded manually into the Unity Catalog for analysis and testing purposes
- Pipeline to automatically fetch data was not expected
- Notebook will be used only in databricks and cannot be run locally or in CI/CD.
- Test cases however can be run locally or in CI/CD to test the functionality of the modules.
- If notebook is not executing properly, you can find the [notebook output](additional/taxi_data_analytics.ipynb) in additional/taxi_data_analytics.ipynb. The notebook output is a static representation of the notebook execution and does not require any dependencies to run.