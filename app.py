import fitz
import io
from PIL import Image
import streamlit as st

def pdf_to_image(pdf_file, password=None):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    if doc.is_encrypted and not doc.authenticate(password):
        return None, "Invalid password."
    def get_cropped_image(rect):
        page.set_mediabox(rect)
        return Image.open(io.BytesIO(page.get_pixmap(dpi=300).tobytes()))
    page = doc[0]
    front = fitz.Rect(31, 99, 293, 264)
    back = fitz.Rect(300, 99, 564, 264)
    return get_cropped_image(front), get_cropped_image(back)

def save_as_pdf(images):
    output = io.BytesIO()
    images[0].save(output, format="PDF", save_all=True, append_images=images[1:], resolution=300)
    output.seek(0)
    return output

# Streamlit App
st.title("Aadhaar Card Cropper")
st.write("Upload your Aadhaar PDF file to extract and process its content.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
password = st.text_input("Enter PDF password (if any):", type="password")

if uploaded_file:
    try:
        front, back = pdf_to_image(uploaded_file, password)
        if not front:
            st.error(back)  # Show error message for invalid password
        else:
            st.image(front, caption="Front Side", use_container_width=True)
            st.image(back, caption="Back Side", use_container_width=True)
            output_pdf = save_as_pdf([front, back])
            st.download_button(
                label="Download Cropped Aadhaar PDF",
                data=output_pdf,
                file_name="CroppedAadhaar.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"An error occurred: {e}")
