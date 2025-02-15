import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas.plotting import scatter_matrix
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

def visualize_data(df, chart_type, plot_frame):
    numeric_df = df.select_dtypes(include=['number'])
    categorical_df = df.select_dtypes(exclude=['number'])

    if numeric_df.empty and categorical_df.empty:
        messagebox.showerror("Error", "No valid data available for visualization.")
        return

    fig, ax = plt.subplots(figsize=(8, 6))

    try:
        if chart_type == "Heatmap":
            sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)

        elif chart_type == "Pair Plot":
            sns.pairplot(numeric_df)
            plt.show()
            return

        elif chart_type == "Scatter Matrix":
            scatter_matrix(numeric_df, alpha=0.8, figsize=(8, 6), diagonal='kde')
            plt.show()
            return

        elif chart_type == "Histogram":
            numeric_df.hist(bins=20, color="skyblue", edgecolor="black", figsize=(8, 6))
            plt.suptitle("Histogram of Numeric Columns")
            plt.show()
            return

        elif chart_type == "Box Plot":
            numeric_df.plot(kind="box", ax=ax)
            ax.set_title("Box Plot of Numeric Columns")

        elif chart_type == "Violin Plot":
            sns.violinplot(data=numeric_df, ax=ax)
            ax.set_title("Violin Plot of Numeric Columns")

        elif chart_type == "Density Plot":
            numeric_df.plot(kind="density", ax=ax)
            ax.set_title("Density Plot of Numeric Columns")

        elif chart_type == "Pie Chart":
            if not categorical_df.empty:
                categorical_df[categorical_df.columns[0]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
                ax.set_title(f"Pie Chart of {categorical_df.columns[0]}")
            else:
                messagebox.showerror("Error", "No categorical data available for Pie Chart.")

        elif chart_type == "Line Chart":
            numeric_df.plot(kind="line", ax=ax, marker="o")
            ax.set_title("Line Chart of Numeric Columns")
            ax.set_xlabel("Index")
            ax.set_ylabel("Values")

        elif chart_type == "Bar Chart":
            if not categorical_df.empty:
                # Count occurrences of the first categorical column
                categorical_df[categorical_df.columns[0]].value_counts().plot(kind="bar", ax=ax, color="skyblue", edgecolor="black")
                ax.set_title(f"Bar Chart of {categorical_df.columns[0]}")
                ax.set_xlabel(categorical_df.columns[0])
                ax.set_ylabel("Count")
            else:
                messagebox.showerror("Error", "No categorical data available for Bar Chart.")


        elif chart_type == "Count Plot":
            if not categorical_df.empty:
                sns.countplot(x=categorical_df.columns[0], data=df, ax=ax)
                ax.set_title(f"Count Plot of {categorical_df.columns[0]}")
            else:
                messagebox.showerror("Error", "No categorical data available for Count Plot.")

        update_canvas(fig, plot_frame)
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate the plot: {e}")

def update_canvas(fig, plot_frame):
    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
