import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import xml.dom.minidom

class CombinedVinDecoderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Combined VIN Decoder App")

        # Bulk VIN Decoder (create this instance first)
        self.bulk_decoder = BulkVinDecoder(self.root)

        # Single VIN Decoder (pass self.root and self.bulk_decoder here)
        self.single_decoder = VinDecoderApp(root, self.bulk_decoder)

class VinDecoderApp(tk.Frame):
    def __init__(self, master=None, bulk_decoder=None):
        super().__init__(master)
        self.root = master
        self.bulk_decoder = bulk_decoder  # Save the reference to bulk_decoder
        self.root.title("Vin Check")

        self.bground = '#ffffff'
        self.fground = '#000000'
        self.tkfont = ("Poppins", 12)
        self.btnfont = ("Poppins", 12, "bold")
        self.warnfont = ("Poppins", 10, "bold")

        self.root.configure(bg=self.bground)

        self.create_label("Enter VIN", 14, 'bold', 0, 0, "w")
        self.vin_entry = self.create_entry(0, 1, 30, "ew")

        self.result_fields = {}
        fields_column1 = ["Manufacturer", "ModelYear", "Make", "VIN", "Axles", "BodyCabType", "DisplacementCC", "EngineModel",
                          "GVWR", "PlantCountry", "VehicleType", "BrakeSystemType", "TransmissionStyle", "WheelBaseLong", "Wheels"]

        fields_column2 = ["Model", "BodyClass", "DriveType", "FuelTypePrimary", "PlantCompanyName", "PlantState", "CurbWeightLB",
                          "WheelBaseShort", "WheelBaseType", "WheelSizeFront", "WheelSizeRear", "ErrorText"]

        for i, (field1, field2) in enumerate(zip(fields_column1, fields_column2)):
            self.result_fields[field1] = self.create_entry(i + 2, 1, 40, "w")
            self.result_fields[field2] = self.create_entry(i + 2, 3, 40, "w")

            self.create_label(field1, 12, "", i + 2, 0, "e")
            self.create_label(field2, 12, "", i + 2, 2, "e")

        # Button to fetch and display VIN information
        self.fetch_button = tk.Button(root, text="Decode Vin", font=self.btnfont, command=self.fetch_and_display)
        self.fetch_button.grid(row=i + 3, columnspan=2, column=0, pady=10, padx=10, sticky="ew")

        # # Button to clear VIN entry and results
        self.bulk_import_button = tk.Button(root, text="Bulk Import", font=self.btnfont, command=self.bulk_decoder.bulk_import_function)
        self.bulk_import_button.grid(row=i + 3, columnspan=1, column=2, pady=10, padx=10, sticky="ew")

        # Button to clear VIN entry and results
        self.clear_button = tk.Button(root, text="Clear", font=self.btnfont, command=self.clear_entries)
        self.clear_button.grid(row=i + 3, columnspan=1, column=3, pady=10, padx=10, sticky="ew")

        # Warning Label
        self.create_warning_label("This application is designed to access VIN data from the NHTSA website.", i + 4)
        # Warning Label
        self.create_warning_label("Please exercise caution when interpreting results, as variations in our equipment may not align precisely with the manufacturer's information.", i + 5)

    def create_label(self, text, size, weight, row, column, sticky):
        label = tk.Label(self.root, text=text, font=("Poppins", size, weight), bg=self.bground, fg=self.fground)
        label.grid(row=row, column=column, pady=8, padx=10, sticky=sticky)
        return label

    def create_entry(self, row, column, width, sticky):
        entry = tk.Entry(self.root, width=width)
        entry.grid(row=row, column=column, pady=8, padx=10, sticky=sticky)
        return entry

    def create_fields(self):
        fields_column1 = ["Manufacturer", "ModelYear", "Make", "VIN", "Axles", "BodyCabType", "DisplacementCC", "EngineModel",
                          "GVWR", "PlantCountry", "VehicleType", "BrakeSystemType", "TransmissionStyle", "WheelBaseLong", "Wheels"]

        fields_column2 = ["Model", "BodyClass", "DriveType", "FuelTypePrimary", "PlantCompanyName", "PlantState", "CurbWeightLB",
                          "WheelBaseShort", "WheelBaseType", "WheelSizeFront", "WheelSizeRear", "ErrorText"]

        for i, (field1, field2) in enumerate(zip(fields_column1, fields_column2)):
            self.result_fields[field1] = self.create_entry(i + 2, 1, 40, "w")
            self.result_fields[field2] = self.create_entry(i + 2, 3, 40, "w")

            self.create_label(field1, 12, "", i + 2, 0, "e")
            self.create_label(field2, 12, "", i + 2, 2, "e")

    def create_button(self, text, font, command, row, column):
        button = tk.Button(self.root, text=text, font=font, command=command)
        button.grid(row=row, column=column, pady=10, padx=10, columnspan=2, sticky="ew")

    def create_warning_label(self, text, row):
        label = tk.Label(self.root, font=self.warnfont, text=text, bg=self.bground, fg=self.fground)
        label.grid(row=row, column=0, pady=10, padx=10, columnspan=4, sticky="ew")

    def fetch_and_display(self):
        self.fetch_button.configure(state="disabled")
        self.clear_result_fields()

        vin = self.vin_entry.get().strip()
        api_url = "https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/"

        try:
            response = self.make_api_request(api_url + vin)
            self.update_result_fields(response)

        except requests.exceptions.RequestException as e:
            error_message = f"Error fetching data: {str(e)}"
            self.display_error_message(error_message)

        finally:
            self.fetch_button.configure(state="normal")

    def make_api_request(self, url):
        with requests.Session() as session:
            response = session.get(url, verify=True)
            response.raise_for_status()
            return response

    def update_result_fields(self, response):
        dom = xml.dom.minidom.parseString(response.text)

        for field, entry in self.result_fields.items():
            elements = dom.getElementsByTagName(field)
            if elements and elements[0].firstChild:
                value = elements[0].firstChild.nodeValue.strip()
            else:
                value = "N/A"
            entry.configure(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.configure(state="readonly")

    def display_error_message(self, message):
        messagebox.showinfo("Error", message)

    def clear_entries(self):
        self.vin_entry.delete(0, tk.END)
        self.clear_result_fields()

    def clear_result_fields(self):
        for entry in self.result_fields.values():
            entry.configure(state="normal")
            entry.delete(0, tk.END)
            entry.configure(state="readonly")

class BulkVinDecoder(tk.Frame):
    COLUMNS = ["Vin", "Status"]

    def __init__(self, root):
        self.root = root
        self.bulk_window = None  # Initialize bulk_window as None

    def bulk_import_function(self):
        # Create a new window if it doesn't exist
        if not self.bulk_window:
            self.bulk_window = tk.Toplevel(self.root)
            self.bulk_window.title("Multi Vin Import")

            bground = '#ffffff'
            self.bulk_window.configure(bg=bground)

        # Buttons
        self.create_button("CSV Import", self.csv_import_function, 1, 0)
        self.check_vins_button = self.create_button("Check VINs", self.fetch_and_display, 1, 1)
        self.create_button("Export CSV", self.export_csv_function, 1, 2)
        self.create_button("Clear", self.clear_tree, 1, 3)

        # Table (using Treeview)
        self.tree = self.create_treeview(self.bulk_window, self.COLUMNS)

        # Pandas DataFrame to store results
        self.results_df = pd.DataFrame(columns=["Vin"] + BulkVinDecoder.COLUMNS[1:])
        
    def create_button(self, text, command, row, column):
        button = tk.Button(self.bulk_window, text=text, font=("Poppins", 12, "bold"), command=command)
        button.grid(row=row, column=column, padx=10, pady=10)
        return button
     
    def clear_tree(self):
        # Clear the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Clear the results DataFrame
        self.results_df = pd.DataFrame(columns=["Vin"] + BulkVinDecoder.COLUMNS[1:])

    def create_loading_bar(self):
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Loading")

        loading_bar = ttk.Progressbar(loading_window, orient="horizontal", length=400, mode="indeterminate")
        loading_bar.pack(pady=20)

        return loading_window, loading_bar

    def create_treeview(self, root, columns):
        table_frame = ttk.Frame(root, width=500, height=900)
        table_frame.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

        tree = ttk.Treeview(table_frame, columns=columns, show="headings")  # Set show option to "headings"

        for col in columns:
            tree.column(col, width=250, anchor=tk.W)
            tree.heading(col, text=col, anchor=tk.W)

        tree.pack(expand=True, fill=tk.BOTH)
        tree.grid(row=0, column=0, columnspan=3, sticky="nsew")

        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        tree.configure(yscrollcommand=y_scrollbar.set)

        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        tree.configure(xscrollcommand=x_scrollbar.set)

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        return tree
    
    def fetch_and_display(self):
        self.check_vins_button.configure(state="disabled")

        # Get the VINs from the Treeview
        vins = [self.tree.item(item, "values")[0] for item in self.tree.get_children()]

        # Check if there are VINs to fetch
        if not vins:
            messagebox.showinfo("Error", "No VINs to fetch.")
            # Enables the fetch button.
            self.check_vins_button.configure(state="normal")
            return

        # Create loading bar window
        loading_window, loading_bar = self.create_loading_bar()

        # Start a new thread for fetching data
        fetch_thread = threading.Thread(target=self.fetch_vin_data_threaded, args=(vins, loading_window, loading_bar))
        fetch_thread.start()

        # Start the loading bar
        loading_bar.start()

    def fetch_vin_data_threaded(self, vins, loading_window, loading_bar):
        # List to store all the results
        results_list = []

        # Iterate through VINs and fetch data
        for vin in vins:
            result = self.fetch_and_display_vin(vin)
            if result:
                # Update the status in the Treeview
                self.update_treeview_with_status(vin, "Processed")
                results_list.append({"Vin": vin, "Status": "Processed", **result})

        # Update the DataFrame with all results
        if results_list:
            self.results_df = pd.concat([self.results_df, pd.DataFrame(results_list)], ignore_index=True)

        # Enables the fetch button.
        self.check_vins_button.configure(state="normal")

        # Stop the loading bar
        loading_bar.stop()

        # Close loading bar window when fetching is complete
        loading_window.destroy()

    def update_treeview_with_status(self, vin, status):
        self.tree.item(vin, values=[vin, status])

    def fetch_and_display_vin(self, vin):
        api_url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin}?format=xml"
        
        # Define the entities you want to retrieve from the API response
        desired_entities = [
            "Manufacturer", "ModelYear", "Make", "VIN", "Axles", "BodyCabType",
            "DisplacementCC", "EngineModel", "GVWR", "PlantCountry", "VehicleType",
            "BrakeSystemType", "TransmissionStyle", "WheelBaseLong", "Wheels", "Model",
            "BodyClass", "DriveType", "FuelTypePrimary", "PlantCompanyName", "PlantState",
            "CurbWeightLB", "WheelBaseShort", "WheelBaseType", "WheelSizeFront",
            "WheelSizeRear", "ErrorText"
        ]

        try:
            response = requests.get(api_url, verify=True)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                decoded_values = root.find(".//DecodedVINValues")
                if decoded_values is not None:
                    data = {}
                    for item in decoded_values.iter():
                        tag = item.tag
                        if tag in desired_entities:
                            value = item.text
                            data[tag] = value

                    return data
                else:
                    return None
            else:
                return None
        except requests.RequestException as e:
            return None

    def csv_import_function(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                # Read the entire CSV file into a Pandas DataFrame
                df = pd.read_csv(file_path, usecols=["Vin"])  # Add other necessary columns as needed

                # Add the "Status" column if not present
                if "Status" not in df.columns:
                    df["Status"] = ""

                # Replace NaN values with an empty string
                df = df.fillna("")

                # Filter out VINs that are already processed
                df = df[~df["Vin"].isin(self.results_df["Vin"])]

                # Insert the DataFrame values into the Treeview
                for index, row in df.iterrows():
                    values = (row["Vin"], "Not Processed")
                    self.tree.insert("", tk.END, values=values, iid=row["Vin"])

                    # Update the DataFrame with the initial status
                    self.results_df = pd.concat([self.results_df, pd.DataFrame({"Vin": [row["Vin"]], "Status": ["Not Processed"]})], ignore_index=True)

            except pd.errors.EmptyDataError:
                messagebox.showinfo("Error", "The selected CSV file is empty.")
            except pd.errors.ParserError:
                messagebox.showinfo("Error", "Error parsing the selected CSV file.")
        else:
            messagebox.showinfo("Info", "No file selected.")

    def export_csv_function(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

        if file_path:
            try:
                # Filter out rows with "Not Processed" status before exporting
                processed_results_df = self.results_df[self.results_df["Status"] != "Not Processed"]

                # Export the filtered DataFrame to CSV
                processed_results_df.to_csv(file_path, index=False)
                messagebox.showinfo("Info", f"CSV exported to: {file_path}")

            except Exception as e:
                messagebox.showinfo("Error", f"Error exporting CSV: {str(e)}")
        else:
            messagebox.showinfo("Info", "Export canceled.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CombinedVinDecoderApp(root)
    root.mainloop()