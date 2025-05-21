import sys
import os
import json
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

class FolderCreatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.factory_mapping = {
            'MX1': ('Juarez', 'Mexico'),
            'MX2': ('Juarez', 'Mexico'),
            'MX3': ('Juarez', 'Mexico'),
            'VAD': ('Vadodara', 'India'),
            'BAO': ('Baodi', 'China'),
            'CAS': ('Castellon', 'Spain'),
            'PON': ('Ponferrada', 'Spain'),
            'GAS': ('Gaspe', 'Canada'),
            'GRF': ('Grand forks', 'United States'),
            'CHE': ('Cherbourg', 'France'),
            'FUJ': ('Fujian', 'China'),
            'DAB': ('Debaspet', 'India')
        }

        # Blade types allowed for each factory
        self.factory_blade_types = {
            'BAO': ['75.7P2', '77.4-2P', '80.4E1'],
            'CAS': ['77.4P3', '77.4-1P', '77.4-2P', '77.4P6'],
            'CHE': ['107P2'],
            'DAB': ['64.6', '62.2P2'],
            'FUJ': ['107P2'],
            'GAS': ['62.2P2', '47.3P', '44.1P'],
            'GRF': ['62.2P2'],
            'PON': ['48.7P', '62.2P2'],
            'VAD': ['75.7P2', '77.4P3', '77.4-2P'],
            'MX1': ['62.2'],
            'MX2': ['75.7'],
            'MX3': ['68.7']
        }


        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
    
        # Logo at the top
        self.logo_label = QLabel(self)
        pixmap = QPixmap("logo.png")
        if pixmap.isNull():
            print("Warning: logo.png not found!")
        else:
            self.logo_label.setPixmap(pixmap.scaled(200, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Employee ID Input
        self.emp_id_label = QLabel('Employee ID/SSO:')
        self.emp_id_input = QLineEdit()
        layout.addWidget(self.emp_id_label)
        layout.addWidget(self.emp_id_input)

        # Customer Name Input
        self.customer_label = QLabel('Customer Name:')
        self.customer_input = QLineEdit('GE Vernova')
        layout.addWidget(self.customer_label)
        layout.addWidget(self.customer_input)

        # Supplier Dropdown
        self.supplier_label = QLabel('Supplier:')
        self.supplier_dropdown = QComboBox()
        self.supplier_dropdown.addItems(['LM', 'TPI'])
        self.supplier_dropdown.currentTextChanged.connect(self.update_factory_options)
        layout.addWidget(self.supplier_label)
        layout.addWidget(self.supplier_dropdown)

        # Factory Name
        self.factory_label = QLabel('Factory Name:')
        self.factory_dropdown = QComboBox()
        self.factory_dropdown.addItems(['BAO', 'VAD', 'CAS', 'DAB', 'FUJ', 'GAS', 'GRF', 'PON', 'CHE'])
        self.factory_dropdown.currentTextChanged.connect(self.update_location_country_blades)
        layout.addWidget(self.factory_label)
        layout.addWidget(self.factory_dropdown)

        # Factory Location
        self.factory_location_label = QLabel('Factory Location:')
        self.factory_location_dropdown = QComboBox()
        self.factory_location_dropdown.setEditable(True)
        self.factory_location_dropdown.addItems(['BAODI', 'CASTILLON', 'CHERBOURG', 'DABASPET', 'FUJIAN', 'GASPE', 'GRAND FORKS', 'JUAREZ', 'PONFERRADA', 'VADODARA'])
        layout.addWidget(self.factory_location_label)
        layout.addWidget(self.factory_location_dropdown)

        # Country Selection
        self.country_label = QLabel('Country:')
        self.country_dropdown = QComboBox()
        self.country_dropdown.setEditable(True)
        self.country_dropdown.addItems(['CHINA','BRAZIL', 'CANADA', 'INDIA', 'FRANCE', 'MEXICO', 'POLAND', 'SPAIN', 'TURKEY', 'UNITED STATES'])
        layout.addWidget(self.country_label)
        layout.addWidget(self.country_dropdown)

        # Blade Type
        self.blade_type_label = QLabel('Blade Type:')
        self.blade_type_dropdown = QComboBox()
        self.blade_type_dropdown.addItems(['75.7P2','77.4-2P','80.4E1'])
        layout.addWidget(self.blade_type_label)
        layout.addWidget(self.blade_type_dropdown)


         # Blade ID Input
        self.blade_id_label = QLabel('Blade ID:')
        self.blade_id_input = QLineEdit()
        layout.addWidget(self.blade_id_label)
        layout.addWidget(self.blade_id_input)

        # Inspection Stage Dropdown
        self.stage_label = QLabel('Inspection Stage:')
        self.stage_dropdown = QComboBox()
        self.stage_dropdown.addItems([
            'Final_Release_Inspection',
            'Post_Mold_inspection', 
            'In_Mold_PreClosing_Inspection',
            'Field_Inspection',
            'Other_Inspection'
        ])
        layout.addWidget(self.stage_label)
        layout.addWidget(self.stage_dropdown)

        # Comment
        self.comment_label = QLabel('Comment:')
        self.comment_input = QLineEdit()
        layout.addWidget(self.comment_label)
        layout.addWidget(self.comment_input)

        # Buttons
        self.create_button = QPushButton('Create Folders')
        self.create_button.clicked.connect(self.create_folder_structure)
        layout.addWidget(self.create_button)

        self.metadata_button = QPushButton('Generate Metadata')
        self.metadata_button.clicked.connect(self.generate_metadata)
        layout.addWidget(self.metadata_button)

        self.setLayout(layout)
        self.setWindowTitle('Folder Creator')
        self.show()
    
    def update_factory_options(self):
        supplier = self.supplier_dropdown.currentText()
        self.factory_dropdown.clear()
        if supplier == "TPI":
            self.factory_dropdown.addItems(['MX1', 'MX2', 'MX3'])
        else:
            self.factory_dropdown.addItems(['BAO', 'VAD', 'CAS', 'DAB', 'FUJ', 'GAS', 'GRF', 'PON', 'CHE'])    

    def update_location_and_country(self):
        factory = self.factory_dropdown.currentText()
        location, country = self.factory_mapping.get(factory, ('', ''))
        if location:
            self.factory_location_dropdown.setCurrentText(location)
        else:
            self.factory_location_dropdown.setEditText('')

        if country:
            self.country_dropdown.setCurrentText(country)

    def update_blade_types(self):
        factory = self.factory_dropdown.currentText()
        blade_types = self.factory_blade_types.get(factory, [])
        self.blade_type_dropdown.clear()
        self.blade_type_dropdown.addItems(blade_types)

    def update_location_country_blades(self):
        self.update_location_and_country()
        self.update_blade_types()
                
    def get_plant_code(self, factory_name):
        plant_codes = {'BAO': '55', 'VAD': '33', 'CAS': '23', 'DAB': '32', 'FUJ': '56', 'GAS': '42', 'GRF': '41', 'PON': '22', 'CHE': '27'}
        return plant_codes.get(factory_name, 'XX')
    
    def create_folder_structure(self):
        """Create the folder structure based on user inputs."""
        customer = self.customer_input.text()
        country = self.country_dropdown.currentText()
        factory = self.factory_dropdown.currentText()
        scan_type = self.scan_type_dropdown.currentText()
        component_type = self.component_dropdown.currentText()
        blade_id = self.blade_id_input.text()
        blade_type = self.blade_type_dropdown.currentText()
        plant_code = self.get_plant_code(factory)

    def create_folder_structure(self):
        customer = self.customer_input.text()
        country = self.country_dropdown.currentText()
        factory = self.factory_dropdown.currentText()
        stage = self.stage_dropdown.currentText()
        blade_id = self.blade_id_input.text()
        blade_type = self.blade_type_dropdown.currentText()
        plant_code = self.get_plant_code(factory)

        # Validation for Blade ID length
        supplier = self.supplier_dropdown.currentText()
        if supplier == 'LM' and len(blade_id) != 6:
            self.show_error_message("Blade ID for LM must be 6 digits.")
            return
        elif supplier == 'TPI' and len(blade_id) != 5:
            self.show_error_message("Blade ID for TPI must be 5 digits.")
            return
        
        # Continue with folder creation if Blade ID is valid

        # Country prefix mapping
        country_prefix_map = {
        'CHINA': 'GECH',
        'INDIA': 'GEIN',
        'MEXICO': 'GEMX',
        'BRAZIL': 'GEBR',
        'CANADA': 'GECA',
        'FRANCE': 'GEFR',
        'POLAND': 'GEPL',
        'SPAIN': 'GES',
        'TURKEY': 'GETR',
        'UNITED STATES': 'GEUS'
        }
        prefix = country_prefix_map.get(country, 'GE')

        # Main Folder Path
        base_folder = os.path.join(os.path.expanduser('~'), 'Desktop', f"{customer}-{country}")
        factory_folder = os.path.join(base_folder, f"Factory_{factory}")

        supplier = self.supplier_dropdown.currentText()

        if supplier == "TPI":
           blade_folder_name = f"Blade_TPI-{blade_id}"
        else:
           blade_folder_name = f"BLADE_{blade_id}-{blade_type}-{plant_code}"

        blade_folder = os.path.join(factory_folder, blade_folder_name)
        service_folder = os.path.join(blade_folder, f"IIN-R-{prefix}_serviceid_00000")
        stage_folder = os.path.join(service_folder, stage)

        os.makedirs(stage_folder, exist_ok=True)

        # ✅ Add this after successful folder creation
        self.create_button.setStyleSheet("background-color: green; color: white;")
        self.create_button.setText("Success!")
        QTimer.singleShot(500, self.reset_create_button)


        # Subfolders
        subfolders = ['Central_Web', 'C-Stiffener', 'Leading_Edge', 'Third_Web', 'Trailing_Edge', 'Ros']
        for sub in subfolders:
            os.makedirs(os.path.join(stage_folder, sub), exist_ok=True)

    def show_error_message(self, message):
        """Displays an error message in a popup."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()
        self.create_button.setStyleSheet("background-color: red; color: white;")
        self.create_button.setText("Error!")
        QTimer.singleShot(500, self.reset_create_button)

    def reset_create_button(self):
        self.create_button.setStyleSheet("")
        self.create_button.setText("Create Folder")
           

    def generate_metadata(self):
        """Generate metadata JSON in subfolders that contain images or videos."""
        base_folder = os.path.join(os.path.expanduser('~'), 'Desktop', f"{self.customer_input.text()}-{self.country_dropdown.currentText()}")
        valid_extensions = {".jpg", ".jpeg", ".png", ".mp4", ".avi", ".360", ".mov"}
        
        supplier = self.supplier_dropdown.currentText()
        factory = self.factory_dropdown.currentText()  # Retrieve factory name here
        plant_code = self.get_plant_code(factory)  # Fix error by passing the correct factory name
        blade_id = self.blade_id_input.text()
        blade_type = self.blade_type_dropdown.currentText()
        # Construct Blade_ESN only if component type is Blade
        if supplier == "TPI":
           blade_esn = f"Blade_TPI-{blade_id}"
        else:
           blade_esn = f"{blade_id}-{blade_type}-{plant_code}" 
        for root, dirs, files in os.walk(base_folder):
            has_media_files = any(file.lower().endswith(tuple(valid_extensions)) for file in files)


            if has_media_files:
                # Extract last folder name for 'sect'
                sect_folder = os.path.basename(root)
                # Format: "1/11/25 23:51" → day/month/year hour:minute
                current_dt = datetime.datetime.now().strftime("%-d/%-m/%y %H:%M") if os.name != 'nt' else datetime.datetime.now().strftime("%#d/%#m/%y %H:%M")

                metadata = {
                    "sso": self.emp_id_input.text(),
                    "datetime": current_dt,
                    "cust": self.customer_input.text(),
                    "supplier": self.supplier_dropdown.currentText(),
                    "country": self.country_dropdown.currentText(),
                    "factory": self.factory_dropdown.currentText(),
                    "location": self.factory_location_dropdown.currentText(),
                    "blade_id": self.blade_id_input.text(),
                    "engine_type": self.blade_type_dropdown.currentText(),
                    "plant_code": plant_code,
                    "esn": blade_esn,
                    "inspection_stage": self.stage_dropdown.currentText(),
                    "sect": sect_folder,
                    "comment": self.comment_input.text()
                }

                metadata_file = os.path.join(root, "metadata.json")
                try:
                    with open(metadata_file, "w") as f:
                        json.dump(metadata, f, indent=4)
                    print(f"✅ Metadata created in: {metadata_file}")
                except Exception as e:
                    print(f"❌ Error creating metadata: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FolderCreatorApp()
    ex.show()
    sys.exit(app.exec_())
