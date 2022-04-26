![GitHub Actions CI Workflow](https://github.com/BME547-Spring2022/ecg-analysis-aymanzyy/actions/workflows/.github/workflows/pytest_runner.yml/badge.svg)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Image Processor

## Welcome back to AJS Industries. We now present you our final product, the Patient Monitoring Client/Server Let's give you an overview of how it works. 
### Responsiblity Clauses:
* The following is the breakdown of responsiblities:
	* Julianna Bordas: Add-On GUI
	* Steven Parker: Monitoring-Side GUI
	* Ayman Yousef: Patient-Side GUI

### Video Demonstration:
Here is a link to a demonstration dont by co-developer Steven Parker about the functionality of all 3 GUIs and how they worrk in tandem: https://www.youtube.com/watch?v=5AuaDZnSStY&t=147s

### Prerequisites 
* This version of the code has been tested with Python 3.9 on both MacOS and Windows systems
*  It is important for you as a user to have the same exact modules installed. For this entire application, one should work in their terminal.
* The very first step is to clone the repository that contains the application. This can be done via the command:
  ```
   git clone https://github.com/BME547-Spring2022/final-project-ayman-julianna-steven.git

  ```
* It is best to create a virtual environment to work in. This can be done via the following command. Python3 is the python version used to create/test the code. 
  ```
  python3 -m venv /path/to/new/virtual/environment 

  ```
* Once you have a virtual environment, you can activate it with the command: source nameofenvironment/bin/activate. With this environment activated, we can now install the right modules. Use the following command to do so: 
    ```
    pip install -r requirements.txt

    ```
### Instructions for Running Patient-Side GUI:

* In order to run the patient-side gui, make sure you are in the correct folder. You should be able to see a file named <em>patientSideGui.py</em>. To start the GUI, run the following:
    ```
    python3 patientSideGUI.py
    ```	

### In-depth Analysis: How does the GUI work?
* By running the above code, you should be able to see something like so: 

![](https://i.gyazo.com/47efe0c916175df3479d8fbcf56092ae.png)

* The first thing to take note of are the two entry boxes to the left of the GUI with the labels "Medical Record Number" and "Patient Name". These are user defined and can be filled in with your patient's record number and name. It is important to note that the record number should be a number with no letters/spaces entered. Messing this up will lead to info posting issues. The patient name should be a one or two word string containing only letters. 
	* It is important to note that a medical record number is necessary for posting to a database. The "Post Info" is disabled unless something is entered. 
* The next thing to take note of are the two display buttons labeled "Display Medical Image" & "Dispaly ECG File". These allow users the ability to show medical/ECG traces locally for their viewing pleasure, with the images visualized in the "Local Medical Image" and "Local ECG Image" boxes respectively. A viewed medical image can be uploaded to a database, which we will go into later on. However, the "Display ECG File" is purely for viewing a trace and not for uploading
	* The "Reset Medical Image" and "Reset ECG Image" buttons allow the user to clear the GUI of these images and allow them to view different ones. 
	
![](https://i.gyazo.com/6c5fd005f3ddb122de4a303b65aee37d.png)

* The "Process ECG File" allows a user to select a CSV file containing time and voltage information of a signal and processes the ECG trace and calculates the heart rate. The ECG trace then gets viewed in the "Local ECG Image" box and the calculated heart rate updates the "Heart Rate" entry box. Both of these are prepped for upload after pressing this button. 
* The "Post Info" button takes the information entered by the user and uploads it to the Mongo database. This information can be any combination of a medical image, ECG image/heart rate, and name plus the necessary medical record number. When a patient's is used for the first time, a new Patient class object is created and uploaded to the database, while every other use of the medical record number will either update the patient's name or append new information to the patient's data. 
	* Posting will also update the status bar just above the ECG image, showcasing a message on what happened when the Post Info button was pressed. 
		* "Name Updated": A name was updated or if the same name is used and nothing else changes
		* "Patient Created w/Files": A new patient is created with files. 
		*  "Patient Created": A new patient is created without files. 
		* "Patient Data Updated": Patient's Data is Updated
* The "Cancel" button is there to exit the GUI. Doing so just closes the program with no harm done to what you've already uploaded. However, it is important to point out that any data that was on the GUI without being uploaded is lost, so be sure to upload what you must before exiting the program. 

### Instructions on running Available Patients GUI:
* If the prerequisities listed at the top of this README have already been met, you can continue. If not, make sure to follow these prereqs before continuing. 
* In order to run the patient-side gui, make sure you are in the correct folder. You should be able to see a file named <em>add_on_gui.py</em>. To start the GUI, run the following:
    ```
    python3 add_on_gui.py
    ```	

* GUI will appear titled "Add_on GUI", and the user should allow for GUI to fully load with current patient data
* ![](https://i.gyazo.com/ff13e1cc6715c2613141f790da258652.png)
 * Displayed in GUI will be a list of heart rates, patient names, and a button for each patient. By clicking on the button for a patient, an ECG image will be displayed if available. Buttons for each patient are labeled either "Display ECG Image" or "No ECG Image" depending on whether or not the data contains an ECG image for aspecific patient
 * ![](https://i.gyazo.com/aef2093ea27753624a387b9b215e7ae5.png)
* The user also has the option to click a button labeled "Reset ECG Image" to return back to the default medical image
* A user can exit the GUI by clicking the button labeled "Cancel"
 * The GUI will refresh every 30 seconds for any new patients and information added to database

### In-Depth Analysis: Available Patients GUI (Add-On) 
* The goal of the following this GUI is to retrieve requested patient information, such as, patient name, patient heart rate, and patient ECG image. 
* This information is displayed and updated every 30 seconds for the user to access. 
* The GUI generates a list of heart rates and patient names, allowing the user the option to click a button to view the ECG image for each patient. After the user is done with viewing the patient's ECG image, they may reset the image by clicking a "Reset" button so that it is back to the default image.


### Instructions for Running Monitoring-Side GUI:

* In order to run the Montioring-side gui, make sure you are in the correct folder. You should be able to see a file named <em>monitoringSideGui.py</em>. To start the GUI, run the following:
    ```
    python3 monitoringSideGUI.py
    ``` 

### In-depth Analysis: How does the GUI work?
* By running the above code, you should be able to see something like so:

![](https://i.gyazo.com/cbb022524f31c5fd77e02a569dccc2c9.png)

* All patient information will be shown on this GUI when the patient is selected. 
* You can choose which patient you would like to access by selecting them in the gui dropdown box and pressing "Enter Patient File" Button. Once you do this,the GUI will update to look something like this:

![](https://i.gyazo.com/ca3bcbea00770029062c48997385c1eb.png)

* Any available patient name, heartrate, timestamp, and medical record number should be updated on the gui. Also, if there is a recent ECG it should be displayed under "Most Recent ECG Image:"

* If there are no available ECG images, there will be no button to view or download them. If there are historic images, their time stamps will be shown in the drop down box. Select the one you want, choose to display it by pressing the display button, then download with the download button if you desire. Do not try to download an image unless you have displayed one.

* If there are no available medical images, there will be no button to view or download them. If there are historic images, their names will be shown in the drop down box. Select the one you want, choose to display it by pressing the display button, then download with the download button if you desire. Do not try to download an image unless you have displayed one.

* The GUI will automatically populate itself with updated information every 25 seconds

* Press the cancel button to close the GUI
### Cloud-Based Server
#### Server Location
The URL of the deployed web service is: http://vcm-25858.vm.duke.edu:5200
#### Server API Routines
* POST ROUTE: /api/patient/new_patient
	* This route takes in a dictionary of data and sends the data off to a driver function to perform checks before saving the patient information to the Mongo database. 
	* The input data should be in the form of a dictionary populated by any number of the following keys: medical record number (which is the only necessary key), name, ECG image, medical image, & heart rate. The post routine returns a message and status code depending on the success/failure of the dictionary checks/validation. 
	* The dictionary checks/validation are centered around checking a few different necessities:
		* A medical record number is required for either adding a patient or updating a patient's information. Failure to do so will return an appropriate message and status code of 400. Likewise, heart rates should be numeric inputs. However, this shouldn't be an issue for the user as the heart rate is automatically calculated when an ECG file is uploaded in order to be traced
		* The medical record number should be supplied as an integer of any length. There isn't any tolerance for alpha-numeric strings and an error message will be returned outlining this if this input format isn't respected
		* The name input can be given as either a singular first name or a first and last name. Similar to the medical record number, the name input should be strictly composed of letters. An error message returns if this isn't respected outlining the necessity for strictly letters when entering a name. 
		* The two images should be given as Base64 strings, with the validation process checking to make sure that the strings can be decoded. Failure to have the appropriate Base64 format will return an appropriate message. 
		* Time stamps are automatically generated when an ECG file is detected and are added to the dictionary that get uploaded to the database. 
* GET ROUTE: /api/monitoring/get_list
    * Obtain a list of strings of all medical record numbers (MRN) as ints
* GET ROUTE: /api/monitoring/get_patient_name/<record_num>
    * Route to obtain a patient's name as a string given MRN as int
* GET ROUTE: /api/monitoring/get_patient_hr/<record_num>
    * Route to obtain a patient's heart rate as string given MRN as int
* GET ROUTE: /api/monitoring/get_patient_timestamp/<record_num>
    * Route to obtain a patient's timestamp as string given MRN as int
* GET ROUTE: /api/monitoring/get_patient_ecg/<record_num>
    * Route to obtain a patient's timestamp as string given MRN as int
* GET ROUTE: /api/monitoring/get_ecg_list/<record_num>
    * Route to obtain a patient's historic ecg list as a list given MRN as int. Each list item is a dictionary containing a b64 string and the timestamp associated.
* GET ROUTE: /api/monitoring/get_med_list/<record_num>
    * Route to obtain a patient's historic medical list as a list given MRN as int. Each list item is a b64 string
* GET ROUTE: /api/add_on/patient_dict/<patient_id>
    * This function implements a GET route with a variable URL.  The desired
    patient id number is included as part of the URL.  The function calls
    another function to implement the functionality and receives an
    answer and status code from that function, which it then returns.
* GET ROUTE: /api/add_on/patient_record_numbers/
    * Obtains a list of strings of all medical record numbers (MRN) as ints
* GET ROUTE: /api/add_on/get_patient_name/<record_num>
    * Route to obtain a patient's name as a string given MRN as int*
### Database Structure:
* The MongoDatabase utilizes the Patient.py structure in order to save patients to the database. A Patient object is made up of 3 different fields: 
	* An Integer Field that holds the medical record number
	* A Character Field that holds the patient's name
	* A ListField that holds all other aspects of the dictionary, including ECG images, medical images, timestamps, and heart rates
	* ![](https://i.gyazo.com/141fadf8eb458688c96fd68fd95a0483.png)
* It is important to remember that not all post requests require all fields. For example, one can post a medical record number and ECG image but not a name. The use of the ListField allowed us flexiblity throughout our coding process. 
