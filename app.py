import fitz
import io
from PIL import Image
import streamlit as st

# Function to extract and crop Aadhaar images from PDF
def pdf_to_image(pdf_file, password=None):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    if doc.is_encrypted and not doc.authenticate(password):
        return None, "❌ Incorrect password. Please try again."
    
    def get_cropped_image(rect):
        page.set_mediabox(rect)
        return Image.open(io.BytesIO(page.get_pixmap(dpi=300).tobytes()))
    
    page = doc[0]
    front = fitz.Rect(48, 58, 302, 220)
    back = fitz.Rect(310, 58, 564, 220)
    return get_cropped_image(front), get_cropped_image(back)

# Function to save cropped images as PDF
def save_as_pdf(images):
    output = io.BytesIO()
    images[0].save(output, format="PDF", save_all=True, append_images=images[1:], resolution=300)
    output.seek(0)
    return output

# Streamlit App
st.title("Aadhaar Card Cropper")
st.write("Upload your Aadhaar PDF to extract the front and back sides.")

# File upload
uploaded_file = st.file_uploader("📄 Choose a PDF file", type="pdf")
password = st.text_input("🔒 Enter PDF password (if any):", placeholder="Leave blank if not password-protected")

if uploaded_file:
    try:
        # Process PDF
        front, back = pdf_to_image(uploaded_file, password)
        if not front:
            st.error(back)  # Show error message
        else:
            st.image(front, caption="Front Side", use_container_width=True)
            st.image(back, caption="Back Side", use_container_width=True)

            # Save as PDF
            output_pdf = save_as_pdf([front, back])
            st.download_button(
                label="⬇️ Download Cropped Aadhaar PDF",
                data=output_pdf,
                file_name="CroppedAadhaar.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
else:
    st.info("📤 Upload a PDF to get started!")

# Tips
st.markdown("### 💡 Tips for Best Results:")
st.markdown("""
- Ensure the Aadhaar PDF is clear and in the correct format.
- Provide the correct password if the file is encrypted.
- Use the download button to save the cropped Aadhaar PDF.
""")

