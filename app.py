import streamlit as st
import requests
import py3Dmol
import io
# Set page config with favicon and tab title
st.set_page_config(
    page_title="dbacp - 3D visualisation",
    page_icon=" "  # You can use an emoji or a path to a .ico/.png file
)
# Retrieve peptide sequence from query params
query_params = st.query_params
peptide_seq = query_params.get("sequence", "")
accession = query_params.get("accession", "")


# Show input
st.subheader("Visualise your 3D structure here")
if peptide_seq:
    st.write("dbACP accession id")
    st.code(accession)
    st.write("Input sequence")
    st.code(peptide_seq)
else:
    st.warning("No peptide sequence provided in query parameter.")
    st.stop()

# Function to show PDB structure
def show_pdb(pdb_string):
    view = py3Dmol.view(width=700, height=400)
    view.addModel(pdb_string, 'pdb')
    view.setStyle({'cartoon': {'color': 'spectrum'}})
    view.setBackgroundColor('white')
    view.zoomTo()
    st.components.v1.html(view._make_html(), height=400)

# Fetch structure from ESMAtlas API
try:
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(
        'https://api.esmatlas.com/foldSequence/v1/pdb/', 
        headers=headers,
        data=peptide_seq,
        verify=True  # ⚠️ For demo only, disable in production
    )

    if response.status_code == 200:
        pdb_string = response.content.decode('utf-8')
        st.success("Get your 3D structure predicted by ESM-Fold")

        # Show 3D model
        show_pdb(pdb_string)

        # Download button
        pdb_file = io.BytesIO(pdb_string.encode("UTF-8"))
        st.download_button(
            label="📥 Download PDB File",
            data=pdb_file,
            file_name="predicted_structure.pdb",
            mime="chemical/x-pdb"
        )
    else:
        st.error(f"API error: {response.status_code}")

except Exception as e:
    st.error(f"Error in fetching or rendering structure: {e}")
