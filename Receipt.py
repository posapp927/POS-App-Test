class ReceiptDesigner:
    def __init__(self, logo_path):
        self.logo_path = logo_path

    def create_receipt_pdf(self, items, customer_id, filename='receipt.pdf'):
        # Your existing code for creating a PDF
        pass


class PrinterConnection:
    def __init__(self, printer_name):
        self.printer_name = printer_name

    def send_to_printer(self, pdf_filename):
        # Your existing code for sending to printer
        pass

    def open_cash_drawer(self):
        # Your existing code for opening the cash drawer
        pass



# import subprocess
# import tempfile
# import time
# from collections import defaultdict
#
# import cups
# import numpy as np
# from flask import Flask, render_template, request, jsonify, url_for
# import pandas as pd
# import os
#
# from reportlab.graphics.barcode import createBarcodeDrawing
# from reportlab.graphics.shapes import Drawing
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import mm
#
#
# app = Flask(__name__)
#
# # Global variable to store product data
# product_data = pd.read_csv('database/Cart Table.csv', dtype={'UPC': str, 'QOH': int})
#
# customer_data = pd.read_csv('database/POS Customer Data.csv', dtype={'Phone': str})
#
# discounts_data = pd.read_csv('database/Astro Offers - August, 2024.csv', dtype={'UPC': str})
#
# # Extract unique discount names
# unique_discount_names = sorted(discounts_data['Discount Name'].unique())
#
# @app.route('/')
# def home():
#     return render_template('index.html', discount_names=unique_discount_names)
#
#
# @app.route('/manage-inventory')
# def manage_inventory():
#     return render_template('manage-inventory.html')
#
# @app.route('/to_index')
# def to_index():
#     return render_template('index.html', discount_names=unique_discount_names)
#
#
#
#
# @app.route('/search', methods=['POST'])
# def search_product():
#     data = request.get_json()
#     query = str(data.get('upc'))
#
#     if query:
#         product_data['System ID'] = product_data['System ID'].astype(str)
#         # Search for both UPC (string) and System ID (int)
#         matching_product_upc = product_data[product_data['UPC'] == query]
#         matching_product_id = product_data[product_data['System ID'] == query]
#
#         if not matching_product_upc.empty:
#             product_info = matching_product_upc.replace({np.nan: None}).to_dict(orient='records')[0]
#         elif not matching_product_id.empty:
#             product_info = matching_product_id.replace({np.nan: None}).to_dict(orient='records')[0]
#         else:
#             return jsonify({'error': 'Product not found'}), 404
#
#         # Look up discount using System ID
#         system_id = product_info.get('System ID')
#         if system_id:
#             discounts_data['System ID'] = discounts_data['System ID'].astype(str)
#             discount_info = discounts_data[discounts_data['System ID'] == system_id]
#             if not discount_info.empty:
#                 discount_value = discount_info.iloc[0]['Discount']
#                 discount_taxable = bool(discount_info.iloc[0]['Discount Taxable'])
#                 discount_name = discount_info.iloc[0]['Discount Name']
#                 print('discount name', discount_name)
#                 product_info['Discount'] = discount_value if pd.notna(discount_value) else 0
#                 product_info['Discount Taxable'] = discount_taxable
#                 product_info['Discount Name'] = discount_name
#             else:
#                 product_info['Discount'] = 0
#         else:
#             product_info['Discount'] = 0
#
#         return jsonify(product_info), 200
#
#     return jsonify({'error': 'No query provided'}), 400
#
#
# @app.route('/product_search', methods=['GET'])
# def product_search():
#     query = request.args.get('query', '')
#     print('query', query)
#     if len(query) > 3:
#         query = query.lower()
#         mask = product_data['Name'].str.lower().str.contains(query)
#         results = product_data[mask][['Name', 'Price', 'UPC', 'System ID', 'Category']].replace({np.nan: ''})
#         print('results', results)
#         return jsonify(results.to_dict(orient='records'))
#     return jsonify([])
#
#
#
# @app.route('/customer_search', methods=['GET'])
# def customer_search():
#     query = request.args.get('query', '')
#     print('query', query)
#     if len(query) > 3:
#         query = query.lower()
#         mask = customer_data.apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)
#         results = customer_data[mask].replace({np.nan: ''})
#         print('return', results)
#         return jsonify(results.to_dict(orient='records'))
#     return jsonify([])
#
#
# from flask import jsonify
# import pandas as pd
#
#
# @app.route('/get_customer/<int:customer_id>', methods=['GET'])
# def get_customer(customer_id):
#     customer = customer_data[customer_data['ID'] == customer_id]
#
#     # Check if customer data is found
#     if not customer.empty:
#         customer_dict = customer.to_dict(orient='records')[0]
#
#         # Convert all NaN values to None (which will be converted to null in JSON)
#         customer_dict = {k: (None if pd.isna(v) else v) for k, v in customer_dict.items()}
#
#         print('got customer', customer_dict)  # Print the entire row for the selected customer
#         return jsonify(customer_dict)
#     else:
#         # Return a not found message if no customer is found
#         return jsonify({'error': 'Customer not found'}), 404
#
#
# @app.route('/get_offer_details', methods=['POST'])
# def get_offer_details():
#     data = request.get_json()
#     discount_name = data.get('discount_name')
#     filtered_data = discounts_data[discounts_data['Discount Name'] == discount_name][['UPC', 'Short Name', 'Size']]
#     filtered_data = filtered_data.replace({np.nan: 'None'})
#     offer_details = filtered_data.to_dict(orient='records')
#     return jsonify(offer_details)
#
# def create_receipt_pdf(items, customer_id, filename='receipt.pdf'):
#     customer_name = get_customer_name(customer_id)
#     initial_height = 3276 * mm
#     c = canvas.Canvas(filename, pagesize=(80 * mm, initial_height))
#     # Updated logo dimensions and position for centering
#     logo_width = 30 * mm
#     logo_height = 30 * mm
#     logo_x_position = (80 * mm - logo_width) / 2  # Center the logo horizontally
#     logo_y_position = initial_height - logo_height  # Top position of the logo
#     print('logo_y_position', logo_y_position)
#     # Add content and track the lowest y_position used
#     min_y_position = logo_y_position  # Track the minimum y used
#     print('initial min_y_position', min_y_position)
#
#     # Draw the logo
#     logo_path = 'static/images/The Little Pet Shoppe Square Logo_Lower Resolution@0.33x.png'
#     c.drawImage(logo_path, logo_x_position, logo_y_position, width=logo_width, height=logo_height,
#                 preserveAspectRatio=True, anchor='c')
#
#     # Adjust details start position based on new logo height
#     details_start_y_position = logo_y_position - 3 * mm  # 10 mm space below the logo
#
#     # Store details
#     c.setFont("Helvetica-Bold", 9)
#     c.drawCentredString(40 * mm, details_start_y_position, "927 Golf Course Dr,")
#     c.drawCentredString(40 * mm, details_start_y_position - 4 * mm, "Rohnert Park, CA 94928")
#     c.drawCentredString(40 * mm, details_start_y_position - 8 * mm, "Phone: (707) 293-9629")
#     c.drawCentredString(40 * mm, details_start_y_position - 12 * mm, "Email: support@littlepetexpress.com")
#
#     # Customer and order details
#     order_details_y_position = details_start_y_position - 18 * mm  # Adjust based on your content
#     c.setFont("Helvetica", 9)
#     c.drawString(5 * mm, order_details_y_position, f"Cashier: Cashier Name")
#     c.drawString(5 * mm, order_details_y_position - 4 * mm, f"Customer: {get_customer_name(customer_id)}")
#     c.drawString(5 * mm, order_details_y_position - 8 * mm, "Order #: XXXXXX")
#
#     # Items header
#     items_header_y_position = order_details_y_position - 16 * mm
#     c.setFont("Helvetica-Bold", 10)
#     c.drawString(5 * mm, items_header_y_position, "Item")
#     c.drawString(52 * mm, items_header_y_position, "Qty")
#     c.drawString(65 * mm, items_header_y_position, "Price")
#
#     # List items
#     y_position = items_header_y_position - 4 * mm
#
#     def wrap_text(text, width, canvas, font_name, font_size):
#         """Wrap text to fit within the specified width."""
#         wrapped_lines = []
#         # Split the text by words and then recombine them within the width limit
#         words = text.split()
#         line = []
#         for word in words:
#             test_line = ' '.join(line + [word])
#             if canvas.stringWidth(test_line, font_name, font_size) <= width:
#                 line.append(word)
#             else:
#                 wrapped_lines.append(' '.join(line))
#                 line = [word]
#         if line:
#             wrapped_lines.append(' '.join(line))
#         return wrapped_lines
#
#     # Build the nested dictionary
#     product_map = defaultdict(lambda: defaultdict(list))
#     for item in items:
#         system_id = item['systemId']
#         category = product_data.loc[product_data['System ID'] == system_id, 'Category'].iloc[0]
#         product_map[category][item['brand']].append(item)
#
#     for category, brands in product_map.items():
#         # Check if category is NaN or not a string
#         if pd.isna(category):
#             category = "Unknown Category"  # Default fallback for NaN or None categories
#         else:
#             category = str(category)  # Ensure category is a string
#         # Print category
#         c.setFont("Helvetica-Bold", 10)
#         c.drawString(5 * mm, y_position, category)  # Draw the category name
#
#         # Calculate the width of the text
#         text_width = c.stringWidth(category, "Helvetica-Bold", 10)
#
#         # Draw the underline
#         # Adjust the y_position offset slightly below the text (-2 mm is a general guideline)
#         c.line(5 * mm, y_position - 0.5 * mm, 5 * mm + text_width, y_position - 0.5 * mm)
#
#         y_position -= 4 * mm
#
#         for brand, items in brands.items():
#             # Print brand
#             c.setFont("Helvetica-Bold", 10)
#             c.drawString(5 * mm, y_position, brand)
#             y_position -= 4 * mm
#
#             # Print items
#             c.setFont("Helvetica", 10)
#             for item in items:
#                 item_description = f"{item['shortName']}, {item['size']}"
#                 wrapped_lines = wrap_text(item_description, 45 * mm, c, "Helvetica", 10)  # Ensure width is set properly
#
#                 for line in wrapped_lines:
#                     c.drawString(5 * mm, y_position, line)
#                     y_position -= 4 * mm  # Move down for next line or next item
#
#                 # Draw the quantity and price after the last line of the description
#                 c.drawString(52 * mm, y_position + 4 * mm, str(item['quantity']))  # Adjust as needed to align properly
#                 c.drawString(65 * mm, y_position + 4 * mm, f"${item['price']}")
#
#     y_position -= 3 * mm
#
#     def clean_currency(value):
#         """Helper function to convert currency strings to float."""
#         if isinstance(value, str):
#             # Strip any potential currency symbols and commas
#             value = value.replace('$', '').replace(',', '')
#         try:
#             return float(value)
#         except ValueError:
#             return 0.0  # Return 0.0 if conversion fails
#
#     def clean_quantity(value):
#         """Helper function to ensure quantity is an integer."""
#         try:
#             return int(value)
#         except ValueError:
#             return 0  # Return 0 if conversion fails
#
#     # Update your main computation using these helpers
#     subtotal = sum(
#         clean_currency(item['price']) * clean_quantity(item['quantity'])
#         for brand_items in product_map.values()
#         for items in brand_items.values()
#         for item in items
#     )
#     discount = sum(
#         clean_currency(item.get('discount', '0'))  # Provide a default of '0'
#         for brand_items in product_map.values()
#         for items in brand_items.values()
#         for item in items
#     )
#     tax = sum(
#         clean_currency(item.get('tax', '0'))  # Provide a default of '0'
#         for brand_items in product_map.values()
#         for items in brand_items.values()
#         for item in items
#     )
#     total = subtotal - discount + tax
#
#     # Drawing summary section
#     c.setFont("Helvetica-Bold", 10)
#     c.drawString(10 * mm, y_position, 'Subtotal:')
#     c.drawString(60 * mm, y_position, f"${subtotal:.2f}")
#     y_position -= 5 * mm
#     if discount > 0:
#         c.drawString(10 * mm, y_position, 'Discount:')
#         c.drawString(60 * mm, y_position, f"-${discount:.2f}")
#         y_position -= 5 * mm
#     c.drawString(10 * mm, y_position, 'Tax:')
#     c.drawString(60 * mm, y_position, f"${tax:.2f}")
#     y_position -= 5 * mm
#     c.drawString(10 * mm, y_position, 'Total:')
#     c.drawString(60 * mm, y_position, f"${total:.2f}")
#     y_position -= 5 * mm
#
#     c.setFont("Helvetica", 8)
#     # Footer and Thank You
#     c.drawCentredString(40 * mm, y_position, "Thank you for shopping at The Little Pet Shoppe!")
#     y_position -= 4 * mm
#     c.drawCentredString(40 * mm, y_position, "Visit www.littlepetexpress.com to shop online")
#     y_position -= 8 * mm  # Extra space before barcode
#
#     # Barcode for the order number
#     barcode = createBarcodeDrawing('Code128', value='XXXXXX', barHeight=7 * mm, width=70 * mm)
#     barcode_draw_obj = Drawing(70 * mm, 10 * mm)
#     barcode_draw_obj.add(barcode, name='barcode')
#     barcode_draw_obj.drawOn(c, 5 * mm, y_position)
#     min_y_position = min(min_y_position, y_position)
#     print('final min_y_position', min_y_position)
#
#     # Adjust the canvas size to fit the content exactly
#     final_height = initial_height - min_y_position + 10 * mm  # Add some padding
#     print('final_height', final_height)
#     c.showPage()
#     c.save()
#     return filename
#
#
#
#
#
#
#
# def get_customer_name(id):
#     try:
#         # Attempt to retrieve the customer's name using the provided ID
#         customer_name = customer_data.loc[customer_data['ID'] == id, 'Full Name'].iloc[0]
#         return customer_name
#     except IndexError:
#         # Return None or an appropriate default if no customer is found
#         return "Customer Not Found"
#
# def store_transaction(items, customer_name, customer_id):
#     print(f"Storing transaction for {customer_name}...")  # Placeholder for database storage logic
#
#
# @app.route('/print_receipt', methods=['POST'])
# def print_receipt():
#     data = request.get_json()
#     items = data['items']
#     customer_name = data['customerName']
#     customer_id = data['customerId']
#
#     print('items, customer_name, customer_id', items, customer_name, customer_id)
#
#     pdf_filename = create_receipt_pdf(items, customer_id)
#     print("pdf saved as: ", pdf_filename)
#     send_to_printer(pdf_filename)
#
#     store_transaction(items, customer_name, customer_id)
#
#     return jsonify({'success': True, 'message': 'Receipt printed successfully'})
#
# def send_to_printer(pdf_filename):
#     if os.name == 'nt':
#         # Windows printing using win32print
#         import win32print
#         import win32ui
#
#         printer_name = win32print.GetDefaultPrinter()
#         hPrinter = win32print.OpenPrinter(printer_name)
#         try:
#             hJob = win32print.StartDocPrinter(hPrinter, 1, {
#                 "pDocName": "Receipt",  # Document name appears in the print queue
#             })
#             win32print.StartPagePrinter(hPrinter)
#             with open(pdf_filename, "rb") as f:
#                 data = f.read()
#                 win32print.WritePrinter(hPrinter, data)
#             win32print.EndPagePrinter(hPrinter)
#             win32print.EndDocPrinter(hPrinter)
#         finally:
#             win32print.ClosePrinter(hPrinter)
#
#     elif os.name == 'posix':
#         import cups
#
#         # Establish a connection to CUPS
#         conn = cups.Connection()
#         printer_name = 'Receipt_Printer'  # Ensure this matches your printer's name in CUPS
#
#         print('Sending', pdf_filename, 'to the printer')
#
#         # Printing options to prevent cash drawer from opening
#         options = {
#             "CashDrawer": "0NoCashDrawer",  # Setting to prevent cash drawer from opening
#             "PageSize": "X80mmY3276mm",  # Example, set page size if needed
#         }
#
#         # Print the PDF file with specified options to control the cash drawer and other aspects
#         job_id = conn.printFile(printer_name, pdf_filename, "Receipt", options)
#         print(f'Print job {job_id} sent to {printer_name} with cash drawer control.')
#
#         return job_id
#
#
# if os.name == 'nt':
#
#     import win32print
#
#
#     # ESC/POS command to open the cash drawer (Common command)
#     OPEN_DRAWER = b'\x1B\x70\x00\x19\xFA'  # This command is likely correct, but verify with your printer manual
#
#
#     def open_cash_drawer_direct():
#         printer_name = 'Receipt Printer'  # Replace with your actual printer name
#
#         # Open the printer
#         hprinter = win32print.OpenPrinter(printer_name)
#
#         try:
#             # Start a raw print job
#             hJob = win32print.StartDocPrinter(hprinter, 1, ("Open Cash Drawer", None, "RAW"))
#             win32print.StartPagePrinter(hprinter)
#
#             # Send the command to open the drawer
#             win32print.WritePrinter(hprinter, OPEN_DRAWER)
#
#             # End the raw print job
#             win32print.EndPagePrinter(hprinter)
#             win32print.EndDocPrinter(hprinter)
#         finally:
#             # Close the printer handle
#             win32print.ClosePrinter(hprinter)
#
#
#     @app.route('/open_cash_drawer', methods=['POST'])
#     def open_cash_drawer():
#         try:
#             open_cash_drawer_direct()  # Call the function to open the cash drawer
#             return jsonify({'status': 'success', 'message': 'Cash drawer opened.'})
#         except Exception as e:
#             return jsonify({'status': 'error', 'message': str(e)}), 500
#
# elif os.name == 'posix':
#     # ESC/POS command to open the cash drawer
#     OPEN_DRAWER = b'\x1B\x70\x00\x19\xFA'
#
#
#     def open_cash_drawer_direct():
#         printer_name = 'Receipt_Printer'
#         conn = cups.Connection()
#         printers = conn.getPrinters()
#
#         if printer_name not in printers:
#             raise Exception("Printer not found.")
#
#         # Using a named temporary file to send raw commands
#         with tempfile.NamedTemporaryFile("wb", delete=True) as tmp:
#             # Write the raw command to open the drawer
#             tmp.write(OPEN_DRAWER)
#             tmp.flush()  # Ensure data is written
#
#             # Printing options to prevent cash drawer from opening
#             options = {
#                 'raw': 'True',
#                 "CashDrawer": "1CashDrawer1BeforePrinting"
#             }
#             # Print the file using raw option
#             job_id = conn.printFile(printer_name, tmp.name, "Open Cash Drawer", options)
#             print(f"Job {job_id} sent to printer.")
#
#             # Check the job status to ensure it's completed or handle it accordingly
#             completed = False
#             for i in range(5):  # Check status up to 5 times
#                 jobs = conn.getJobs()
#                 if job_id not in jobs:
#                     completed = True
#                     break
#                 time.sleep(1)  # Wait a second between checks
#
#             if not completed:
#                 conn.cancelJob(job_id, purge_job=True)
#                 raise Exception("Failed to complete the drawer opening job.")
#
#
#     @app.route('/open_cash_drawer', methods=['POST'])
#     def open_cash_drawer():
#         try:
#             open_cash_drawer_direct()
#             return jsonify({'status': 'success', 'message': 'Cash drawer opened.'})
#         except Exception as e:
#             return jsonify({'status': 'error', 'message': str(e)}), 500
#
#
# if __name__ == '__main__':
#     app.run(debug=True)









    # @app.route('/search', methods=['POST'])
    # def search_product():
    #     data = request.get_json()
    #     upc = str(data.get('upc'))
    #     if upc:
    #         matching_product = product_data[product_data['UPC'] == upc]
    #         if not matching_product.empty:
    #             product_info = matching_product.replace({np.nan: None}).to_dict(orient='records')[0]
    #
    #             # Look up discount using System ID
    #             system_id = product_info.get('System ID')
    #             if system_id:
    #                 discount_info = discounts_data[discounts_data['System ID'] == system_id]
    #                 if not discount_info.empty:
    #                     discount_value = discount_info.iloc[0]['Discount']
    #                     product_info['Discount'] = discount_value if pd.notna(discount_value) else 0
    #                 else:
    #                     product_info['Discount'] = 0
    #             else:
    #                 product_info['Discount'] = 0
    #
    #             return jsonify(product_info), 200
    #         else:
    #             return jsonify({'error': 'Product not found'}), 404
    #     return jsonify({'error': 'No UPC provided'}), 400

    # @app.route('/print_receipt', methods=['POST'])
    # def print_receipt():
    #     data = request.get_json()
    #     items = data['items']
    #     customer_name = data['customerName']
    #     customer_id = data['customerId']
    #
    #     print('items, customer_name, customer_id', items, customer_name, customer_id)
    #     # Here you would format the receipt text and send the command to the printer
    #     receipt_text = format_receipt(items, customer_id)
    #     send_to_printer(receipt_text)
    #
    #     # Optionally, store the transaction in the database
    #     store_transaction(items, customer_name, customer_id)
    #
    #     return jsonify({'success': True, 'message': 'Receipt printed successfully'})
    #
    #
    # def format_receipt(items, customer_id):
    #     # Implement receipt formatting here suitable for 80mm receipt
    #     receipt_lines = []
    #     receipt_lines.append(f"Customer: {customer_name} (ID: {customer_id})\n")
    #     for item in items:
    #         receipt_lines.append(f"{item['brand']} {item['shortName']} {item['size']}")
    #         receipt_lines.append(f"Qty: {item['quantity']} Price: {item['price']} Discount: {item['discount']}\n")
    #     return '\n'.join(receipt_lines)
    # import usb.core
    # import usb.util
    # @app.route('/open_cash_drawer', methods=['POST'])
    # def open_cash_drawer():
    #     try:
    #         # Vendor and Product IDs should be replaced with those of your printer
    #         vendor_id = 0x811e
    #         product_id = 0x0fe6
    #
    #         # Find the printer
    #         printer = usb.core.find(idVendor=vendor_id, idProduct=product_id)
    #         print('printer', printer)
    #
    #         if printer is None:
    #             raise ValueError("Printer not found")
    #
    #         # Detach kernel driver if necessary
    #         if printer.is_kernel_driver_active(0):
    #             printer.detach_kernel_driver(0)
    #
    #         # Set the active configuration
    #         printer.set_configuration()
    #
    #         # ESC/POS command to open the drawer
    #         drawer_command = b'\x1B\x70\x00\x19\xFA'
    #
    #         # Send the command to the endpoint
    #         endpoint = printer[0][(0, 0)][0]
    #         print('sending command to open cash drawer')
    #         printer.write(endpoint.bEndpointAddress, drawer_command)
    #
    #         return jsonify({'status': 'success', 'message': 'Cash drawer opened.'})
    #
    #     except Exception as e:
    #         return jsonify({'status': 'error', 'message': str(e)}), 500

# def open_cash_drawer():
#     try:
#         # Send the command to open the cash drawer
#         command = 'echo -e "\\x1B\\x70\\x00\\x19\\xFA" | lp -d USB_80Series2_2'
#         subprocess.run(command, shell=True)
#
#         # Optional: reset the USB connection or clear the printer queue
#         subprocess.run("lpstat -o | awk '{print $1}' | xargs cancel", shell=True)  # Clear print jobs
#         subprocess.run(
#             "lpadmin -x USB_80Series2_2 && lpadmin -p USB_80Series2_2 -v usb://USB/80Series2?serial=GD2078D8374DD0937",
#             shell=True)  # Reset USB connection
#
#         print("Cash drawer command sent successfully.")
#
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
# @app.route('/open_cash_drawer', methods=['POST'])
# def open_cash_drawer_route():
#     open_cash_drawer()
#     return jsonify({"status": "success", "message": "Cash drawer opened."})








# //const cartItems = {};
# //let grossSales = 0;
# //let totalTax = 0;
# //let netSales = 0;
# //let discountAmount = 0;
# //let taxableSale = 0;
# //let isFromBarcode = false;  // Flag to track the source of the UPC
# //
# //async function searchProduct(upc) {
# //    const successSound = new Audio('static/sound/Success.wav');
# //    const errorSound = new Audio('static/sound/Fail.wav');
# //    if (upc) {
# //        console.log('upc', upc)
# //        try {
# //            const response = await fetch('/search', {
# //                method: 'POST',
# //                headers: {
# //                    'Content-Type': 'application/json'
# //                },
# //                body: JSON.stringify({ upc: upc })
# //            });
# //
# //            const responseText = await response.text(); // Get the response as text
# //            console.log('Response text:', responseText); // Log the response text
# //
# //            if (!response.ok) {
# //                throw new Error('Network response was not ok');
# //            }
# //
# //            const productInfo = JSON.parse(responseText); // Parse the response text as JSON
# //            console.log('Product found:', productInfo);
# //
# //            addToCartTable(productInfo);
# //
# //            successSound.play();
# //
# //            // Clear the search input field if the UPC came from the search input
# //            if (!isFromBarcode) {
# //                document.querySelector('.search-input').value = '';
# //            }
# //
# //            // Reset the flag
# //            isFromBarcode = false;
# //            // Focus the search input
# //            focusSearchInput();
# //        } catch (error) {
# //            console.error('Error:', error);
# //            document.querySelector('.error-bar').style.display = 'block'; // Show error bar
# //            document.querySelector('.error-bar').textContent = 'Item not Found!';
# //            errorSound.play();
# //            // Optionally, hide the error bar after some time
# //            setTimeout(() => {
# //                document.querySelector('.error-bar').style.display = 'none';
# //            }, 3000);
# //        }
# //    } else {
# //        console.error('Please enter a UPC.');
# //    }
# //}
# //
# //function adjustAvailableOffersHeight() {
# //    const tableBody = document.querySelector('.cart-items-table tbody');
# //    const availableOffers = document.querySelector('.available-offers');
# //    if (tableBody.children.length > 0) {
# //        availableOffers.style.height = '30%';
# //    } else {
# //        availableOffers.style.height = 'auto';
# //    }
# //}
# //
# //function updateTotalTableVisibility() {
# //    const cartTableContainer = document.querySelector('.cart-table');
# //    const customerContainer = document.querySelector('.customer-container');
# //    const totalTableContainer = document.querySelector('.total-table-container');
# //    const fixedBottomBar = document.querySelector('.fixed-bottom-bar');
# //
# //    if (cartTableContainer.classList.contains('has-rows')) {
# //        totalTableContainer.style.display = 'block';
# //        fixedBottomBar.style.display = 'flex';
# //        cartTableContainer.style.maxHeight = '90%'
# //        customerContainer.style.maxHeight = '90%'
# //    } else {
# //        totalTableContainer.style.display = 'none';
# //        fixedBottomBar.style.display = 'none';
# //        cartTableContainer.style.maxHeight = '100%'
# //        customerContainer.style.maxHeight = '100%'
# //    }
# //}
# //
# //function addToCartTable(product) {
# //    const tableBody = document.querySelector('.cart-items-table tbody');
# //    const upc = product.UPC;
# //    const price = parseFloat(product.Price);
# //    const brand = product.Brand;
# //    const shortName = product['Short Name'];
# //    const size = product.Size;
# //    const taxRate = 0.09;
# //    const pets = product.Pets;
# //    const discount = product.Discount || 0; // Default to 0 if no discount
# //    let discount_name;
# //    console.log('discount amount here', discount)
# //    const systemId = product['System ID']
# //    if (discount > 0) {
# //        discount_name = product['Discount Name'];
# //        discount_name = discount_name.split('|')[1].trim();
# //        // Check if discount_name starts with 'Get ' and remove it
# //        if (discount_name.startsWith('Get ')) {
# //            discount_name = discount_name.replace(/^Get\s+/, '');
# //        }
# //    }
# //    console.log('discount_name:', discount_name);
# //    const discount_taxable = product['Discount Taxable'];
# //    console.log('discount_taxable:', discount_taxable);
# //    const garbageIconUrl = document.getElementById('garbage-icon-url').getAttribute('data-url');
# //    let tax;
# //
# //    let itemColumnContent = '';
# //    if (brand) {
# //        itemColumnContent += `<div style="font-size: 0.9em;"><strong>${brand}</strong></div>`;
# //    }
# //    if (shortName) {
# //        itemColumnContent += `<div style="font-size: 0.8em;">${shortName}</div>`;
# //    }
# //    if (size) {
# //        itemColumnContent += `<div style="font-size: 0.6em;">${size} | ${pets}</div>`;
# //    } else {
# //        itemColumnContent += `<div style="font-size: 0.6em;">${pets}</div>`;
# //    }
# //
# //    let quantity = 1;
# //
# //    if (cartItems[upc]) {
# //        const existingRow = cartItems[upc].row;
# //        quantity = cartItems[upc].quantity + 1;
# //        const quantityInput = existingRow.querySelector('.quantity-column input');
# //        quantityInput.value = quantity;
# //        existingRow.querySelector('.discounts-column').innerText = discount.toFixed(2);
# //        if (!discount_taxable) {
# //            tax = (price - discount)* quantity * taxRate;
# //        }
# //        else {
# //            tax = price * quantity * taxRate;
# //        }
# //
# //        existingRow.querySelector('.tax-column').innerText = tax.toFixed(2);
# //        const total = (price * quantity) + tax;
# //        existingRow.querySelector('.total-column').innerText = total.toFixed(2);
# //        cartItems[upc].quantity = quantity;
# //    } else {
# //        if (!discount_taxable) {
# //            tax = (price - discount)* quantity * taxRate;
# //        }
# //        else {
# //            tax = price * quantity * taxRate;
# //        }
# //        const total = (price * quantity) + tax;
# //
# //        document.querySelector('.cart-table').classList.add('has-rows');
# //        const row = document.createElement('tr');
# //        row.className = 'cart-item-row';
# //        row.setAttribute('data-upc', upc);
# //        row.setAttribute('data-system-id', systemId);
# //
# //
# //        row.innerHTML = `
# //            <td class="item-column">
# //                ${itemColumnContent}
# //            </td>
# //            <td class="price-column">
# //                ${discount > 0
# //                    ? `<span class="original-price" style="text-decoration: line-through;">${price.toFixed(2)}</span><br>
# //                       <span class="discounted-price">${(price - discount).toFixed(2)}</span>`
# //                    : `<span class="original-price">${price.toFixed(2)}</span>`
# //                }
# //            </td>
# //            <td class="quantity-column">
# //                <input type="number" value="${quantity}" min="1" />
# //            </td>
# //            <td class="discounts-column ${discount > 0 ? (discount_taxable ? 'taxable' : 'non-taxable') : ''}">
# //                <span style="line-height: 1;">${discount.toFixed(2)}</span>
# //                ${discount > 0 ? `<br><span class="discount-name">${discount_name}</span>` : ''}
# //            </td>
# //            <td class="tax-column">${tax.toFixed(2)}</td>
# //            <td class="total-column">
# //                ${discount > 0 ? (total - discount * quantity).toFixed(2) : total.toFixed(2)}
# //            </td>
# //            <td class="empty-column">
# //                <img src="${garbageIconUrl}" class="delete-icon row" alt="Delete">
# //            </td>
# //        `;
# //        row.querySelector('.delete-icon.row').addEventListener('click', () => {
# //            removeFromCart(upc);
# //            adjustAvailableOffersHeight();
# //            updateTotalTableVisibility();
# //        });
# //        // Add event listener to select text on focus
# //        row.querySelector('.quantity-column input').addEventListener('click', function() {
# //            this.select();
# //            const input = this;
# //            input.addEventListener('wheel', function(event) {
# //                event.preventDefault();
# //                const delta = Math.sign(event.deltaY);
# //                const newQuantity = Math.max(1, parseInt(input.value, 10) - delta * 1);
# //                input.value = newQuantity;
# //                cartItems[upc].quantity = newQuantity;
# //                updateRowValues(row, price, taxRate, discount, newQuantity, discount_taxable);
# //                updateSummaryTable();
# //            }, { passive: false });
# //        });
# //
# //
# //
# //        // Add event listener to update total on quantity change
# //        row.querySelector('.quantity-column input').addEventListener('change', function() {
# //            const newQuantity = parseInt(this.value, 10);
# //            cartItems[upc].quantity = newQuantity;
# //            updateRowValues(row, price, taxRate, discount, newQuantity, discount_taxable);
# //            updateSummaryTable();
# //        });
# //
# //
# //
# //
# //        tableBody.prepend(row);
# //        cartItems[upc] = { row: row, quantity: quantity };
# //    }
# //
# //    // Update summary table
# //    updateSummaryTable();
# //    adjustAvailableOffersHeight();
# //    updateTotalTableVisibility();
# //}
# //
# ////function removeFromCart(upc) {
# ////    const item = cartItems[upc];
# ////    if (item) {
# ////        item.row.remove();
# ////        delete cartItems[upc];
# ////        // Update summary table
# ////        updateSummaryTable();
# ////        adjustAvailableOffersHeight();
# ////        updateTotalTableVisibility();
# ////    }
# ////}
# //
# //function removeFromCart(upc) {
# //    const item = cartItems[upc];
# //    if (item) {
# //        item.row.remove();
# //        delete cartItems[upc];
# //
# //        // Check if the cart is empty
# //        const tableBody = document.querySelector('.cart-items-table tbody');
# //        const cartTableContainer = document.querySelector('.cart-table');
# //        console.log('tableBody.children.length', tableBody.children.length)
# //        if (tableBody.children.length === 0) {
# //            cartTableContainer.classList.remove('has-rows');
# //        }
# //
# //        // Update summary table
# //        updateSummaryTable();
# //        adjustAvailableOffersHeight(); // Adjust height when item is removed
# //        updateTotalTableVisibility(); // Update visibility when item is removed
# //    }
# //}
# //
# //function updateSummaryTable() {
# //    grossSales = 0;
# //    totalTax = 0;
# //    netSales = 0;
# //    discountAmount = 0;
# //    taxableSale = 0;
# //
# //    Object.keys(cartItems).forEach(upc => {
# //        const item = cartItems[upc];
# //        const originalPrice = parseFloat(item.row.querySelector('.original-price').innerText);
# //        const discountedPriceElement = item.row.querySelector('.discounted-price');
# //        const discountedPrice = discountedPriceElement ? parseFloat(discountedPriceElement.innerText) : false;
# //        console.log('discounted-price', discountedPrice)
# //        const discount = parseFloat(item.row.querySelector('.discounts-column').innerText);
# //        const discountElement = item.row.querySelector('.discounts-column');
# //        console.log('class list', discountElement.className)
# //        const discount_taxable = discountElement.classList.contains('taxable') ? true : false;
# //        const quantity = item.quantity;
# //        const tax = parseFloat(item.row.querySelector('.tax-column').innerText);
# //
# //
# //        grossSales += originalPrice * quantity;
# //        discountAmount += discount * quantity;
# //
# //        if (discountedPrice) {
# //            netSales += discountedPrice * quantity;
# //        }
# //        else {
# //            netSales += originalPrice * quantity;
# //        }
# //
# //
# //        totalTax += tax;
# //
# //        console.log('discount_taxable', discount_taxable)
# //
# //
# //        if (discount_taxable) {
# //            console.log('executed 1st')
# //            taxableSale += originalPrice * quantity;
# //        } else if (discountedPrice) {
# //            console.log('executed 2nd')
# //            taxableSale += discountedPrice * quantity;
# //        } else {
# //            console.log('executed 3rd')
# //            taxableSale += originalPrice * quantity;
# //        }
# //
# //        console.log('taxableSale', taxableSale)
# //
# //
# //    });
# //
# //    const total = netSales + totalTax;
# //
# //    document.querySelector('.total-table-amount.gross-sale').innerText = grossSales.toFixed(2);
# //    document.querySelector('.total-table-amount.discounts').innerText = discountAmount.toFixed(2);
# //    document.querySelector('.total-table-amount.net-sale').innerText = netSales.toFixed(2);
# //    document.querySelector('.total-table-amount.taxable-sales').innerText = taxableSale.toFixed(2);
# //    document.querySelector('.total-table-amount.total-tax').innerText = totalTax.toFixed(2);
# //    document.querySelector('.total-table-amount-total.total').innerText = total.toFixed(2);
# //
# //    document.querySelector('.payment-section .total-amount').innerText = total.toFixed(2);
# //}
# //
# //function focusSearchInput() {
# //    const searchInput = document.querySelector('.search-input');
# //    if (document.activeElement !== searchInput) {
# //        searchInput.focus();
# //    }
# //}
# //
# //function focusAndEraseSearchInput() {
# //    const searchInput = document.querySelector('.search-input');
# //    searchInput.value = '';
# //    if (document.activeElement !== searchInput) {
# //        searchInput.focus();
# //    }
# //}
# //
# //function updateRowValues(row, price, taxRate, discount, quantity, discount_taxable) {
# //    let tax;
# //    if (!discount_taxable) {
# //        tax = (price - discount) * quantity * taxRate;
# //    } else {
# //        tax = price * quantity * taxRate;
# //    }
# //
# //    const total = (price * quantity) + tax - (discount * quantity);
# //
# //    row.querySelector('.tax-column').innerText = tax.toFixed(2);
# //    row.querySelector('.total-column').innerText = total.toFixed(2);
# //    row.querySelector('.discounts-column').innerText = discount.toFixed(2);
# //}
# //
# //
# //document.addEventListener('DOMContentLoaded', () => {
# //    const searchInput = document.querySelector('.search-input');
# //
# //    // Initialize variables to capture barcode input
# //    let barcode = '';
# //    let lastKeyTime = Date.now();
# //    let isFromBarcode = false;  // Track whether the input is from the barcode scanner
# //
# //    // Function to process the input (from barcode scanner or search box)
# //    function processInput(input) {
# //        if (input.length > 0) {
# //            searchProduct(input);
# //            searchInput.value = ''; // Clear the search input
# //            barcode = ''; // Clear the barcode
# //        }
# //    }
# //
# //    // Function to handle barcode input
# //    function handleBarcodeInput(event) {
# //        const currentTime = Date.now();
# //        if (currentTime - lastKeyTime > 100) {
# //            barcode = '';
# //        }
# //        lastKeyTime = currentTime;
# //
# //        if (event.key !== 'Enter') {
# //            barcode += event.key;
# //        } else {
# //            if (barcode.length > 0) {
# //                isFromBarcode = true;  // Set the flag to indicate barcode input
# //                processInput(barcode);
# //                isFromBarcode = false; // Reset the flag after processing
# //            }
# //        }
# //    }
# //
# //    // Listen for keypress events globally
# //    document.addEventListener('keydown', handleBarcodeInput);
# //
# //    // Listen for Enter key press on the search input
# //    searchInput.addEventListener('keydown', (event) => {
# //        if (event.key === 'Enter') {
# //            const upc = searchInput.value;
# //            processInput(upc);
# //        }
# //    });
# //
# //    // Focus the search input
# //    focusSearchInput();
# //    updateTotalTableVisibility();
# //
# //});
# //
# //
# //// Debugging statement to ensure jQuery is loaded
# //console.log('jQuery version:', $.fn.jquery);
# //
# //$(document).ready(function() {
# //    console.log('Document is ready');
# //    $('#customer-search-input').on('input', function() {
# //        console.log('Input event triggered');
# //        let query = $(this).val().trim();
# //        console.log('Query:', query);
# //        if (query.length > 3) {
# //            $.ajax({
# //                url: '/customer_search',
# //                method: 'GET',
# //                data: { query: query },
# //                success: function(data) {
# //                    console.log('Data received:', data);
# //                    let suggestions = $('.suggestions');
# //                    suggestions.empty();
# //                    if (data.length > 0) {
# //                        data.forEach(function(item) {
# //                            suggestions.append(`<li data-id="${item.ID}">${item.Name} (${item.Email}, ${item.Phone})</li>`);
# //                        });
# //                        suggestions.show();
# //                    } else {
# //                        suggestions.hide();
# //                    }
# //                },
# //                error: function(xhr, status, error) {
# //                    console.error('Error fetching data:', error);
# //                    $('.suggestions').hide();
# //                }
# //            });
# //        } else {
# //            $('.suggestions').hide();
# //        }
# //    });
# //
# //
# //    $(document).on('click', '.suggestions li', function() {
# //        let customer_id = $(this).data('id');
# //
# //        $.ajax({
# //            url: `/get_customer/${customer_id}`,
# //            method: 'GET',
# //            success: function(data) {
# //                console.log('Customer data:', data);
# //
# //                // Update the customer information and store the ID
# //                $('#customer-name').text(data['Full Name']).data('customer-id', customer_id);
# //                $('#customer-email').text(data.Email);
# //                $('#customer-phone').text(data.Phone);
# //
# //                // Display the customer info and hide other elements
# //                $('.customer-search-container').hide();
# //                $('.new-customer-button').hide();
# //                $('#customer-info-container').show();
# //
# //                // Clear the input
# //                $('#customer-search-input').val('');
# //            },
# //            error: function(xhr, status, error) {
# //                console.error('Error fetching customer data:', error);
# //            }
# //        });
# //        $('.suggestions').hide();
# //    });
# //
# //
# //
# //
# //    $('#crossButton').on('click', function() {
# //        $('.customer-search-container').show();
# //        $('.new-customer-button').show();
# //        $('#customer-info-container').hide();
# //    });
# //
# //    // Product search
# //    $('.search-input').on('input', function() {
# //        console.log('Product input event triggered');
# //        let query = $(this).val().trim();
# //        console.log('Product Query:', query);
# //        if (query.length > 3) {
# //            $.ajax({
# //                url: '/product_search',
# //                method: 'GET',
# //                data: { query: query },
# //                success: function(data) {
# //                    console.log('Product Data received:', data);
# //                    let product_suggestions = $('.product-suggestions');
# //                    product_suggestions.empty();
# //                    if (data.length > 0) {
# //                        data.forEach(function(item) {
# //                            console.log('Item:', item); // Check individual item
# //                            product_suggestions.append(`<li data-system-id="${item['System ID']}">${item.Name} - $${item.Price}</li>`);
# //                            console.log('Suggestions:', `<li data-system-id="${item['System ID']}">${item.Name} - $${item.Price}</li>`);
# //                        });
# //                        product_suggestions.show();
# //                    } else {
# //                        product_suggestions.hide();
# //                    }
# //                },
# //                error: function(xhr, status, error) {
# //                    console.error('Error fetching product data:', error);
# //                }
# //            });
# //        } else {
# //            $('.product-suggestions').hide();
# //        }
# //    });
# //
# //    // Handle product suggestion click
# //    $(document).on('click', '.product-suggestions li', function() {
# //        let systemId = $(this).data('system-id');
# //        console.log('Selected System ID:', systemId);
# //        searchProduct(systemId); // Function to add the product to the cart
# //        focusAndEraseSearchInput()
# //        $('.product-suggestions').hide();
# //    });
# //
# //});
# //
# //
# //
# //
# //document.getElementById('manageInventoryButton').addEventListener('click', function() {
# //    var url = this.getAttribute('data-url');
# //    window.location.href = url;
# //});
# //
# //
# //$(document).ready(function() {
# //    $('.offer').click(function() {
# //        const discountName = $(this).data('discount-name');
# //        const offerDetails = $(this).find('.offer-details');
# //
# //        if (offerDetails.is(':visible')) {
# //            offerDetails.hide();
# //        } else {
# //            $.ajax({
# //                url: '/get_offer_details',
# //                type: 'POST',
# //                contentType: 'application/json',
# //                data: JSON.stringify({ discount_name: discountName }),
# //                success: function(data) {
# //                    console.log('data', data)
# //                    offerDetails.empty();
# //                    const ul = $('<ul></ul>');
# //                    data.forEach(item => {
# //                        ul.append('<li>' + item['Short Name'] + (item.Size ? ' - ' + item.Size : '') + '</li>');
# //                    });
# //                    console.log('offer detail', ul)
# //                    offerDetails.append(ul);
# //                    offerDetails.show();
# //                }
# //            });
# //        }
# //    });
# //});
# //
# //
# //document.addEventListener('DOMContentLoaded', function() {
# //    // Handle input attributes
# //    const inputs = document.querySelectorAll('input[type="text"]');
# //    inputs.forEach(input => {
# //        input.setAttribute('autocomplete', 'off');
# //        input.setAttribute('autocorrect', 'off');
# //        input.setAttribute('spellcheck', 'false');
# //    });
# //
# //    // Setup popup for Finish and Pay
# //    const finishAndPayButton = document.querySelector('.finish-and-pay');
# //    const popup = document.getElementById('popup');
# //    const closePopupButton = document.getElementById('close-popup');
# //
# //    finishAndPayButton.addEventListener('click', function() {
# //        transferTableData();
# //        popup.style.display = 'flex'; // Show the popup
# //    });
# //
# //    closePopupButton.addEventListener('click', function() {
# //        popup.style.display = 'none'; // Hide the popup
# //    });
# //
# //    // Data transfer function
# //    function transferTableData() {
# //        const grossSaleValue = document.querySelector('.total-table-amount.gross-sale').innerText;
# //        const discountsValue = document.querySelector('.total-table-amount.discounts').innerText;
# //        const netSaleValue = document.querySelector('.total-table-amount.net-sale').innerText;
# //        const taxableSalesValue = document.querySelector('.total-table-amount.taxable-sales').innerText;
# //        const totalTaxValue = document.querySelector('.total-table-amount.total-tax').innerText;
# //        const totalValue = document.querySelector('.total-table-amount-total.total').innerText;
# //        const paidAmount = parseInt(document.querySelector('.order-summary-table-data.paid').innerText.replace('$', ''));
# //
# //
# //        document.querySelector('.order-summary-table-data.gross-sale').innerText = `$${grossSaleValue}`;
# //        document.querySelector('.order-summary-table-data.discounts').innerText = `$${discountsValue}`;
# //        document.querySelector('.order-summary-table-data.net-sale').innerText = `$${netSaleValue}`;
# //        document.querySelector('.order-summary-table-data.taxable-sales').innerText = `$${taxableSalesValue}`;
# //        document.querySelector('.order-summary-table-data.total-tax').innerText = `$${totalTaxValue}`;
# //        document.querySelector('.order-summary-table-data.total').innerText = `$${totalValue}`;
# //        updateTotalDue()
# //
# //
# //        var totalDueElement = document.querySelector('.order-summary-table-data.total-due');
# //        var chargeAmountElement = document.getElementById('fullAmount');
# //
# //        if (totalDueElement && chargeAmountElement) {
# //            chargeAmountElement.textContent = totalDueElement.textContent;
# //            document.getElementById('fullAmountToCard').value = totalDueElement.textContent;
# //        }
# //    }
# //
# //    // Setup print receipt popup
# //    const finishSaleButton = document.getElementById('finishSaleButton');
# //    const printReceiptPopup = document.querySelector('.print-receipt-popup');
# //    const printReceiptButton = document.querySelector('.print-receipt-button');
# //    const doNotPrintButton = document.querySelector('.do-not-print-receipt-button');
# //    const mainContent = document.getElementById('mainContent');
# //    const customAlert = document.getElementById('customAlert');
# //    const closeButton = document.querySelector('.close-btn');
# //
# ////    finishSaleButton.addEventListener('click', function() {
# ////        if (finishSaleButton.classList.contains('enabled')) {
# ////            printReceiptPopup.style.display = 'flex'; // Show the popup
# ////            mainContent.classList.add('blur-background'); // Blur the background content
# ////            printReceiptPopup.classList.add('unblur'); // Ensure popup is not blurred
# ////        } else {
# ////            alert('Please select a payment type received first!'); // Provide feedback if not enabled
# ////        }
# ////    });
# //
# //    finishSaleButton.addEventListener('click', function() {
# //        if (finishSaleButton.classList.contains('enabled')) {
# //            printReceiptPopup.style.display = 'flex'; // Show the popup
# //            mainContent.classList.add('blur-background'); // Blur the background content
# //            printReceiptPopup.classList.add('unblur'); // Ensure popup is not blurred
# //        } else {
# //            customAlert.style.display = 'flex';
# //        }
# //    });
# //
# //    closeButton.addEventListener('click', function() {
# //        customAlert.style.display = 'none';  // Hide the custom alert on close button click
# //    });
# //
# //    // Hide alert when clicking outside of it
# //    window.addEventListener('click', function(event) {
# //        if (event.target === customAlert) {
# //            customAlert.style.display = 'none';
# //        }
# //    });
# //
# //    printReceiptButton.addEventListener('click', function() {
# //        printReceiptPopup.style.display = 'none'; // Hide the popup
# //        popup.style.display = 'none'; // Hide the main popup as well
# //        mainContent.classList.remove('blur-background');
# //        // Redirect to the index page using window.location
# //        window.location.href = '/to_index';
# //    });
# //
# //    doNotPrintButton.addEventListener('click', function() {
# //        printReceiptPopup.style.display = 'none'; // Hide the popup
# //        popup.style.display = 'none'; // Hide the main popup as well
# //        mainContent.classList.remove('blur-background');
# //        // Redirect to the index page using window.location
# //        window.location.href = '/to_index';
# //    });
# //});
# //
# //function printReceipt() {
# //    const items = [];
# //    document.querySelectorAll('.cart-item-row').forEach(row => {
# //        const item = {
# //            brand: row.querySelector('.item-column strong')?.innerText || '',
# //            shortName: row.querySelector('.item-column div:nth-child(2)')?.innerText || '',
# //            size: row.querySelector('.item-column div:nth-child(3)')?.innerText.split('|')[0].trim() || '',
# //            pets: row.querySelector('.item-column div:nth-child(3)')?.innerText.split('|')[1].trim() || '',
# //            price: row.querySelector('.price-column .original-price')?.innerText || '',
# //            discount: row.querySelector('.discounts-column span')?.innerText || '0',
# //            quantity: row.querySelector('.quantity-column input')?.value || '1',
# //            tax: row.querySelector('.tax-column')?.innerText || '0',
# //            upc: row.getAttribute('data-upc'),
# //            systemId: row.getAttribute('data-system-id')
# //        };
# //        items.push(item);
# //    });
# //
# //    const customerName = $('#customer-name').text();
# //    const customerId = $('#customer-name').data('customer-id');  // Use .data() to get the stored ID
# //
# //    console.log('Customer ID:', customerId);  // Debugging to check if ID is retrieved correctly
# //
# //
# //
# //    fetch('/print_receipt', {
# //        method: 'POST',
# //        headers: {
# //            'Content-Type': 'application/json'
# //        },
# //        body: JSON.stringify({ items, customerName, customerId })
# //    }).then(response => response.json())
# //      .then(data => {
# //        if (data.success) {
# //            console.log('Receipt printing initiated.');
# //        }
# //    }).catch(error => console.error('Error printing receipt:', error));
# //}
# //
# //
# //
# //
# //document.addEventListener('DOMContentLoaded', function() {
# //    var totalAmountElement = document.querySelector('.order-summary-table-data.total');
# //    var exactCashButton = document.querySelector('.exact-cash-amount');
# //    var nextDollarButton = document.querySelector('.next-dollar');
# //    var nextLargeBillButton = document.querySelector('.next-large-bill');
# //
# //    if (totalAmountElement && exactCashButton && nextDollarButton && nextLargeBillButton) {
# //        // Function to update button text
# //        function updateButtonValue() {
# //            var totalAmountText = totalAmountElement.textContent; // e.g., "$35.74"
# //            var totalAmount = parseFloat(totalAmountText.replace('$', '')); // Convert to number
# //
# //            // Update exact cash button
# //            exactCashButton.textContent = totalAmountText;
# //
# //            // Calculate next dollar
# //            var nextDollar = Math.ceil(totalAmount);
# //            nextDollarButton.textContent = '$' + nextDollar.toFixed(2);
# //
# //            // Calculate next large bill
# //            var bills = [5, 10, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150, 200];
# //            var nextLargeBill = bills.find(bill => bill > totalAmount);
# //            if (!nextLargeBill) {
# //                nextLargeBill = Math.ceil(totalAmount / 50) * 50; // Round to next 50 increment above 200
# //            }
# //            nextLargeBillButton.textContent = '$' + nextLargeBill.toFixed(2);
# //
# //            // Hide nextLargeBillButton if it's the same as nextDollar
# //            if (nextLargeBill === nextDollar) {
# //                nextLargeBillButton.style.display = 'none';
# //            } else {
# //                nextLargeBillButton.style.display = 'inline-block'; // Make sure it's visible if not the same
# //            }
# //        }
# //
# //        // Call the function initially and set an observer for future updates
# //        updateButtonValue();
# //        var observer = new MutationObserver(function(mutations) {
# //            mutations.forEach(function(mutation) {
# //                if (mutation.type === 'childList' || mutation.type === 'characterData') {
# //                    updateButtonValue();
# //                }
# //            });
# //        });
# //
# //        // Configuration of the observer:
# //        var config = { childList: true, subtree: true, characterData: true };
# //        observer.observe(totalAmountElement, config);
# //    }
# //});
# //
# //
# //// Object to keep track of the original states of buttons and inputs
# //const buttonStates = new Map();
# //
# //function replaceButtonClass(containerSelector, classToRemove, classToAdd, exclusions, exclusionClass) {
# //    const container = document.querySelector(containerSelector);
# //    if (!container) {
# //        console.error('Container not found');
# //        return;
# //    }
# //
# //    // Select both buttons and radio inputs
# //    const elements = container.querySelectorAll('button, input[type="radio"]');
# //    elements.forEach(element => {
# //        if (!exclusions.includes(element.className)) {
# //            if (!buttonStates.has(element)) {
# //                buttonStates.set(element, {
# //                    classes: new Set(element.classList),  // Save current classes
# //                    disabled: element.disabled,  // Save the disabled state
# //                    cursor: element.style.cursor  // Save the cursor style
# //                });
# //            }
# //
# //            // Check and manage exclusionClass if specified
# //            if (exclusionClass && element.classList.contains(exclusionClass)) {
# //                element.classList.remove(exclusionClass);  // Temporarily remove exclusionClass
# //            }
# //
# //            element.classList.remove(classToRemove);
# //            element.classList.add(classToAdd);
# //            element.disabled = true;  // Disable the element
# //            element.style.cursor = 'not-allowed';  // Set cursor to not-allowed
# //        }
# //    });
# //}
# //
# //function restoreOriginalButtonStates() {
# //    buttonStates.forEach((state, element) => {
# //        element.className = ''; // Reset class names
# //        state.classes.forEach(cls => element.classList.add(cls));
# //        element.disabled = state.disabled;  // Restore the original disabled state
# //        element.style.cursor = state.cursor;  // Restore the original cursor style
# //    });
# //
# //    buttonStates.clear();  // Clear the map after restoring states
# //}
# //
# //
# //
# //
# //document.addEventListener('DOMContentLoaded', function() {
# //    const container = document.querySelector('.popup-content.payment-details');  // Adjust as necessary for your specific case
# //
# //    // Function to transform button to input and back
# //    function toggleCustomAmountInput(button) {
# //        // Check if the button has already been transformed into an input container
# //        if (button.nodeName === 'DIV' && button.classList.contains('currency-input-container')) {
# //            restoreOriginalButtonStates()
# //            // Transform back to button
# //            const originalButton = document.createElement('button');
# //            originalButton.className = 'custom-amount ready';
# //            originalButton.textContent = 'Custom';
# //            button.parentNode.replaceChild(originalButton, button);
# //        } else {
# //            replaceButtonClass('.popup-content.payment-details', 'ready', 'not-ready', ['custom-amount'], 'active')
# //            // Transform to input container
# //            const inputContainer = document.createElement('div');
# //            inputContainer.className = 'currency-input-container';
# //
# //            const input = document.createElement('input');
# //            input.type = 'text';
# //            input.className = 'currency-input';
# //            input.placeholder = '$0.00';
# //
# //            const removeButton = document.createElement('div');
# //            removeButton.className = 'remove-custom-amount';
# //            removeButton.innerHTML = `<img src="/static/images/garbage icon.png" alt="Remove">`;
# //            removeButton.style.cursor = 'pointer';
# //
# //            inputContainer.appendChild(input);
# //            inputContainer.appendChild(removeButton);
# //            button.parentNode.replaceChild(inputContainer, button);
# //
# //            input.focus();
# //            input.addEventListener('click', () => input.select());
# //
# //            removeButton.addEventListener('click', function() {
# //                toggleCustomAmountInput(inputContainer); // Toggle back to button when remove is clicked
# //            });
# //
# //            input.addEventListener('input', function() {
# //                let value = input.value.replace(/[^0-9]/g, '');
# //                if (value === '') {
# //                    input.value = '$0.00';
# //                } else {
# //                    value = value.padStart(3, '0');
# //                    let integerPart = value.slice(0, -2);
# //                    let decimalPart = value.slice(-2);
# //                    integerPart = parseInt(integerPart, 10).toString();
# //                    input.value = '$' + integerPart + '.' + decimalPart;
# //                }
# //            });
# //        }
# //    }
# //
# //    // Delegate click events within the container
# //    container.addEventListener('click', function(event) {
# //        if (event.target.matches('.custom-amount.ready')) {
# //            toggleCustomAmountInput(event.target);
# //        } else if (event.target.closest('.remove-custom-amount')) {
# //            // Handles click on the remove button if it's within an input container
# //            const inputContainer = event.target.closest('.currency-input-container');
# //            if (inputContainer) {
# //                toggleCustomAmountInput(inputContainer);
# //            }
# //        }
# //    });
# //});
# //
# //
# //document.addEventListener('DOMContentLoaded', function() {
# //    const buttons = document.querySelectorAll('.popup-content.payment-details button');
# //
# //    buttons.forEach(button => {
# //        // Use capturing phase to handle the event first
# //        button.addEventListener('click', function(event) {
# //            if (this.classList.contains('not-ready')) {
# //                console.log('Button click prevented due to not-ready state.');
# //                event.preventDefault(); // Prevent default button action
# //                event.stopImmediatePropagation(); // Prevent any further handlers from executing
# //            }
# //        }, true); // True sets the listener to capture phase
# //    });
# //});
# //
# //
# //document.addEventListener('DOMContentLoaded', function() {
# //    const buttons = document.querySelectorAll('.popup-content.payment-details button.ready:not(.custom-amount)');
# //
# //    buttons.forEach(button => {
# //        // Ensure this runs after the above prevention logic in the bubbling phase
# //        button.addEventListener('click', function() {
# //            if (!this.classList.contains('not-ready')) { // Only toggle if not prevented
# //                if (this.classList.contains('active')) {
# //                    this.classList.remove('active');
# //                    this.classList.add('ready');
# //                } else {
# //                    this.classList.add('active');
# //                    this.classList.remove('ready');
# //                }
# //            }
# //        });
# //    });
# //});
# //
# //document.addEventListener('DOMContentLoaded', function() {
# //    // Selector for all potential buttons
# //    const buttonSelectors = [
# //        '.payment-processed-button',
# //        '.exact-cash-amount',
# //        '.next-dollar',
# //        '.next-large-bill'
# //    ];
# //
# //    // Function to handle button click
# //    function handleButtonClick(button) {
# //        if (button) { // Check if the button actually exists
# //            button.addEventListener('click', function() {
# //                if (this.classList.contains('active')) {
# //                    replaceButtonClass(
# //                            '.popup-content.payment-details',
# //                            'ready',
# //                            'not-ready',
# //                            [this.className],  // Exclude this button
# //                            'active'  // Optionally manage 'active' class
# //                        );
# //
# //                } else if (this.classList.contains('ready')) {
# //                    // Button is currently active, restore all button states
# //                    restoreOriginalButtonStates();
# //
# //                }
# //            });
# //        }
# //    }
# //
# //    // Attach the event listener to each button if it exists
# //    buttonSelectors.forEach(selector => {
# //        const button = document.querySelector(selector);
# //        handleButtonClick(button);
# //    });
# //});
# //
# //
# //
# //
# //
# //document.addEventListener('DOMContentLoaded', function() {
# //    const buttonSelectors = ['.exact-cash-amount', '.next-dollar', '.next-large-bill'];
# //    const paidAmountElement = document.querySelector('.order-summary-table-data.paid');
# //    const inputContainer = document.querySelector('.process-cash-payment'); // Assuming input appears here
# //
# //    if (!paidAmountElement) {
# //        console.error('Paid amount display element not found');
# //        return;
# //    }
# //
# //    function updatePaidAmountFromButton(button) {
# //        button.addEventListener('click', function() {
# //            if (this.classList.contains('active')) {
# //                const amount = this.textContent.trim();
# //                paidAmountElement.textContent = amount;
# //            }
# //        });
# //    }
# //
# //    buttonSelectors.forEach(selector => {
# //        const buttons = document.querySelectorAll(selector);
# //        buttons.forEach(button => updatePaidAmountFromButton(button));
# //    });
# //
# //    // Observe changes in the container to handle dynamic addition/removal of input
# //    const observer = new MutationObserver(mutations => {
# //        mutations.forEach(mutation => {
# //            if (mutation.addedNodes.length) {
# //                mutation.addedNodes.forEach(node => {
# //                    if (node.classList && node.classList.contains('currency-input-container')) {
# //                        const input = node.querySelector('.currency-input');
# //                        input.addEventListener('input', () => {
# //                            paidAmountElement.textContent = input.value;
# //                            updateTotalDue();
# //                        });
# //                    }
# //                });
# //            }
# //            if (mutation.removedNodes.length) {
# //                mutation.removedNodes.forEach(node => {
# //                    if (node.classList && node.classList.contains('currency-input-container')) {
# //                        paidAmountElement.textContent = '$0.00'; // Reset when input is removed
# //                        updateTotalDue();
# //                    }
# //                });
# //            }
# //        });
# //    });
# //
# //    // Configuration for the observer
# //    const config = { childList: true, subtree: true };
# //    observer.observe(inputContainer, config);
# //});
# //
# //
# //function updateTotalDue() {
# //        const totalElement = document.querySelector('.total-table-amount-total.total');
# //        const paidElement = document.querySelector('.order-summary-table-data.paid');
# //        const totalDueElement = document.querySelector('.order-summary-table-data.total-due');
# //        const totalDueHeader = document.querySelector('.order-summary-table-data-header.total-due');
# //        let totalValue = parseFloat(totalElement.innerText.replace('$', ''));
# //        let paidAmount = parseFloat(paidElement.innerText.replace('$', ''));
# //        let totalDue = totalValue - paidAmount;
# //
# //        // Check if totalDue is less than or equal to zero
# //        if (totalDue <= 0) {
# //            console.log('if (totalDue <= 0)')
# //            totalDueHeader.innerText = 'Change Due';
# //            totalDueHeader.style.color = '#d50912'; // Change color to red
# //            totalDueElement.innerText = `$${Math.abs(totalDue).toFixed(2)}`; // Show absolute value for change due
# //            totalDueElement.style.color = '#d50912'; // Change element color to red
# //        } else {
# //            console.log('else')
# //            totalDueHeader.innerText = 'Total Due';
# //            totalDueHeader.style.color = 'green'; // Reset header color
# //            totalDueElement.innerText = `$${totalDue.toFixed(2)}`; // Display the total due normally
# //            totalDueElement.style.color = 'green'; // Reset element color
# //        }
# //    }
# //
# //
# //document.addEventListener('DOMContentLoaded', function() {
# //    const totalElement = document.querySelector('.total-table-amount-total.total');
# //    const paidElement = document.querySelector('.order-summary-table-data.paid');
# //    const totalDueElement = document.querySelector('.order-summary-table-data.total-due');
# //    const totalDueHeader = document.querySelector('.order-summary-table-data-header.total-due');
# //
# //    // Selectors for specific buttons and inputs
# //    const paymentButtons = document.querySelectorAll('.exact-cash-amount, .next-dollar, .next-large-bill, .payment-processed-button');
# //    const currencyInput = document.querySelector('.currency-input'); // Assumes only one such input exists
# //
# //
# //
# //    paymentButtons.forEach(button => {
# //        button.addEventListener('click', function() {
# //            if (!this.classList.contains('active')) {
# //                paidElement.innerText = '$0.00';
# //            } else {
# //                if (this.classList.contains('payment-processed-button')) {
# //                    // Set to total when payment processed button is active
# //                    paidElement.innerText = totalElement.innerText;
# //                } else {
# //                    // Set to the amount of the button
# //                    paidElement.innerText = this.innerText;
# //                }
# //            }
# //            updateTotalDue();
# //        });
# //    });
# //
# //
# //    // Setup to reset paid amount if no active or currency input exists
# //    document.addEventListener('click', function(event) {
# //        if (!event.target.matches('.exact-cash-amount.active, .next-dollar.active, .next-large-bill.active, .payment-processed-button.active, .currency-input')) {
# //            if (currencyInput && currencyInput.value.trim() === '') {
# //                paidElement.innerText = '$0.00';
# //                updateTotalDue();
# //            }
# //        }
# //    });
# //
# //});
# //
# //document.addEventListener('DOMContentLoaded', function() {
# //    var drawerOpened = false;
# //    const cashDrawerButton = document.querySelector('.open-cash-drawer');
# //    const paymentButtons = document.querySelectorAll('.exact-cash-amount, .next-dollar, .next-large-bill');
# //    const inputContainer = document.querySelector('.process-cash-payment'); // Assuming the input appears here
# //    const finishSaleButton = document.querySelector('.finish-sale');
# //    var cashPaid = false;
# //
# //
# //    // Function to check and update the cash drawer button status
# //    function updateCashDrawerStatus() {
# //        let isActivePresent = Array.from(paymentButtons).some(button => button.classList.contains('active'));
# //        let currencyInput = document.querySelector('.currency-input');
# //        let isInputActive = currencyInput && currencyInput.value.trim() !== '';
# //
# //
# //        if (isActivePresent || isInputActive) {
# //            cashDrawerButton.classList.remove('not-ready');
# //            cashDrawerButton.classList.add('ready');
# //            cashDrawerButton.style.cursor = 'pointer';
# //            cashDrawerButton.disabled = false;
# //            cashPaid = true;
# //        } else {
# //            cashDrawerButton.classList.remove('ready');
# //            cashDrawerButton.classList.add('not-ready');
# //            cashPaid = false;
# //        }
# //    }
# //
# //
# //    // Attach event listeners to each payment button
# //    paymentButtons.forEach(button => {
# //        button.addEventListener('click', updateCashDrawerStatus);
# //    });
# //
# //
# //    // MutationObserver to handle dynamic addition of the input
# //    const observer = new MutationObserver(mutations => {
# //        mutations.forEach(mutation => {
# //            if (mutation.addedNodes) {
# //                mutation.addedNodes.forEach(node => {
# //                    if (node.nodeType === Node.ELEMENT_NODE && node.matches('.currency-input-container')) {
# //                        const input = node.querySelector('.currency-input');
# //                        if (input) {
# //                            input.addEventListener('input', updateCashDrawerStatus);
# //                            updateCashDrawerStatus(); // Check status immediately after input is added
# //                        }
# //                    }
# //                });
# //            }
# //        });
# //    });
# //
# //
# //    observer.observe(inputContainer, { childList: true, subtree: true });
# //
# //
# //    cashDrawerButton.addEventListener('click', function() {
# //        drawerOpened = true;
# //        if (!this.classList.contains('not-ready')) { // Only toggle if not prevented
# //            if (this.classList.contains('active')) {
# //                this.classList.remove('active');
# //                this.classList.add('ready');
# //            } else {
# //                this.classList.add('active');
# //                this.classList.remove('ready');
# //            }
# //        }
# //    });
# //
# //
# //    finishSaleButton.addEventListener('click', function() {
# //        if (finishSaleButton.classList.contains('enabled')){
# //            console.log('drawerOpened', drawerOpened)
# //            console.log('cashPaid', cashPaid)
# //            if (!drawerOpened && cashPaid) {
# //                fetch('/open_cash_drawer', { method: 'POST' })
# //                    .then(response => response.json())
# //                    .then(data => {
# //                        if (data.status === 'success') {
# //                            drawerOpened = true; // Update state to reflect the drawer is open
# //                        } else {
# //                            alert('Failed to open cash drawer: ' + data.message);
# //                        }
# //                    })
# //                    .catch(error => {
# //                        console.log('Error: ' + error.message);
# //                });
# //            }
# //        }
# //    });
# //
# //
# //    // Open cash drawer if ready
# //    cashDrawerButton.addEventListener('click', function() {
# //        if (this.classList.contains('active')) {
# //            fetch('/open_cash_drawer', { method: 'POST' })
# //                .then(response => response.json())
# //                .then(data => {
# //                    if (data.status === 'success') {
# //                        console.log('Cash drawer opened successfully.');
# //                    } else {
# //                        console.log('Failed to open cash drawer: ' + data.message);
# //                    }
# //                })
# //                .catch(error => {
# //                    console.error('Error opening cash drawer:', error);
# //                });
# //        }
# //    });
# //
# //
# //
# //
# //});
# //
# //
# //
# //document.addEventListener('DOMContentLoaded', function() {
# //    const finishSaleButton = document.getElementById('finishSaleButton');
# //    const paidAmountElement = document.querySelector('.order-summary-table-data.paid');
# //    const totalDueElement = document.querySelector('.order-summary-table-data.total');
# //
# //    // Function to convert currency string to a number
# //    function parseCurrency(currencyStr) {
# //        return parseFloat(currencyStr.replace('$', '').replace(',', ''));
# //    }
# //
# //    // Function to check and update the button state
# //    function updateFinishSaleButtonState() {
# //        let paidAmount = parseCurrency(paidAmountElement.innerText);
# //        let totalDue = parseCurrency(totalDueElement.innerText);
# //
# //        if (paidAmount >= totalDue) {
# //            finishSaleButton.classList.add('enabled');
# //        } else {
# //            finishSaleButton.classList.remove('enabled');
# //        }
# //    }
# //
# //    // Set up an observer to monitor changes in the Paid and Total elements
# //    const observer = new MutationObserver(() => {
# //        updateFinishSaleButtonState();
# //    });
# //
# //    observer.observe(paidAmountElement, { childList: true, subtree: true, characterData: true });
# //    observer.observe(totalDueElement, { childList: true, subtree: true, characterData: true });
# //
# //    // Initial check on load
# //    updateFinishSaleButtonState();
# //});
# //
# //
# //
# //
# //
# //
# //
# //
# //
# ////document.addEventListener('DOMContentLoaded', function() {
# ////    const button = document.querySelector('.custom-amount.ready');
# ////
# ////    button.addEventListener('click', function() {
# ////        const inputContainer = document.createElement('div');
# ////        inputContainer.className = 'currency-input-container';
# ////
# ////        const input = document.createElement('input');
# ////        input.type = 'text'; // Use text type for custom formatting
# ////        input.className = 'currency-input';
# ////        input.placeholder = '0.00'; // Intuitive placeholder for currency
# ////        input.style.width = '100%'; // Ensure input uses the full width of container
# ////
# ////        inputContainer.appendChild(input);
# ////        button.parentNode.replaceChild(inputContainer, button);
# ////
# ////        input.focus(); // Automatically focus the new input
# ////
# ////        // Handle input for currency formatting
# ////        input.addEventListener('input', function() {
# ////            let value = input.value.replace(/[^0-9]/g, ''); // Strip non-numeric characters
# ////            if (value === '') {
# ////                input.value = '0.00'; // Display 0.00 if no input
# ////            } else {
# ////                value = value.padStart(3, '0'); // Pad with zeros to ensure at least three digits
# ////                let integerPart = value.slice(0, -2); // Get all but the last two digits
# ////                let decimalPart = value.slice(-2); // Get the last two digits
# ////                integerPart = parseInt(integerPart, 10).toString(); // Convert to integer to remove any extra leading zeros
# ////                input.value = integerPart + '.' + decimalPart; // Combine into a final string
# ////            }
# ////        });
# ////    });
# ////});
# //
# //
# //
# //
# //
# //
# //
# //
# //
# //
# //
# ////document.addEventListener('DOMContentLoaded', function() {
# ////    const inputs = document.querySelectorAll('input[type="text"]');
# ////    inputs.forEach(input => {
# ////        input.setAttribute('autocomplete', 'off');
# ////        input.setAttribute('autocorrect', 'off');
# ////        input.setAttribute('spellcheck', 'false');
# ////    });
# ////});
# ////
# ////document.addEventListener('DOMContentLoaded', function() {
# ////    const finishAndPayButton = document.querySelector('.finish-and-pay');
# ////    const popup = document.getElementById('popup');
# ////    const closePopupButton = document.getElementById('close-popup');
# ////
# ////    finishAndPayButton.addEventListener('click', function() {
# ////        transferTableData();
# ////        popup.style.display = 'flex'; // Show the popup
# ////    });
# ////
# ////    closePopupButton.addEventListener('click', function() {
# ////        popup.style.display = 'none'; // Hide the popup
# ////    });
# ////
# ////    function transferTableData() {
# ////        // Transfer Gross Sale
# ////        const grossSaleValue = document.querySelector('.total-table-amount.gross-sale').innerText;
# ////        console.log('grossSaleValue', grossSaleValue)
# ////        document.querySelector('.order-summary-table-data.gross-sale').innerText = `$${grossSaleValue}`;
# ////
# ////        // Transfer Discounts
# ////        const discountsValue = document.querySelector('.total-table-amount.discounts').innerText;
# ////        console.log('discounts', discountsValue)
# ////        document.querySelector('.order-summary-table-data.discounts').innerText = `$${discountsValue}`;
# ////
# ////        // Transfer Net Sale
# ////        const netSaleValue = document.querySelector('.total-table-amount.net-sale').innerText;
# ////        console.log('netSaleValue', netSaleValue)
# ////        document.querySelector('.order-summary-table-data.net-sale').innerText = `$${netSaleValue}`;
# ////
# ////        // Transfer Taxable Sales
# ////        const taxableSalesValue = document.querySelector('.total-table-amount.taxable-sales').innerText;
# ////        console.log('taxableSalesValue', taxableSalesValue)
# ////        document.querySelector('.order-summary-table-data.taxable-sales').innerText = `$${taxableSalesValue}`;
# ////
# ////        // Transfer Total Tax
# ////        const totalTaxValue = document.querySelector('.total-table-amount.total-tax').innerText;
# ////        document.querySelector('.order-summary-table-data.total-tax').innerText = `$${totalTaxValue}`;
# ////
# ////        // Transfer Total
# ////        const totalValue = document.querySelector('.total-table-amount-total.total').innerText;
# ////        document.querySelector('.order-summary-table-data.total').innerText = `$${totalValue}`;
# ////
# ////        const paidAmount = parseInt(document.querySelector('.order-summary-table-data.paid').innerText.replace('$', ''));
# ////        console.log('totalValue', totalValue)
# ////        console.log('paidAmount', paidAmount)
# ////        totalDue = parseFloat(totalValue) - parseFloat(paidAmount)
# ////        console.log('totalValue - paidAmount', totalValue - paidAmount)
# ////
# ////        document.querySelector('.order-summary-table-data.total-due').innerText = `$${totalDue}`;
# ////
# ////        var totalDueElement = document.querySelector('.order-summary-table-data.total-due');
# ////        var chargeAmountElement = document.getElementById('fullAmount');
# ////
# ////        if (totalDueElement && chargeAmountElement) {
# ////            chargeAmountElement.textContent = totalDueElement.textContent;
# ////            document.getElementById('fullAmountToCard').value = totalDueElement.textContent;
# ////        }
# ////    }
# ////});
# ////
# ////
# ////document.addEventListener('DOMContentLoaded', function() {
# ////    const finishSaleButton = document.getElementById('finishSaleButton');
# ////    const printReceiptPopup = document.querySelector('.print-receipt-popup');
# ////    const doNotPrintButton = document.querySelector('.do-not-print-receipt-button');
# ////
# ////    finishSaleButton.addEventListener('click', function() {
# ////        printReceiptPopup.style.display = 'flex'; // Show the popup
# ////    });
# ////
# ////    const popup = document.getElementById('popup');
# ////
# ////    printReceiptButton.addEventListener('click', function() {
# ////        printReceiptPopup.style.display = 'none'; // Hide the popup
# ////        popup.style.display = 'none'; // Hide the popup
# ////    });
# ////    doNotPrintButton.addEventListener('click', function() {
# ////        printReceiptPopup.style.display = 'none'; // Hide the popup
# ////        popup.style.display = 'none'; // Hide the popup
# ////    });
# ////
# ////});
# ////
