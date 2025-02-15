import pandas as pd
import pdfplumber
from tkinter import messagebox, filedialog

def load_data(file_path):
    """Loads data from CSV, TXT, or PDF files and returns a Pandas DataFrame."""
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".txt"):
            df = pd.read_csv(file_path, sep=None, engine="python")  # Auto-detect delimiter
        elif file_path.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                extracted_text = [page.extract_text() for page in pdf.pages if page.extract_text()]
                if not extracted_text:
                    messagebox.showerror("Error", "No extractable text found in the PDF.")
                    return None
                
                text = "\n".join(extracted_text)
                data = [line.split() for line in text.split("\n") if line.strip()]
                
                if not data:
                    messagebox.showerror("Error", "Failed to parse structured data from the PDF.")
                    return None
                
                df = pd.DataFrame(data)
        else:
            messagebox.showerror("Error", "Unsupported file format.")
            return None
        
        return df

    except Exception as e:
        messagebox.showerror("Error", f"Error loading dataset: {e}")
        return None


def clean_data(df):
    """Cleans the dataset by handling missing values."""
    try:
        missing_values = df.isnull().sum().sum()
        
        if missing_values > 0:
            user_choice = messagebox.askyesno(
                "Missing Values Detected", 
                f"{missing_values} missing values found. Drop them? (Yes) or Fill with Mean/Mode? (No)"
            )
            
            if user_choice:
                df.dropna(inplace=True)
            else:
                # Fill numeric columns with mean
                for col in df.select_dtypes(include=['number']).columns:
                    df[col].fillna(df[col].mean(), inplace=True)
                
                # Fill categorical columns with mode (most frequent value)
                for col in df.select_dtypes(exclude=['number']).columns:
                    df[col].fillna(df[col].mode()[0], inplace=True)

            messagebox.showinfo("Success", "Missing values handled successfully.")
        
        return df

    except Exception as e:
        messagebox.showerror("Error", f"Error during data cleaning: {e}")
        return df


def save_cleaned_data(df):
    """Saves the cleaned dataset to a CSV file."""
    try:
        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        
        if output_file:
            df.to_csv(output_file, index=False)
            messagebox.showinfo("Success", f"Cleaned data saved to {output_file}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Error saving file: {e}")

