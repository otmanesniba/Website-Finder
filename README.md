# Website Finder 🌐


**Website Finder** is a Python script built with **Selenium** and **Microsoft Edge WebDriver** to automate the process of finding official websites for a list of companies. It uses human-like interactions to avoid detection and provides a user-friendly terminal interface.

---

## **Features**
- **Automated Search**: Searches Google for the official website of a given company.
- **Human-Like Interactions**: Simulates realistic typing and browsing behavior to avoid detection.
- **File Input/Output**: Accepts a list of companies from a `.txt` file or manual input.
- **Results Saving**: Saves the results to a `.txt` file on your desktop.
- **User-Friendly Interface**: Colorful terminal output with ASCII banners and progress tracking.

---

## **Prerequisites**
Before running the script, ensure you have the following:
1. **Python 3.8+** installed.
2. **Microsoft Edge** installed.
3. **Microsoft Edge WebDriver** installed. Download it from [here](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).
4. Required Python libraries installed. You can install them using:

   ```bash
   pip install selenium pyfiglet colorama fake-useragent
