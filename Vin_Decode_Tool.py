import tkinter as tk
import requests
import xml.dom.minidom

class VinDecoderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VIN Decoder App")

        bground = '#ffffff'
        fground = '#000000'
        tkfont =  ("Areial", 12)
        btnfont = ("Areial", 12, "bold")
        warnfont = ("Areial", 10, "bold")     

        root.configure(bg=bground)
             
        # Label for VIN entry
        self.vin_label = tk.Label(root, text="Enter VIN", font=("Areial",14,'bold'), bg=bground, fg=fground)
        self.vin_label.grid(row=0, column=0, pady=10, padx=10, columnspan=1, sticky="w")

        # Entry for VIN input
        self.vin_entry = tk.Entry(root, width=30)
        self.vin_entry.grid(row=0, column=1, pady=5, padx=10, columnspan=4, sticky="ew")

        # Fields to display VIN information
        self.result_fields = {}
        fields_column1 = ["Manufacturer", "ModelYear", "Make", "VIN", "Axles", "BodyCabType", "DisplacementCC", "EngineModel",
                          "GVWR", "PlantCountry", "VehicleType", "BrakeSystemType", "TransmissionStyle", "WheelBaseLong", "Wheels"]

        fields_column2 = ["Model", "BodyClass", "DriveType", "FuelTypePrimary", "PlantCompanyName", "PlantState", "CurbWeightLB", 
                          "WheelBaseShort", "WheelBaseType", "WheelSizeFront", "WheelSizeRear", "ErrorText"]

        for i, (field1, field2) in enumerate(zip(fields_column1, fields_column2)):
            label1 = tk.Label(root, text=field1, bg=bground, fg=fground, font=tkfont)
            label1.grid(row=i + 2, column=0, pady=8, padx=10, sticky="e")

            entry1 = tk.Entry(root, state="readonly", width=40)
            entry1.grid(row=i + 2, column=1, pady=8, padx=10, sticky="w")
            self.result_fields[field1] = entry1

            label2 = tk.Label(root, text=field2, bg=bground, fg=fground, font=tkfont)
            label2.grid(row=i + 2, column=2, pady=8, padx=10, sticky="e")

            entry2 = tk.Entry(root, state="readonly", width=40)
            entry2.grid(row=i + 2, column=3, pady=8, padx=10, sticky="w")
            self.result_fields[field2] = entry2

        # Button to fetch and display VIN information
        self.fetch_button = tk.Button(root, text="Decode Vin", font=btnfont, command=self.fetch_and_display)
        self.fetch_button.grid(row=i + 3, columnspan=2, column=0, pady=10, padx=10, sticky="ew")

        # Button to clear VIN entry and results
        self.clear_button = tk.Button(root, text="Clear", font=btnfont, command=self.clear_entries)
        self.clear_button.grid(row=i + 3, columnspan=2, column=2, pady=10, padx=10, sticky="ew")
        
        # Warning Label
        self.vin_label = tk.Label(root, font=warnfont, text="This application is designed to access VIN data from the NHTSA website.", bg=bground, fg=fground)
        self.vin_label.grid(row=i + 4, column=0, pady=10, padx=10, columnspan=4, sticky="ew")
        # Warning Label
        self.vin_label = tk.Label(root, font=warnfont, text="Please exercise caution when interpreting results, as variations in our equipment may not align precisely with the manufacturer's information.", bg=bground, fg=fground)
        self.vin_label.grid(row=i + 5, column=0, pady=10, padx=10, columnspan=4, sticky="ew")

    def fetch_and_display(self):
        self.fetch_button.configure(state="disabled")
        
        # Clear out prior entries
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
            # Enables the fetch button.
            self.fetch_button.configure(state="normal")

    def make_api_request(self, url):
        with requests.Session() as session:
            response = session.get(url, verify=True)
            response.raise_for_status()
            return response

    def update_result_fields(self, response):
        dom = xml.dom.minidom.parseString(response.text)

        # Update result fields with VIN information
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
        for entry in self.result_fields.values():
            entry.configure(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, message)
            entry.configure(state="readonly")

    def clear_entries(self):
        # Clear VIN entry and result fields
        self.vin_entry.delete(0, tk.END)
        self.clear_result_fields()

    def clear_result_fields(self):
        for entry in self.result_fields.values():
            entry.configure(state="normal")
            entry.delete(0, tk.END)
            entry.configure(state="readonly")

if __name__ == "__main__":
    root = tk.Tk()
    app = VinDecoderApp(root)
    root.mainloop()
