# Daily Journal Memory Manager

A Pygame and Tkinter-based journal manager for creating, storing, and viewing daily journal entries with selfies. This memory manager also includes sentiment analysis to gauge the tone of each entry, displayed in a clean and interactive UI with my custom Pygame-based **PgUI** module.

## Features

- **Journal Entry Management**: Add daily text entries alongside an image, auto-stored by date.
- **Sentiment Analysis**: Uses NLP to analyze the tone of entries (positive/negative) and displays color-coded feedback.
- **PgUI Custom Interface**: Built on a custom Pygame-based UI framework for dynamic and interactive entry management.
- **Search and Pagination**: Search through entries and navigate between entries with forward/back buttons.

## Installation

1. **Clone the repository**

2. **Install dependencies**: Ensure you have Python installed, then install the following modules:
    ```bash
    pip install pygame transformers torch
    ```

3. **Download or Set Up Local Model for Sentiment Analysis**: Download a compatible transformers model or set up a local model at ./local_model/ for sentiment analysis.

4. **Run the Application**:
    ```bash
    python main.py
    ```

## Usage
- **Adding Entries**: Click on "+" to create a new journal entry with a date and optional text. A file dialog will open to select an image.
- **Navigating Entries**: Use forward/back buttons or search to locate specific entries.
- **Sentiment Analysis**: Sentiment scores are auto-updated upon journal review, offering a color-coded indication of tone.

## Folder Structure
- **files/**: Stores text and image files for each date entry.
- **meta.txt**: Tracks sentiment analysis results with positive and negative scores.

# Requirements
- **Python 3.6+**
- **Pygame**
- **Transformers and PyTorch** for sentiment analysis
- **Tkinter** for file dialog support