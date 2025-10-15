import streamlit as st
import pandas as pd
from utils.cleaning import clean_keywords
from utils.grouping import group_keywords
from backend.outline import generate_outline_for_group
from backend.post_idea import generate_post_idea_for_group


# App config
st.set_page_config(page_title='SlackBot - Keyword Manager', layout='wide')
st.title('SlackBot - Keyword Manager')
st.write('Upload a CSV file or paste keywords manually.')

# Initialize session state
if 'keywords' not in st.session_state:
    st.session_state['keywords'] = []

if 'groups' not in st.session_state:
    st.session_state['groups'] = {}

# --- Upload CSV ---
uploaded_file = st.file_uploader('Upload a CSV file:', type=['csv'])
csv_keywords = []

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    col_name = st.selectbox('Select the column with keywords:', df.columns)
    csv_keywords = df[col_name].dropna().astype(str).tolist()
    st.success(f'Loaded {len(csv_keywords)} keywords from "{uploaded_file.name}"')

# --- Manual input ---
st.write('### Or paste keywords manually below:')
text_input = st.text_area('Paste keywords (comma or newline separated):', height=150)
text_keywords = []
process_btn = st.button('Submit Keywords')

if process_btn and text_input.strip():
    text_keywords = [kw.strip() for kw in text_input.replace(',', '\n').split('\n') if kw.strip()]
    st.success(f'Processed {len(text_keywords)} pasted keywords.')

# --- Combine & Clean Keywords ---
if process_btn or uploaded_file:
    combined_keywords = list(set(csv_keywords + text_keywords))
    cleaned_keywords = clean_keywords(combined_keywords)
    st.session_state['keywords'] = cleaned_keywords
    st.session_state['groups'] = group_keywords(cleaned_keywords)

# --- Display Keywords ---
if st.session_state['keywords']:
    st.write('### Preview of Keywords')
    st.dataframe(pd.DataFrame(st.session_state['keywords'], columns=['Keywords']))
else:
    st.info('No keywords added yet. Upload a CSV or paste keywords above.')

# --- Grouping Display ---
if st.session_state['groups']:
    if st.button('Show Keyword Groups'):
        groups = st.session_state['groups']
        st.success(f'Grouped into {len(groups)} semantic groups.')

        for i, (group_id, kw_list) in enumerate(groups.items(), 1):
            with st.expander(f'Group {i} ({len(kw_list)} keywords)'):
                st.write(', '.join(kw_list))

st.sidebar.markdown("---")
if st.sidebar.button('🔄 Reset Session'):
    st.session_state['keywords'] = []
    st.session_state['groups'] = {}
    st.success('Session reset. Upload or enter new keywords.')



# Outline + Post Idea Generation
if st.session_state['groups']:
    st.header('Generate Outline & Post Idea for Each Group')

    for i, (group_id, kw_list) in enumerate(st.session_state['groups'].items(), 1):
        st.subheader(f'Group {i}')
        st.write(', '.join(kw_list))

        if st.button(f'Create Outline & Post Idea for Group {i}', key=f"group_{i}"):
            with st.spinner(f'Generating outline and post idea for Group {i}...'):
                # Generate Outline
                outline = generate_outline_for_group(kw_list)

                # Generate Post Idea using the outline as context
                post_idea = generate_post_idea_for_group(kw_list, outline)

            # Display results
            st.text_area(f'Generated Outline for Group {i}', outline, height=300)
            st.text_area(f'Generated Post Idea for Group {i}', post_idea, height=100)
