CSRF PoC Generator

![image-removebg-preview](https://github.com/imadeapancake/CSRF-PoC-Generator/assets/104873442/2e1f2a4c-eb53-413d-ac99-400b4193071d)



The CSRF PoC Generator is a Python-based tool designed to assist security professionals and penetration testers in creating Cross-Site Request Forgery (CSRF) Proof of Concept (PoC) payloads. This program features a user-friendly graphical interface built with Tkinter, allowing users to easily configure and generate CSRF attack vectors.

Key Features:
HTTP Method Selection: Choose between various HTTP methods (POST, GET, HEAD, PUT, DELETE) for your CSRF payload.
Target URL: Specify the target URL where the CSRF request will be sent.
Input Data: Enter key-value pairs for the form data to be submitted with the CSRF request.
Custom Headers and Cookies: Include custom headers and cookies that might be required for the CSRF attack.
Auto-submit Option: Automatically submit the form when the payload is loaded.
Include Head Option: Option to include or exclude the HTML head section in the generated payload.
Preview and Generate: Preview the generated CSRF payload before saving it to ensure accuracy and effectiveness.
Usage:
Configure Settings: Set default values for HTTP method, target URL, auto-submit, and include head options through the settings menu.
Generate Payload: Enter the necessary details such as target URL, input data, custom headers, and cookies. Use the "Generate" button to create the CSRF payload and save it as an HTML file.
Preview Payload: Use the "Preview" button to view the generated CSRF payload in a new window, with syntax highlighting for better readability.
This tool simplifies the process of creating CSRF attack vectors, making it easier to test the security of web applications against CSRF vulnerabilities.
