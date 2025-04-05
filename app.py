# app.py

import os
# Added flash for better messages
from flask import Flask, render_template, request, flash
from logic import extractive_summarization  # Import the function

app = Flask(__name__)

# Secret key is needed for flashing messages
app.secret_key = os.urandom(24)  # Generate a random secret key


@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles both displaying the form and processing the summarization request."""
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        num_sentences_str = request.form.get('num_sentences', '')

        original_text = text  # Keep original text for display
        summary = None
        error = None

        # --- Input Validation ---
        if not text:
            error = "Text input cannot be empty."
            # flash("Error: Text input cannot be empty.", "error") # Using flash message
        elif not num_sentences_str:
            error = "Number of sentences cannot be empty."
            # flash("Error: Number of sentences cannot be empty.", "error")
        else:
            try:
                num_sentences = int(num_sentences_str)
                if num_sentences <= 0:
                    error = "Number of sentences must be a positive integer."
                    # flash("Error: Number of sentences must be a positive integer.", "error")
                else:
                    # --- Call Summarization Logic ---

                    summary = extractive_summarization(text, num_sentences)
                    print("Summarization complete.")  # Server log

                    # Check if the summarization function returned an error message
                    if summary.startswith("Error:"):
                        error = summary
                        summary = None  # Don't display summary if there was an error string returned

            except ValueError:
                error = "Invalid input: Number of sentences must be an integer."
                # flash("Error: Invalid input: Number of sentences must be an integer.", "error")
            except Exception as e:
                pass
                # Catch unexpected errors during processing
                # app.logger.error(f"Unexpected error during summarization request: {
                #                  e}", exc_info=True)
                # error = "An unexpected server error occurred. Please try again later."
                # flash("An unexpected server error occurred. Please try again later.", "error")

        # Render the template, passing relevant data
        # We pass original_text even if there's an error, so the textarea is repopulated
        return render_template('index.html',
                               original_text=original_text,
                               summary=summary,
                               error=error)

    # --- Handle GET Request ---
    # Just display the empty form on the initial visit
    return render_template('index.html', original_text=None, summary=None, error=None)
