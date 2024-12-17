from flask import Flask, request, jsonify
import win32print

app = Flask(__name__)


def print_text_to_printer(text):
    try:
        printer_name = win32print.GetDefaultPrinter()

        hprinter = win32print.OpenPrinter(printer_name)

        job = win32print.StartDocPrinter(hprinter, 1, ("Flask Print Job", None, "RAW"))
        win32print.StartPagePrinter(hprinter)

        try:
            win32print.WritePrinter(hprinter, text.encode('utf-8'))
        finally:
            # End the print job
            win32print.EndPagePrinter(hprinter)
            win32print.EndDocPrinter(hprinter)
            win32print.ClosePrinter(hprinter)
        return "Printed successfully."
    except Exception as e:
        return f"Failed to print: {str(e)}"


@app.route('/print', methods=['POST'])
def print_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input. Provide 'text' in JSON format."}), 400

    text_to_print = data['text']
    result = print_text_to_printer(text_to_print)
    return jsonify({"message": result})


if __name__ == '__main__':
    app.run(debug=True)
