import json
import os
import argparse

def traverse_json(data, indent_level=0):
    report = []

    # Indentation for nesting.
    indent = "  " * indent_level
    
    # Check if it's a dictionary.
    if isinstance(data, dict):

        # Recursively traverse the dictionary.
        for key, value in data.items():
            
            # Add key:value pair.
            report.append(f"{indent}{key}:")

            # Recursively traverse the value.
            report.extend(traverse_json(value, indent_level + 1))
    
    # Check if it's a list.
    elif isinstance(data, list):
                
        # Loop through the list.
        for item in data:

            # If it's a dictionary, recursively traverse it.
            if isinstance(item, dict):
                report.extend(traverse_json(item, indent_level))
                
            else:
                
                # If it's not a dictionary, it's a key:value pair.
                report.append(f"{indent}- {item}")
    else:

        # Add key:value pair.
        report.append(f"{indent}{data}")
    
    return report

def generate_html_report_page(output_dir, logo_path, analyzer_report):
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Analyzer Reports</title>
        <style>
            body {{
                background-color: #000;
                color: #fff;
                font-family: Arial, sans-serif;
                padding: 20px;
                margin: 0;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                text-align: center;
            }}
            h1 {{
                color: #f9c74f;
            }}
            a {{
                color: #90be6d;
                text-decoration: none;
                font-size: 18px;
                display: block;
                margin: 10px 0;
                padding: 10px;
                background-color: #1d3557;
                border-radius: 8px;
                transition: background-color 0.3s ease;
            }}
            a:hover {{
                background-color: #457b9d;
            }}
            img {{
                max-width: 100px;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="{logo_path}" alt="Logo">
            <h1>Analyzer Reports</h1>
    """.format(logo_path=logo_path)

    # Add links to each report in the analyzer_reports directory.
    for filename in os.listdir(output_dir):
        if filename.endswith("_report.txt"):
            html_content += f'<a href="{output_dir}/{filename}" target="_blank">{filename}</a>\n'

    html_content += """
        </div>
    </body>
    </html>
    """


    # Write the HTML content to a file.
    with open(analyzer_report, "w") as html_file:
        html_file.write(html_content)
    
    print("HTML report page has been generated: analyzer_reports_page.html")

def generate_dynamic_report(data, title):

    report = []
    
    # Add a title for the report
    report.append(f"Dynamic Report for {title}\n")
    
    # Recursively traverse the JSON and generate the report
    report.extend(traverse_json(data))
    
    # Join the report into a single text block and return
    return "\n".join(report)

if __name__ == "__main__":

    # Get the path to the JSON file and the output directory.
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Path to the intelOwl JSON file", required=True)
    parser.add_argument("-d", "--dir", help="Output directory", required=True)
    parser.add_argument("-r", "--report", help="HTML report", required=True)
    args = parser.parse_args()
    
    # Set the path to the JSON file
    intelOwlReport = args.file
    outputDir = args.dir
    htmlReport = args.report

    # Check if the file and directory values are passed to the cli.
    if not intelOwlReport or not outputDir or not htmlReport:
        print("Please provide the path to the JSON file, the output directory, and the HTML report.")
        print("Example: python intelOwlReport.py -f intelOwl.json -d analyzer_reports -r analyzer_reports.html")
        exit()

    # Check if the JSON file exists and prompt if they want to overwrite it.
    if os.path.exists(htmlReport):
        overwrite = input(f"The file '{htmlReport}' already exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != "y":
            print("Exiting...")
            exit()
    
    # Load the intelOwl report.
    with open(intelOwlReport, 'r') as file:
        full_json_data = json.load(file)
    
    # Get the analyzer reports.
    analyzer_reports = full_json_data.get("analyzer_reports", [])

    # Check if the analyzer directory exists. If so, keep running.
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # Generate individual files for each analyzer report based on the "name" field.
    for report in analyzer_reports:

        # This ensures the filename is 'safe' for the OS so spaces are removed and no slashes are allowed.
        report_name = report_name = report["name"].replace(" ", "_").replace("/", "_")
        report_content = generate_dynamic_report(report, report_name)
        
        # Save the report for each analyzer in the analyzer_report list.
        file_path = os.path.join(outputDir, f"{report_name}_report.txt")
        with open(file_path, "w") as report_file:
            report_file.write(report_content)
        
        logo_path = outputDir +"/intelowlwhite.png"
        print(f"Report for {report_name} has been written to {file_path}")
        
    generate_html_report_page(outputDir, logo_path, htmlReport)

