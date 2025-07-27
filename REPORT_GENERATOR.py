import csv
from fpdf import FPDF
from datetime import datetime
import statistics

class PDFReportGenerator:
    def __init__(self, data_file, output_file="report.pdf"):
        self.data_file = data_file
        self.output_file = output_file
        self.data = []
        self.analysis_results = {}
        
    def load_data(self):
        """Load data from CSV file"""
        try:
            with open(self.data_file, 'r') as file:
                reader = csv.DictReader(file)
                self.data = [row for row in reader]
            return True
        except FileNotFoundError:
            print(f"Error: File '{self.data_file}' not found.")
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def analyze_data(self):
        """Perform basic analysis on the loaded data"""
        if not self.data:
            return False
            
        # Assuming the CSV has numeric columns 'value1' and 'value2'
        try:
            values1 = [float(row['value1']) for row in self.data if 'value1' in row]
            values2 = [float(row['value2']) for row in self.data if 'value2' in row]
            
            self.analysis_results = {
                'count': len(self.data),
                'value1_avg': statistics.mean(values1) if values1 else 0,
                'value1_min': min(values1) if values1 else 0,
                'value1_max': max(values1) if values1 else 0,
                'value2_avg': statistics.mean(values2) if values2 else 0,
                'value2_min': min(values2) if values2 else 0,
                'value2_max': max(values2) if values2 else 0,
                'generated_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return True
        except KeyError as e:
            print(f"Error: Required column {e} not found in data.")
            return False
        except Exception as e:
            print(f"Error analyzing data: {e}")
            return False
    
    def generate_report(self):
        """Generate PDF report with analysis results"""
        if not self.analysis_results:
            print("No analysis results to report.")
            return False
            
        pdf = FPDF()
        pdf.add_page()
        
        # Set font and title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Data Analysis Report", ln=1, align='C')
        pdf.ln(10)
        
        # Report metadata
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 6, f"Generated on: {self.analysis_results['generated_on']}", ln=1)
        pdf.cell(0, 6, f"Data source: {self.data_file}", ln=1)
        pdf.cell(0, 6, f"Records analyzed: {self.analysis_results['count']}", ln=1)
        pdf.ln(10)
        
        # Summary section
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, "Summary Statistics", ln=1)
        pdf.set_font("Arial", '', 10)
        
        # Create a table for statistics
        col_width = pdf.w / 4
        row_height = 8
        
        # Table header
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(col_width, row_height, "Metric", border=1, fill=True)
        pdf.cell(col_width, row_height, "Value 1", border=1, fill=True)
        pdf.cell(col_width, row_height, "Value 2", border=1, fill=True)
        pdf.ln(row_height)
        
        # Table rows
        pdf.cell(col_width, row_height, "Average", border=1)
        pdf.cell(col_width, row_height, f"{self.analysis_results['value1_avg']:.2f}", border=1)
        pdf.cell(col_width, row_height, f"{self.analysis_results['value2_avg']:.2f}", border=1)
        pdf.ln(row_height)
        
        pdf.cell(col_width, row_height, "Minimum", border=1)
        pdf.cell(col_width, row_height, f"{self.analysis_results['value1_min']:.2f}", border=1)
        pdf.cell(col_width, row_height, f"{self.analysis_results['value2_min']:.2f}", border=1)
        pdf.ln(row_height)
        
        pdf.cell(col_width, row_height, "Maximum", border=1)
        pdf.cell(col_width, row_height, f"{self.analysis_results['value1_max']:.2f}", border=1)
        pdf.cell(col_width, row_height, f"{self.analysis_results['value2_max']:.2f}", border=1)
        pdf.ln(15)
        
        # Add a simple bar chart representation
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, "Data Visualization", ln=1)
        pdf.set_font("Arial", '', 10)
        
        max_val = max(self.analysis_results['value1_max'], self.analysis_results['value2_max']) or 1
        scale = 100 / max_val
        
        # Value 1 bar
        pdf.cell(40, 8, "Value 1 Avg:")
        pdf.set_fill_color(100, 200, 100)
        pdf.cell(self.analysis_results['value1_avg'] * scale, 8, 
                f" {self.analysis_results['value1_avg']:.2f}", fill=True, ln=1)
        
        # Value 2 bar
        pdf.cell(40, 8, "Value 2 Avg:")
        pdf.set_fill_color(100, 100, 200)
        pdf.cell(self.analysis_results['value2_avg'] * scale, 8, 
                f" {self.analysis_results['value2_avg']:.2f}", fill=True, ln=1)
        
        # Footer
        pdf.ln(20)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 6, "End of Report - Generated by Data Analysis Tool", align='C')
        
        # Save the PDF
        pdf.output(self.output_file)
        print(f"Report generated successfully: {self.output_file}")
        return True

if __name__ == "__main__":
    # Example usage
    data_file = "sample_data.csv"
    report_file = "analysis_report.pdf"
    
    print("Starting report generation...")
    generator = PDFReportGenerator(data_file, report_file)
    
    if generator.load_data():
        if generator.analyze_data():
            generator.generate_report()
        else:
            print("Failed to analyze data.")
    else:
        print("Failed to load data.")
