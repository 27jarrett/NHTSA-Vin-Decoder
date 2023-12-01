# VIN Decoder App (v1)

Vin_Decode_tool.py

This is a simple Python application built using the tkinter library for decoding Vehicle Identification Numbers (VIN). The app uses the National Highway Traffic Safety Administration (NHTSA) API to fetch and display information related to the provided VIN.

Features
User-friendly Interface: The application provides a clean and intuitive user interface with labeled entry fields for VIN input and sections to display VIN information.

Data Fetching: The app makes use of the NHTSA API to fetch detailed information about the vehicle based on the provided VIN.

Display Fields: The fetched information is displayed in categorized fields, making it easy for users to interpret the VIN data.

Cautionary Notes: The app includes warning labels to inform users about the source of the data and the need for caution when interpreting results.

    Click the "Decode Vin" button to fetch and display the VIN information.
    Use the "Clear" button to reset the VIN entry and result fields.

# VIN Decoder App (v2)

Vin Check.py

What's New in Version 2?

Welcome to the enhanced version (v2) of our VIN Decoder App! We've souped up the features and added some cool functionalities to make your VIN-decoding experience even better.

Features and Upgrades

Discover the addition of the "Bulk Import" button and function for an enriched user experience. The app now includes a "Bulk Import" feature, allowing you to process multiple VINs simultaneously. Excitingly, you can now export the results to a CSV file. This feature comes in handy when you need to keep a record of the decoded VIN information.

    Note: When importing vin numbers they should be listed in the first column in the import file.

How to Navigate

    CSV Import: Import VINs from a CSV file to populate the table.
    Check VINs: Fetch and display information for each imported VIN.
    Export CSV: Save displayed results to a CSV file for record-keeping.
    Clear: Reset VIN entry fields and result table for a fresh operation.

Building on the robust foundation of the NHTSA API, v2 introduces advanced data fetching capabilities. Expect quicker responses and more comprehensive details about your vehicle.

We've taken error handling to the next level. In v2, the app provides real-time feedback on potential issues during the API request process. Clear and concise error messages guide you through any hiccups.

Still crafted with love by 27jarrett.

Legal Bits

As always, this app is sailing under the MIT License.
