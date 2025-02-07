import streamlit as st
from transformers import pipeline
import PyPDF2
import re

# Load NLP models
clause_extraction_model = pipeline("ner", model="nlpaueb/legal-bert-base-uncased")  # LegalBERT for clause extraction

# Define essential clauses for comparison
essential_clauses = [
    "Confidentiality",
    "Termination",
    "Governing Law",
    "Indemnity",
    "Force Majeure",
]

# Define risky terms for red flag detection
risky_terms = {
    "liability": ["unlimited liability", "not limited"],
    "termination": ["unilateral termination", "short notice period"],
    "confidentiality": ["no confidentiality", "missing confidentiality"],
}

# Define formatting error patterns
formatting_patterns = {
    "numbering": r"^\d+\.\d+",  # Example: "1.1", "2.3"
    "placeholders": r"\[.*?\]",  # Example: "[Insert Name Here]"
}

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to check for missing clauses
def check_missing_clauses(text, essential_clauses):
    missing = []
    for clause in essential_clauses:
        if clause.lower() not in text.lower():
            missing.append(clause)
    return missing

# Function to detect formatting errors
def detect_formatting_errors(text, patterns):
    errors = []
    for error_type, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            errors.append((error_type, matches))
    return errors

# Function to detect red flags
def detect_red_flags(text, risky_terms, client_context):
    red_flags = []
    for clause, terms in risky_terms.items():
        for term in terms:
            if term in text.lower():
                red_flags.append(f"Red flag in {clause} clause: {term}")
    return red_flags

# Function to summarize the contract
def summarize_contract(text):
    # Placeholder for summarization logic (can use GPT or other models)
    summary = "This is a placeholder summary of the contract."
    return summary

# Function to identify blanks and missing information
def identify_blanks(text):
    blanks = re.findall(r"\[.*?\]", text)
    return blanks

# Streamlit app
st.title("AI-Powered Contract Review")

# Upload contract
uploaded_file = st.file_uploader("Upload a contract (PDF)", type=["pdf"])

if uploaded_file:
    # Extract text from the uploaded contract
    contract_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Contract Text", contract_text, height=300)

    # Feature 1: Check for missing clauses
    st.subheader("Missing Clauses")
    missing_clauses = check_missing_clauses(contract_text, essential_clauses)
    if missing_clauses:
        st.write("The following essential clauses are missing:")
        for clause in missing_clauses:
            st.write(f"- {clause}")
    else:
        st.write("No missing clauses detected.")

    # Feature 2: Detect formatting errors
    st.subheader("Formatting Errors")
    formatting_errors = detect_formatting_errors(contract_text, formatting_patterns)
    if formatting_errors:
        st.write("The following formatting errors were detected:")
        for error_type, matches in formatting_errors:
            st.write(f"- {error_type.capitalize()}: {', '.join(matches)}")
    else:
        st.write("No formatting errors detected.")

    # Feature 3: Identify red flags
    st.subheader("Red Flags")
    client_context = st.selectbox("Select Client Context", ["Buyer", "Seller", "Employer", "Employee"])
    red_flags = detect_red_flags(contract_text, risky_terms, client_context)
    if red_flags:
        st.write("The following red flags were detected:")
        for flag in red_flags:
            st.write(f"- {flag}")
    else:
        st.write("No red flags detected.")

    # Feature 4: Summarize the contract
    st.subheader("Contract Summary")
    summary = summarize_contract(contract_text)
    st.write(summary)

    # Feature 5: Identify blanks and missing information
    st.subheader("Blanks and Missing Information")
    blanks = identify_blanks(contract_text)
    if blanks:
        st.write("The following blanks were detected:")
        for blank in blanks:
            st.write(f"- {blank}")
    else:
        st.write("No blanks detected.")

    # Feature 6: Analyze based on user instructions
    st.subheader("Analyze Based on Instructions")
    user_instruction = st.text_input("Enter your instruction (e.g., 'Check if the termination clause allows unilateral termination')")
    if user_instruction:
        # Placeholder for instruction-based analysis logic
        st.write(f"Analysis for instruction: '{user_instruction}'")
        st.write("This feature is under development.")