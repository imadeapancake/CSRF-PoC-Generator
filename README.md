#CSRF PoC Generator

![image-removebg-preview](https://github.com/imadeapancake/CSRF-PoC-Generator/assets/104873442/f3949eb4-e655-4fa9-9ea2-69e6e2044f94)

This program features a user-friendly GUI built with Tkinter.

#### Key Features:

- **HTTP Method Selection:** Choose between various HTTP methods (POST, GET, HEAD, PUT, DELETE) for your CSRF payload.
- **Target URL:** Specify the target URL where the CSRF request will be sent.
- **Input Data:** Enter key-value pairs for the form data to be submitted with the CSRF request.
- **Custom Headers and Cookies:** Include custom headers and cookies that might be required for the CSRF attack.
- **Auto-submit Option:** Automatically submit the form when the payload is loaded.
- **Include Head Option:** Option to include or exclude the HTML head section in the generated payload.
- **Preview and Generate:** Preview the generated CSRF payload before saving it to ensure accuracy and effectiveness.

#### Usage:

1. **Configure Settings:** Set default values for HTTP method, target URL, auto-submit, and include head options through the settings menu.
2. **Generate Payload:** Enter the necessary details such as target URL, input data, custom headers, and cookies. Use the "Generate" button to create the CSRF payload and save it as an HTML file.
3. **Preview Payload:** Use the "Preview" button to view the generated CSRF payload in a new window, with syntax highlighting for better readability.
