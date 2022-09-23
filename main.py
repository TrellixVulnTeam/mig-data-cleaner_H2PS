import streamlit as st
import pandas as pd
# import numpy as np
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(layout="wide", page_title="MIG Data Cleaning App",
                   page_icon="https://www.agilitypr.com/wp-content/uploads/2018/02/favicon-192.png")
hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


def top_x_by_mentions(df, column_name):
    """Returns top 10 items by mention count"""

    top10 = df[[column_name, 'Mentions']].groupby(
        by=[column_name]).sum().sort_values(
        ['Mentions'], ascending=False)
    top10 = top10.rename(columns={"Mentions": "Hits"})

    return top10.head(10)


def basic_metrics(set_name, df):
    if len(df) > 0:
        with st.expander(set_name):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Basic Metrics")
                st.metric(label="Mentions", value="{:,}".format(len(df)))
                st.metric(label="Impressions",
                          value="{:,}".format(df['Impressions'].sum()))
            with col2:
                st.subheader("Media Type")
                st.write(df['Type'].cat.remove_unused_categories().value_counts())
            st.subheader("Data")
            st.markdown('(First 50 rows)')
            st.dataframe(df.head(50).style.format(format_dict, na_rep=' '))


format_dict = {'AVE': '${0:,.0f}', 'Audience Reach': '{:,d}', 'Impressions': '{:,d}'}

# Initialize Session State Variables
string_vars = {'page': '1: Getting Started', 'top_auths_by': 'Mentions', 'export_name': ''}
for key, value in string_vars.items():
  if key not in st.session_state:
      st.session_state[key] = value

df_vars = ['df_traditional', 'df_social', 'df_dupes', 'original_trad_auths', 'auth_outlet_table', 'original_auths', 'df_raw', 'df_untouched', 'author_outlets', 'broadcast_set', 'blank_set', 'df_yahoos']
for _ in df_vars:
    if _ not in st.session_state:
        st.session_state[_] = pd.DataFrame()

step_vars = ['upload_step', 'standard_step', 'translated_headline', 'translated_summary', 'translated_snippet', 'filled'] #outliers',
for _ in step_vars:
    if _ not in st.session_state:
        st.session_state[_] = False

counter_vars = ['counter', 'auth_outlet_skipped']
for _ in counter_vars:
    if _ not in st.session_state:
        st.session_state[_] = 0



# Sidebar and page selector
st.sidebar.image('https://agilitypr.news/images/Agility-centered.svg', width=200)
st.sidebar.title('MIG: Data Cleaning App')
pagelist = [
    "1: Getting Started",
    "2: Standard Cleaning",
    "3: Authors - Missing",
    "4: Authors - Outlets",
    "5: Translation",
    "6: Download"]

page = st.sidebar.radio("Data Cleaning Steps:", pagelist, index=0)
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.write("**Quick Links**")
st.sidebar.markdown("""
    [Bug Tracker](https://mediamiser.sharepoint.com/:x:/s/MIG/ESIF0YBKmq9EuXffFemDJKsBOuTn05Wii9ABFcj_q39A0A?e=zZ9oB2) \n
    [Quickstart Guide](https://github.com/JeremyParkin/mig-data-cleaner/blob/main/README.md) \n
    [GitHub Project](https://github.com/JeremyParkin/mig-data-cleaner) 
    """)
st.sidebar.caption("v.1.5.4.2")

if page == "1: Getting Started":
    st.title('Getting Started')
    # import altair as alt
    # import io

    # TODO: Fully blank author column creates an error with top X function


    if st.session_state.upload_step == True:
        st.success('File uploaded.')
        if st.button('Start Over?'):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()


        st.session_state.df_untouched["Mentions"] = 1

        if "Impressions" in st.session_state.df_untouched:
            st.session_state.df_untouched = st.session_state.df_raw.rename(columns={
                'Impressions': 'Audience Reach'})


        st.session_state.df_untouched['Audience Reach'] = st.session_state.df_untouched['Audience Reach'].astype('Int64')
        st.session_state.df_untouched['AVE'] = st.session_state.df_untouched['AVE'].fillna(0)


        st.header('Exploratory Data Analysis')
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Basic Metrics")
            st.metric(label="Mentions", value="{:,}".format(len(st.session_state.df_untouched.dropna(thresh=3))))
            st.metric(label="Impressions", value="{:,}".format(st.session_state.df_untouched['Audience Reach'].sum()))
        with col2:
            st.subheader("Media Type")
            st.write(st.session_state.df_untouched['Media Type'].value_counts())

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Top Authors")
            original_top_authors = (top_x_by_mentions(st.session_state.df_untouched, "Author"))
            st.write(original_top_authors)
            st.session_state.original_auths = original_top_authors
        with col4:
            st.subheader("Top Outlets")
            original_top_outlets = (top_x_by_mentions(st.session_state.df_untouched, "Outlet"))
            st.write(original_top_outlets)

        st.markdown('##')
        # st.subheader('Mention Trend')
        #
        # trend = alt.Chart(st.session_state.df_untouched).mark_line().encode(
        #     x='Published Date:T',
        #     y='sum(Mentions):Q'
        # )
        # st.altair_chart(trend, use_container_width=True)
        #
        # st.markdown('##')
        # st.subheader('Impressions Trend')
        # trend2 = alt.Chart(st.session_state.df_untouched).mark_line().encode(
        #     x='Published Date:T',
        #     y='sum(Audience Reach):Q'
        # )
        # st.altair_chart(trend2, use_container_width=True)
        #
        # st.subheader("Raw Data")
        # st.markdown('(First 100 rows)')
        # st.dataframe(st.session_state.df_untouched.head(100).style.format(format_dict, na_rep=' '))
        # st.markdown('##')


    if st.session_state.upload_step == False:
        with st.form('my_form'):
            client = st.text_input('Client organization name*', placeholder='eg. Air Canada', key='client',
                                   help='Required to build export file name.')
            period = st.text_input('Reporting period or focus*', placeholder='eg. March 2022', key='period',
                                   help='Required to build export file name.')
            uploaded_file = st.file_uploader(label='Upload your CSV*', type='csv',
                                             accept_multiple_files=False,
                                             help='Only use CSV files exported from the Agility Platform.')

            submitted = st.form_submit_button("Submit")
            if submitted and (client == "" or period == "" or uploaded_file == None):
                st.error('Missing required form inputs above.')

            elif submitted:
                with st.spinner("Converting file format."):
                    st.session_state.df_untouched = pd.read_csv(uploaded_file)
                    if "Impressions" in st.session_state.df_untouched:
                        st.session_state.df_untouched = st.session_state.df_untouched.rename(columns={
                            'Impressions': 'Audience Reach'})

                    st.session_state.df_untouched = st.session_state.df_untouched.dropna(thresh=3)
                    st.session_state.df_untouched["Mentions"] = 1

                    st.session_state.df_untouched['Audience Reach'] = st.session_state.df_untouched['Audience Reach'].astype('Int64')
                    st.session_state.df_untouched['AVE'] = st.session_state.df_untouched['AVE'].fillna(0)
                    st.session_state.export_name = f"{client} - {period} - clean_data.xlsx"
                    st.session_state.df_raw = st.session_state.df_untouched
                    st.session_state.df_raw.drop(["Timezone",
                                                  "Word Count",
                                                  "Duration",
                                                  "Image URLs",
                                                  "Folders",
                                                  "Notes",
                                                  "County",
                                                  "isAudienceFromPartnerUniqueVisitor"],
                                                 axis=1, inplace=True, errors='ignore')

                    st.session_state.df_raw = st.session_state.df_raw.astype(
                        {"Media Type": 'category',
                         "Sentiment": 'category',
                         "Continent": 'category',
                         "Country": 'category',
                         "Province/State": 'category',
                         "City": 'category',
                         "Language": 'category'
                         })

                    if "Published Date" in st.session_state.df_raw:
                        st.session_state.df_raw['Date'] = pd.to_datetime(st.session_state.df_raw['Published Date'] + ' ' + st.session_state.df_raw['Published Time'])
                        st.session_state.df_raw.drop(["Published Date", "Published Time"], axis=1, inplace=True, errors='ignore')

                        first_column = st.session_state.df_raw.pop('Date')
                        st.session_state.df_raw.insert(0, 'Date', first_column)



                    st.session_state.df_raw = st.session_state.df_raw.rename(columns={
                        'Media Type': 'Type',
                        'Coverage Snippet': 'Snippet',
                        'Province/State': 'Prov/State',
                        'Audience Reach': 'Impressions'})

                    st.session_state.upload_step = True
                    st.experimental_rerun()


elif page == "2: Standard Cleaning":
    st.title('Standard Cleaning')
    from titlecase import titlecase


    if st.session_state.upload_step == False:
        st.error('Please upload a CSV before trying this step.')
    elif st.session_state.standard_step:
        st.success("Standard cleaning done!")

        if len(st.session_state.df_traditional) > 0:
            with st.expander("Traditional"):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Basic Metrics")
                    st.metric(label="Mentions", value="{:,}".format(len(st.session_state.df_traditional)))
                    st.metric(label="Impressions", value="{:,}".format(st.session_state.df_traditional['Impressions'].sum()))
                with col2:
                    st.subheader("Media Type")
                    st.write(st.session_state.df_traditional['Type'].cat.remove_unused_categories().value_counts())
                st.subheader("Data")
                st.markdown('(First 50 rows)')
                st.dataframe(st.session_state.df_traditional.head(50).style.format(format_dict, na_rep=' '))


        if len(st.session_state.df_social) > 0:
            with st.expander("Social"):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Basic Metrics")
                    st.metric(label="Mentions", value="{:,}".format(len(st.session_state.df_social)))
                    st.metric(label="Impressions", value="{:,}".format(st.session_state.df_social['Impressions'].sum()))
                with col2:
                    st.subheader("Media Type")
                    st.write(st.session_state.df_social['Type'].cat.remove_unused_categories().value_counts())
                st.subheader("Data")
                st.markdown('(First 50 rows)')
                st.dataframe(st.session_state.df_social.head(50).style.format(format_dict, na_rep=' '))
        if len(st.session_state.df_dupes) > 0:
            with st.expander("Deleted Duplicates"):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Basic Metrics")
                    st.metric(label="Mentions", value="{:,}".format(len(st.session_state.df_dupes)))
                    st.metric(label="Impressions", value="{:,}".format(st.session_state.df_dupes['Impressions'].sum()))
                with col2:
                    st.subheader("Media Type")
                    st.write(st.session_state.df_dupes['Type'].cat.remove_unused_categories().value_counts())
                st.dataframe(st.session_state.df_dupes.style.format(format_dict, na_rep=' '))
    else:
        # def yahoo_cleanup(df, url_string):
        #     df.loc[df['URL'].str.contains(url_string, na=False), "Outlet"] = "Yahoo! News"
        #     df.loc[df['URL'].str.contains(url_string, na=False), "Impressions"] = 80828000
        #     df.loc[df['URL'].str.contains(url_string, na=False), "Country"] = (np.nan)
        #     df.loc[df['URL'].str.contains(url_string, na=False), "Continent"] = (np.nan)
        #     df.loc[df['URL'].str.contains(url_string, na=False), "City"] = (np.nan)
        #     df.loc[df['URL'].str.contains(url_string, na=False), "Prov/State"] = (np.nan)
        #     df.loc[df['URL'].str.contains(url_string, na=False), "sub"] = df['URL'].str.rsplit('/', 1).str[-1]
        #     df.loc[df['URL'].str.contains(url_string, na=False), "URL"] = 'https://news.yahoo.com/' + df["sub"]
        #     df.drop(["sub"], axis=1, inplace=True, errors='ignore')
        #
        #
        # def moreover_yahoo_cleanup(df, outlet_name):
        #     df.loc[(df['URL'].str.contains('ct.moreover')) & (df['Outlet'] == outlet_name), "Outlet"] = "Yahoo! News"
        #     df.loc[(df['URL'].str.contains('ct.moreover')) & (df['Outlet'] == outlet_name), "Impressions"] = 80828000
        #     df.loc[(df['URL'].str.contains('ct.moreover')) & (df['Outlet'] == outlet_name), "Country"] = (np.nan)
        #     df.loc[(df['URL'].str.contains('ct.moreover')) & (df['Outlet'] == outlet_name), "Continent"] = (np.nan)
        #     df.loc[(df['URL'].str.contains('ct.moreover')) & (df['Outlet'] == outlet_name), "City"] = (np.nan)
        #     df.loc[(df['URL'].str.contains('ct.moreover')) & (df['Outlet'] == outlet_name), "Prov/State"] = (np.nan)


        def fixable_impressions_list(df):
            """WIP - Returns item from most fixable imp list"""
            imp_table = pd.pivot_table(df, index="Outlet", values=["Mentions", "Impressions"], aggfunc="count")
            imp_table["Missing"] = imp_table["Mentions"] - imp_table["Impressions"]
            imp_table = imp_table[imp_table["Impressions"] > 0]
            imp_table = imp_table[imp_table['Missing'] > 0]
            imp_table = imp_table.sort_values("Missing", ascending=False)
            imp_table = imp_table.reset_index()
            return imp_table


        def fix_imp(df, outlet, new_impressions_value):
            """Updates all impressions for a given outlet"""
            df.loc[df["Outlet"] == outlet, "Impressions"] = new_impressions_value


        def outlet_imp(df, outlet):
            """Returns the various authors for a given headline"""
            outlet_imps = (df[df.Outlet == outlet].Impressions.value_counts().reset_index())
            return outlet_imps



        with st.form("my_form_basic_cleaning"):
            st.subheader("Cleaning options")
            merge_online = st.checkbox("Merge 'blogs' and 'press releases' into 'Online'", value=True)
            fill_known_imp = st.checkbox("Fill missing impressions values where known match exists in data", value=True)
            drop_dupes = st.checkbox("Drop duplicates", value=True)
            # skip_yahoos = st.checkbox("Skip FULL Yahoo normalization", value=True)

            submitted = st.form_submit_button("Go!")
            if submitted:
                with st.spinner("Running standard cleaning."):

                    st.session_state.df_raw["Type"].replace({"ONLINE_NEWS": "ONLINE NEWS", "PRESS_RELEASE": "PRESS RELEASE"}, inplace=True)

                    type_categories = (['ONLINE NEWS', 'PRINT', 'RADIO', 'TV', 'BLOGS', 'PRESS RELEASE', 'FACEBOOK', 'TWITTER', 'INSTAGRAM', 'REDDIT', 'YOUTUBE'])

                    st.session_state.df_raw["Type"] = pd.Categorical(
                        st.session_state.df_raw["Type"], categories=type_categories)
                    st.session_state.df_raw.loc[st.session_state.df_raw['URL'].str.contains("www.facebook.com", na=False), 'Type'] = "FACEBOOK"
                    st.session_state.df_raw.loc[st.session_state.df_raw['URL'].str.contains("/twitter.com", na=False), 'Type'] = "TWITTER"
                    st.session_state.df_raw.loc[st.session_state.df_raw['URL'].str.contains("www.instagram.com", na=False), 'Type'] = "INSTAGRAM"
                    st.session_state.df_raw.loc[st.session_state.df_raw['URL'].str.contains("reddit.com", na=False), 'Type'] = "REDDIT"
                    st.session_state.df_raw.loc[st.session_state.df_raw['URL'].str.contains("youtube.com", na=False), 'Type'] = "YOUTUBE"

                    if merge_online:
                        st.session_state.df_raw.Type.replace({
                            "ONLINE NEWS": "ONLINE",
                            "PRESS RELEASE": "ONLINE",
                            "BLOGS": "ONLINE"}, inplace=True)


                    if "Original URL" in st.session_state.df_raw:
                        st.session_state.df_raw.loc[st.session_state.df_raw["Original URL"].notnull(), "URL"] = st.session_state.df_raw["Original URL"]


                    st.session_state.df_raw.drop(["Original URL"], axis=1, inplace=True, errors='ignore')


                    # Move columns
                    temp = st.session_state.df_raw.pop('Impressions')
                    st.session_state.df_raw.insert(4, 'Impressions', temp)
                    temp = st.session_state.df_raw.pop('Mentions')
                    st.session_state.df_raw.insert(4, 'Mentions', temp)


                    # Strip extra white space
                    st.session_state.df_raw['Headline'] = st.session_state.df_raw['Headline'].astype(str)
                    strip_columns = ['Headline', 'Outlet', 'Author']
                    for column in strip_columns:
                        st.session_state.df_raw[column].str.strip()
                        st.session_state.df_raw[column] = st.session_state.df_raw[column].str.replace('   ', ' ')
                        st.session_state.df_raw[column] = st.session_state.df_raw[column].str.replace('  ', ' ')


                    # Remove (Online)
                    st.session_state.df_raw['Outlet'] = st.session_state.df_raw['Outlet'].str.replace(' \(Online\)', '')

                    # Replace wonky apostrophes
                    st.session_state.df_raw['Headline'] = st.session_state.df_raw['Headline'].str.replace('\‘', '\'')
                    st.session_state.df_raw['Headline'] = st.session_state.df_raw['Headline'].str.replace('\’', '\'')


                    # SOCIALS To sep df
                    soc_array = ['FACEBOOK', 'TWITTER', 'INSTAGRAM', 'REDDIT', 'YOUTUBE']
                    st.session_state.df_social = st.session_state.df_raw.loc[st.session_state.df_raw['Type'].isin(soc_array)]
                    st.session_state.df_raw = st.session_state.df_raw[~st.session_state.df_raw['Type'].isin(soc_array)]

                    # original_top_authors = (top_x_by_mentions(st.session_state.df_untouched, "Author"))
                    original_trad_auths = (top_x_by_mentions(st.session_state.df_raw, "Author"))
                    st.session_state.original_trad_auths = original_trad_auths


                    # Fill known impressions
                    if fill_known_imp:
                        imp_fix_table = fixable_impressions_list(st.session_state.df_raw)
                        for outlet in imp_fix_table.Outlet:
                            if len(outlet_imp(st.session_state.df_raw, outlet)) == 1:
                                fix_imp(st.session_state.df_raw, outlet, int(outlet_imp(st.session_state.df_raw, outlet)['index']))

                    # SPLIT OUT BROADCAST
                    broadcast_array = ['RADIO', 'TV']
                    st.session_state.broadcast_set = st.session_state.df_raw.loc[st.session_state.df_raw['Type'].isin(broadcast_array)]
                    st.session_state.df_raw = st.session_state.df_raw[~st.session_state.df_raw['Type'].isin(broadcast_array)]


                    # AP Cap
                    st.session_state.df_raw[['Headline']] = st.session_state.df_raw[['Headline']].fillna('')
                    st.session_state.df_raw['Headline'] = st.session_state.df_raw['Headline'].map(lambda Headline: titlecase(Headline))


                    # if skip_yahoos == False:
                    #     # Yahoo standardizer
                    #     yahoo_cleanup(st.session_state.df_raw, 'sports.yahoo.com')
                    #     yahoo_cleanup(st.session_state.df_raw, 'www.yahoo.com')
                    #     yahoo_cleanup(st.session_state.df_raw, 'news.yahoo.com')
                    #     yahoo_cleanup(st.session_state.df_raw, 'style.yahoo.com')
                    #     yahoo_cleanup(st.session_state.df_raw, 'finance.yahoo.com')
                    #     yahoo_cleanup(st.session_state.df_raw, 'es-us.finanzas.yahoo.com')
                    #     yahoo_cleanup(st.session_state.df_raw, 'money.yahoo.com')
                    #
                    #     moreover_yahoo_cleanup(st.session_state.df_raw, 'Yahoo! US')
                    #     moreover_yahoo_cleanup(st.session_state.df_raw, 'Yahoo! en Español')
                    #     moreover_yahoo_cleanup(st.session_state.df_raw, 'Yahoo! Money')
                        # moreover_yahoo_cleanup(st.session_state.df_raw, 'Yahoo! Style')
                        # moreover_yahoo_cleanup(st.session_state.df_raw, 'Yahoo! News')


#                     if drop_dupes == True:
                        # extract subset of all yahoos
#                         st.session_state.df_yahoos = st.session_state.df_raw.loc[
#                             st.session_state.df_raw['Outlet'].str.contains('Yahoo')]
#                         st.session_state.df_raw = st.session_state.df_raw[
#                             ~st.session_state.df_raw['Outlet'].str.contains('Yahoo')]

                        # sort by headline THEN by impressions
#                         st.session_state.df_yahoos = st.session_state.df_yahoos.sort_values(
#                             ["Headline", "Impressions", "Author"], axis=0, ascending=[True, False, True])

                        # Save duplicate yahoo headlines -- NOTE - LOCAL VARIABLE ISSUE
#                         dupe_yahoos = st.session_state.df_yahoos[
#                             st.session_state.df_yahoos['Headline'].duplicated(keep='first') == True]

                        # drop duplicates (to dupe dataframe), keep first
#                         st.session_state.df_yahoos = st.session_state.df_yahoos[
#                             ~st.session_state.df_yahoos['Headline'].duplicated(keep='first') == True]

                        # rejoin yahoos to main
#                         frames = [st.session_state.df_raw, st.session_state.df_yahoos]
#                         st.session_state.df_raw = pd.concat(frames)

                        # st.write("DF YAHOOS")
                        # st.dataframe(st.session_state.df_yahoos)
                        #
                        # st.write("DUPE YAHOOS")
                        # st.dataframe(dupe_yahoos)



                    # Duplicate removal
                    if drop_dupes:

                        ### DROP DUPLICATES BY URL MATCHES #############

                        # Set aside blank URLs
                        blank_urls = st.session_state.df_raw[st.session_state.df_raw.URL.isna()]
                        st.session_state.df_raw = st.session_state.df_raw[~st.session_state.df_raw.URL.isna()]

                        # Add temporary dupe URL helper column
                        st.session_state.df_raw['URL_Helper'] = st.session_state.df_raw['URL'].str.lower()
                        st.session_state.df_raw['URL_Helper'] = st.session_state.df_raw['URL_Helper'].str.replace('http:', 'https:')

                        # Sort duplicate URLS
                        st.session_state.df_raw = st.session_state.df_raw.sort_values(["URL_Helper", "Author", "Impressions", "AVE"], axis=0,
                                                ascending=[True, True, False, False])
                        # Save duplicate URLS
                        dupe_urls = st.session_state.df_raw[st.session_state.df_raw['URL_Helper'].duplicated(keep='first') == True]

                        # Remove duplicate URLS
                        st.session_state.df_raw = st.session_state.df_raw[~st.session_state.df_raw['URL_Helper'].duplicated(keep='first') == True]

                        # Drop URL Helper column from both dfs
                        st.session_state.df_raw.drop(["URL_Helper"], axis=1, inplace=True, errors='ignore')
                        dupe_urls.drop(["URL_Helper"], axis=1, inplace=True, errors='ignore')

                        frames = [st.session_state.df_raw, blank_urls]
                        st.session_state.df_raw = pd.concat(frames)


                        ### DROP DUPLICATES BY COLUMN MATCHES #############


                        # Split off records with blank headline/outlet/type
                        blank_set = st.session_state.df_raw[st.session_state.df_raw.Headline.isna() | st.session_state.df_raw.Outlet.isna() | st.session_state.df_raw.Type.isna() | len(st.session_state.df_raw.Headline) == 0]
                        # st.session_state.df_raw = st.session_state.df_raw[~st.session_state.df_raw.Headline.isna() | ~st.session_state.df_raw.Outlet.isna() | ~st.session_state.df_raw.Type.isna() | ~len(st.session_state.df_raw.Headline) == 0]
                        st.session_state.df_raw = st.session_state.df_raw[~st.session_state.df_raw.Headline.isna()]
                        st.session_state.df_raw = st.session_state.df_raw[~st.session_state.df_raw.Outlet.isna()]
                        st.session_state.df_raw = st.session_state.df_raw[~st.session_state.df_raw.Type.isna()]
                        # st.session_state.df_raw = st.session_state.df_raw[~(len(st.session_state.df_raw.Headline) < 1)]


                        # Add helper column
                        st.session_state.df_raw["dupe_helper"] = st.session_state.df_raw['Type'].astype('string') + st.session_state.df_raw['Outlet'].astype('string') + st.session_state.df_raw[
                            'Headline']
                        st.session_state.df_raw = st.session_state.df_raw.sort_values(["dupe_helper", "Author", "Impressions", "AVE"], axis=0,
                                                ascending=[True, True, False, False])
                        dupe_cols = st.session_state.df_raw[st.session_state.df_raw['dupe_helper'].duplicated(keep='first') == True]
                        st.session_state.df_raw = st.session_state.df_raw[~st.session_state.df_raw['dupe_helper'].duplicated(keep='first') == True]


                        # Drop helper column and rejoin broadcast
                        st.session_state.df_raw.drop(["dupe_helper"], axis=1, inplace=True, errors='ignore')
                        dupe_cols.drop(["dupe_helper"], axis=1, inplace=True, errors='ignore')
                        frames = [st.session_state.df_raw, st.session_state.broadcast_set, st.session_state.blank_set]
                        st.session_state.df_traditional = pd.concat(frames)
                        st.session_state.df_dupes = pd.concat([dupe_urls, dupe_cols, dupe_yahoos])


                    else:
                        frames = [st.session_state.df_raw, st.session_state.broadcast_set]
                        st.session_state.df_traditional = pd.concat(frames)

                    del st.session_state.df_raw

                    # original_trad_auths = (top_x_by_mentions(st.session_state.df_traditional, "Author"))
                    # st.session_state.original_trad_auths = original_trad_auths
                    st.session_state.standard_step = True
                    st.experimental_rerun()



elif page == "3: Authors - Missing":
    st.title('Authors - Missing')
    # original_trad_auths = st.session_state.original_trad_auths

    if st.session_state.upload_step == False:
        st.error('Please upload a CSV before trying this step.')

    elif st.session_state.standard_step == False:
        st.error('Please run the Standard Cleaning before trying this step.')
    elif len(st.session_state.df_traditional) == 0:
        st.subheader("No traditional media in data. Skip to next step.")

    else:
        counter = st.session_state.counter
        original_top_authors = st.session_state.original_auths


        def fix_author(df, headline_text, new_author):
            """Updates all authors for a given headline"""
            df.loc[df["Headline"] == headline_text, "Author"] = new_author


        def headline_authors(df, headline_text):
            """Returns the various authors for a given headline"""
            headline_authors = (df[df.Headline == headline_text].Author.value_counts().reset_index())
            return headline_authors


        headline_table = st.session_state.df_traditional[['Headline', 'Mentions', 'Author']]
        headline_table = headline_table.groupby("Headline").count()
        headline_table["Missing"] = headline_table["Mentions"] - headline_table["Author"]
        headline_table = headline_table[(headline_table["Author"] > 0) & (headline_table['Missing'] > 0)].sort_values(
            "Missing", ascending=False).reset_index()
        headline_table.rename(columns={'Author': 'Known', 'Mentions': 'Total'},
                              inplace=True, errors='raise')

        temp_headline_list = headline_table
        if counter < len(temp_headline_list):
            headline_text = temp_headline_list.iloc[counter]['Headline']

            but1, col3, but2 = st.columns(3)
            with but1:
                next_auth = st.button('Skip to Next Headline')
                if next_auth:
                    counter += 1
                    st.session_state.counter = counter
                    st.experimental_rerun()

            if counter > 0:
                with col3:
                    st.write(f"Skipped: {counter}")
                with but2:
                    reset_counter = st.button('Reset Skip Counter')
                    if reset_counter:
                        counter = 0
                        st.session_state.counter = counter
                        st.experimental_rerun()

            possibles = headline_authors(st.session_state.df_traditional, headline_text)['index'].tolist()

            # CSS to inject contained in a string
            hide_table_row_index = """
                                <style>
                                tbody th {display:none}
                                .blank {display:none}
                                </style>
                                """
            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([12, 1, 9])
            with col1:
                st.subheader("Headline")
                st.table(headline_table.iloc[[counter]])
            with col2:
                st.write(" ")
            with col3:
                st.subheader("Authors in CSV")
                if len(headline_authors(st.session_state.df_traditional, headline_text)) > 5:
                    st.dataframe(headline_authors(st.session_state.df_traditional, headline_text).rename(columns={'index': 'Possible Author(s)',
                                                                                      'Author': 'Matches'}))
                else:
                    st.table(headline_authors(st.session_state.df_traditional, headline_text).rename(
                        columns={'index': 'Possible Author(s)',
                                 'Author': 'Matches'}))

            with st.form('auth updater', clear_on_submit=True):

                col1, col2, col3 = st.columns([8, 1, 8])
                with col1:
                    box_author = st.selectbox('Pick from possible Authors', possibles,
                                              help='Pick from one of the authors already associated with this headline.')

                with col2:
                    st.write(" ")
                    st.subheader("OR")

                with col3:
                    string_author = st.text_input("Write in the author name",
                                                  help='Override above selection by writing in a custom name.')

                if len(string_author) > 0:
                    new_author = string_author
                else:
                    new_author = box_author

                submitted = st.form_submit_button("Update Author")
                if submitted:
                    fix_author(st.session_state.df_traditional, headline_text, new_author)
                    st.experimental_rerun()
        else:
            st.info("You've reached the end of the list!")
            if counter > 0:
                reset_counter = st.button('Reset Counter')
                if reset_counter:
                    counter = 0
                    st.session_state.counter = counter
                    st.experimental_rerun()
            else:
                st.success("✓ Nothing left to update here.")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Top Authors")
            st.dataframe(st.session_state.original_trad_auths)

        with col2:
            st.subheader("New Top Authors")
            st.dataframe((top_x_by_mentions(st.session_state.df_traditional, "Author")))

        # st.subheader("Fixable Author Stats")
        # stats = (fixable_headline_stats(traditional, primary="Headline", secondary="Author"))
        # st.text(stats)
        # st.dataframe(st.session_state.df_traditional)


elif page == "4: Authors - Outlets":
    st.title("Author - Outlets")
    if st.session_state.upload_step == False:
        st.error('Please upload a CSV before trying this step.')
    elif st.session_state.standard_step == False:
        st.error('Please run the Standard Cleaning before trying this step.')
    else:
        from unidecode import unidecode
        import requests
        from requests.structures import CaseInsensitiveDict

        st.session_state.df_traditional.Mentions = st.session_state.df_traditional.Mentions.astype('int')
        auth_outlet_skipped = st.session_state.auth_outlet_skipped
        auth_outlet_table = st.session_state.auth_outlet_table
        # top_auths_by = st.session_state.top_auths_by

        def fetch_outlet(author_name):
            contact_url = "https://mediadatabase.agilitypr.com/api/v4/contacts/search"
            headers = CaseInsensitiveDict()
            headers["Content-Type"] = "text/json"
            headers["Accept"] = "text/json"
            headers["Authorization"] = st.secrets["authorization"]
            headers["client_id"] = st.secrets["client_id"]
            headers["userclient_id"] = st.secrets["userclient_id"]

            data_a = '''
          {  
            "aliases": [  
              "'''

            data_b = '''"  
            ]   
          }
          '''

            data = data_a + author_name + data_b
            contact_resp = requests.post(contact_url, headers=headers, data=data)

            return contact_resp.json()


        def reset_skips():
            st.session_state.auth_outlet_skipped = 0


        def name_match(series):
            non_match = 'color: #985331;'
            match = 'color: goldenrod'
            return [non_match if cell_value != author_name else match for cell_value in series]


        st.session_state.top_auths_by = st.selectbox('Top Authors by: ', ['Mentions', 'Impressions'], on_change=reset_skips)
        # st.session_state.top_auths_by = top_auths_by
        if len(auth_outlet_table) == 0:
            if st.session_state.top_auths_by == 'Mentions':
                auth_outlet_table = st.session_state.df_traditional[['Author', 'Mentions', 'Impressions']].groupby(
                    by=['Author']).sum().sort_values(
                    ['Mentions', 'Impressions'], ascending=False).reset_index()
                auth_outlet_table['Outlet'] = ''
                auth_outlet_todo = auth_outlet_table

            if st.session_state.top_auths_by == 'Impressions':
                auth_outlet_table = st.session_state.df_traditional[['Author', 'Mentions', 'Impressions']].groupby(
                    by=['Author']).sum().sort_values(
                    ['Impressions', 'Mentions'], ascending=False).reset_index()
                auth_outlet_table['Outlet'] = ''
                auth_outlet_todo = auth_outlet_table

        else:
            if st.session_state.top_auths_by == 'Mentions':
                auth_outlet_table = auth_outlet_table.sort_values(['Mentions', 'Impressions'],
                                                                  ascending=False)  # .reset_index()
                auth_outlet_todo = auth_outlet_table.loc[auth_outlet_table['Outlet'] == '']

            if st.session_state.top_auths_by == 'Impressions':
                auth_outlet_table = auth_outlet_table.sort_values(['Impressions', 'Mentions'],
                                                                  ascending=False)  # .reset_index()
                auth_outlet_todo = auth_outlet_table.loc[auth_outlet_table['Outlet'] == '']

        auth_outlet_skipped = st.session_state.auth_outlet_skipped

        if auth_outlet_skipped < len(auth_outlet_todo):
            author_name = auth_outlet_todo.iloc[auth_outlet_skipped]['Author']

            # NAME, SKIP & RESET SKIP SECTION
            col1, but1, but2 = st.columns([2, 1, 1])
            with col1:
                st.markdown("""
                                <h2 style="color: goldenrod; padding-top:0!important; margin-top:-"> 
                                """ + author_name +
                            """</h2>
                            <style>.css-12w0qpk {padding-top:22px !important}</style>
                            """, unsafe_allow_html=True)
            with but1:
                next_auth = st.button('Skip to Next Author')
                if next_auth:
                    auth_outlet_skipped += 1
                    st.session_state.auth_outlet_skipped = auth_outlet_skipped
                    st.experimental_rerun()

                with but2:
                    reset_counter = st.button('Reset Skips')
                    if reset_counter:
                        auth_outlet_skipped = 0
                        st.session_state.auth_outlet_skipped = auth_outlet_skipped
                        st.experimental_rerun()

            search_results = fetch_outlet(unidecode(author_name))

            db_outlets = []

            if 'results' in search_results:
                number_of_authors = len(search_results['results'])


                if search_results['results'] == []:
                    matched_authors = []
                elif search_results['results'] == None:
                    matched_authors = []
                else:
                    response_results = search_results['results']
                    outlet_results = []

                    for result in response_results:
                        auth_name = result['firstName'] + " " + result['lastName']
                        job_title = result['primaryEmployment']['jobTitle']
                        outlet = result['primaryEmployment']['outletName']
                        if result['country'] == None:
                            country = ''

                        else:
                            country = result['country']['name']
                        auth_tuple = (auth_name, job_title, outlet, country)
                        outlet_results.append(auth_tuple)

                    matched_authors = pd.DataFrame.from_records(outlet_results,
                                                                columns=['Name', 'Title', 'Outlet', 'Country'])
                    matched_authors.loc[matched_authors.Outlet == "[Freelancer]", "Outlet"] = "Freelance"

                    db_outlets = matched_authors.Outlet.tolist()

            # OUTLETS IN COVERAGE VS DATABASE
            # CSS to inject contained in a string
            hide_table_row_index = """
                                            <style>
                                            tbody th {display:none}
                                            .blank {display:none}
                                            </style>
                                            """

            hide_dataframe_row_index = """
                        <style>
                        .row_heading.level0 {width:0; display:none}
                        .blank {width:0; display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([8, 1, 16])
            with col1:
                st.subheader("Outlets in CSV")  #########################################
                outlets_in_coverage = st.session_state.df_traditional.loc[st.session_state.df_traditional.Author == author_name].Outlet.value_counts()
                outlets_in_coverage_list = outlets_in_coverage.index
                outlets_in_coverage_list = outlets_in_coverage_list.insert(0, "Freelance")
                outlets_in_coverage = outlets_in_coverage.rename_axis('Outlet').reset_index(name='Hits')

                if len(outlets_in_coverage) > 7:
                    st.dataframe(outlets_in_coverage.style.apply(
                    lambda x: ['background: goldenrod; color: black' if v in db_outlets else "" for v in x],
                    axis=1))
                else:
                    st.table(outlets_in_coverage.style.apply(
                        lambda x: ['background: goldenrod; color: black' if v in db_outlets else "" for v in x],
                        axis=1))

            with col2:
                st.write(" ")

            with col3:
                st.subheader("Media Database Results")  #####################################
                if 'results' not in search_results:
                    st.warning("NO MATCH FOUND")
                    matched_authors = []
                elif search_results['results'] == []:
                    st.warning("NO MATCH FOUND")
                    matched_authors = []
                elif search_results == None:
                    st.warning("NO MATCH FOUND")
                    matched_authors = []

                else:
                    response_results = search_results['results']
                    outlet_results = []

                    for result in response_results:
                        auth_name = result['firstName'] + " " + result['lastName']
                        job_title = result['primaryEmployment']['jobTitle']
                        outlet = result['primaryEmployment']['outletName']
                        if result['country'] == None:
                            country = 'None'

                        else:
                            country = result['country']['name']
                        auth_tuple = (auth_name, job_title, outlet, country)
                        outlet_results.append(auth_tuple)

                    matched_authors = pd.DataFrame.from_records(outlet_results,
                                                                columns=['Name', 'Title', 'Outlet', 'Country'])
                    matched_authors.loc[matched_authors.Outlet == "[Freelancer]", "Outlet"] = "Freelance"

                    if len(matched_authors) > 7:
                        st.dataframe(matched_authors.style.apply(lambda x: [
                        'background: goldenrod; color: black' if v in outlets_in_coverage.Outlet.tolist() else "" for v
                        in x], axis=1).apply(name_match, axis=0, subset='Name'))
                    else:
                        st.table(matched_authors.style.apply(lambda x: [
                            'background: goldenrod; color: black' if v in outlets_in_coverage.Outlet.tolist() else ""
                            for v
                            in x], axis=1).apply(name_match, axis=0, subset='Name'))

                    possibles = matched_authors.Outlet

            # FORM TO UPDATE AUTHOR OUTLET ######################
            with st.form('auth updater', clear_on_submit=True):
                col1, col2, col3 = st.columns([8, 1, 8])
                with col1:
                    if len(matched_authors) > 0:
                        box_outlet = st.selectbox('Pick outlet from DATABASE MATCHES', possibles,
                                                  help='Pick from one of the outlets associated with this author name.')

                    else:
                        box_outlet = st.selectbox('Pick outlet from COVERAGE or "Freelance"', outlets_in_coverage_list)

                with col2:
                    st.write(" ")
                    st.subheader("OR")
                with col3:
                    string_outlet = st.text_input("Write in an outlet name",
                                                  help='Override above selection by writing in a custom name.')

                submitted = st.form_submit_button("Assign Outlet")

            if submitted:
                if len(string_outlet) > 0:
                    new_outlet = string_outlet
                else:
                    new_outlet = box_outlet

                auth_outlet_table.loc[auth_outlet_table["Author"] == author_name, "Outlet"] = new_outlet
                st.session_state.auth_outlet_skipped = auth_outlet_skipped
                st.session_state.auth_outlet_table = auth_outlet_table
                st.experimental_rerun()

            col1, col2, col3 = st.columns([8, 1, 4])
            with col1:
                st.subheader("Top Authors")
                if 'Outlet' in auth_outlet_table.columns:
                    if st.session_state.top_auths_by == 'Mentions':
                        st.table(
                            auth_outlet_table[['Author', 'Outlet', 'Mentions', 'Impressions']].fillna('').sort_values(
                                ['Mentions', 'Impressions'], ascending=False).head(15).style.format(format_dict, na_rep=' '))
                    if st.session_state.top_auths_by == 'Impressions':
                        st.table(
                            auth_outlet_table[['Author', 'Outlet', 'Mentions', 'Impressions']].fillna('').sort_values(
                                ['Impressions', 'Mentions'], ascending=False).head(15).style.format(format_dict, na_rep=' '))

                else:
                    st.table(auth_outlet_table[['Author', 'Mentions', 'Impressions']].fillna('').head(15).style.format(
                        format_dict, na_rep=' '))
            with col2:
                st.write(" ")
            with col3:
                st.subheader('Outlets assigned')

                if 'Outlet' in auth_outlet_table.columns:
                    assigned = len(auth_outlet_table.loc[auth_outlet_table['Outlet'] != ''])
                    st.metric(label='Assigned', value=assigned)
                else:
                    st.metric(label='Assigned', value=0)
        else:
            st.info("You've reached the end of the list!")
            st.write(f"Authors skipped: {auth_outlet_skipped}")
            # st.write(f"To Do: {len(auth_outlet_todo)}")
            if auth_outlet_skipped > 0:
                reset_counter = st.button('Reset Counter')
                if reset_counter:
                    auth_outlet_skipped = 0
                    st.session_state.auth_outlet_skipped = auth_outlet_skipped
                    st.experimental_rerun()
            else:
                st.write("✓ Nothing left to update here.")


elif page == "5: Translation":
    st.title('Translation')
    from deep_translator import GoogleTranslator
    from concurrent.futures import ThreadPoolExecutor
    from titlecase import titlecase

    traditional = st.session_state.df_traditional
    # social = st.session_state.df_social
    if st.session_state.upload_step == False:
        st.error('Please upload a CSV before trying this step.')
    elif st.session_state.standard_step == False:
        st.error('Please run the Standard Cleaning before trying this step.')
    elif st.session_state.translated_headline == True and st.session_state.translated_snippet == True and st.session_state.translated_summary == True:
        st.subheader("✓ Translation complete.")
        trad_non_eng = len(traditional[traditional['Language'] != 'English'])
        soc_non_eng = len(st.session_state.df_social[st.session_state.df_social['Language'] != 'English'])

        if trad_non_eng > 0:
            with st.expander("Traditional - Non-English"):
                st.dataframe(traditional[traditional['Language'] != 'English'][
                                 ['Outlet', 'Headline', 'Snippet', 'Summary', 'Language', 'Country']])

        if soc_non_eng > 0:
            with st.expander("Social - Non-English"):
                st.dataframe(st.session_state.df_social[st.session_state.df_social['Language'] != 'English'][
                                 ['Outlet', 'Snippet', 'Summary', 'Language', 'Country']])
    elif len(traditional[traditional['Language'] != 'English']) == 0 and len(
            st.session_state.df_social[st.session_state.df_social['Language'] != 'English']) == 0:
        st.subheader("No translation required")
    else:
        def translate_col(df, name_of_column):
            """Replaces non-English string in column with English"""
            global dictionary
            dictionary = {}
            unique_non_eng = list(set(df[name_of_column][df['Language'] != 'English'].dropna()))
            if '' in unique_non_eng:
                unique_non_eng.remove('')
            with st.spinner('Running translation now...'):
                with ThreadPoolExecutor(max_workers=30) as ex:
                    results = ex.map(translate, [text for text in unique_non_eng])
            df[name_of_column].replace(dictionary, inplace=True)


        def translate(text):
            dictionary[text] = (GoogleTranslator(source='auto', target='en').translate(text[:1500]))


        def translation_stats_combo():
            non_english_records = len(traditional[traditional['Language'] != 'English']) + len(
                st.session_state.df_social[st.session_state.df_social['Language'] != 'English'])

            st.write(f"There are {non_english_records} non-English records in your data.")


        translation_stats_combo()
        if len(traditional) > 0:
            with st.expander("Traditional - Non-English"):
                st.dataframe(traditional[traditional['Language'] != 'English'][
                                 ['Outlet', 'Headline', 'Snippet', 'Summary', 'Language', 'Country']])

        if len(st.session_state.df_social) > 0:
            with st.expander("Social - Non-English"):
                st.dataframe(st.session_state.df_social[st.session_state.df_social['Language'] != 'English'][
                                 ['Outlet', 'Snippet', 'Summary', 'Language', 'Country']])

        with st.form('translation_form'):
            st.subheader("Pick columns for translations")
            st.warning("WARNING: Translation will over-write the original text.")

            if len(traditional) > 0:
                if st.session_state.translated_headline == False:
                    headline_to_english = st.checkbox('Headline', value=True)
                else:
                    st.success('✓ Headlines translated.')
                    headline_to_english = False
            else:
                headline_to_english = False

            if st.session_state.translated_snippet == False:
                snippet_to_english = st.checkbox('Snippet', value=True)
            else:
                st.success('✓ Snippets translated.')
                snippet_to_english = False

            if st.session_state.translated_summary == False:
                summary_to_english = st.checkbox('Summary', value=True)
            else:
                st.success('✓ Summaries translated.')
                summary_to_english = False

            submitted = st.form_submit_button("Go!")
            if submitted:
                st.warning("Stay on this page until translation is complete")

                if headline_to_english:
                    traditional['Original Headline'] = traditional.Headline
                    translate_col(traditional, 'Headline')

                    # AP Cap
                    broadcast_array = ['RADIO', 'TV']
                    broadcast = traditional.loc[traditional['Type'].isin(broadcast_array)]
                    traditional = traditional[~traditional['Type'].isin(broadcast_array)]
                    traditional[['Headline']] = traditional[['Headline']].fillna('')
                    traditional['Headline'] = traditional['Headline'].map(lambda Headline: titlecase(Headline))
                    frames = [traditional, broadcast]
                    traditional = pd.concat(frames)

                    st.session_state.df_social['Original Headline'] = st.session_state.df_social.Headline

                    translate_col(st.session_state.df_social, 'Headline')
                    st.session_state.translated_headline = True
                    st.success(f'Done translating headlines!')
                if summary_to_english:
                    translate_col(traditional, 'Summary')
                    translate_col(st.session_state.df_social, 'Summary')
                    st.session_state.translated_summary = True
                    st.success(f'Done translating summaries!')
                if snippet_to_english:
                    translate_col(traditional, 'Snippet')
                    translate_col(st.session_state.df_social, 'Snippet')
                    st.session_state.translated_snippet = True
                    st.success(f'Done translating snippets!')
                st.session_state.df_traditional = traditional
                # st.session_state.df_social = social
                st.experimental_rerun()



elif page == "6: Download":
    st.title('Download')
    import io

    if st.session_state.upload_step == False:
        st.error('Please upload a CSV before trying this step.')
    elif st.session_state.standard_step == False:
        st.error('Please run the Standard Cleaning before trying this step.')
    else:
        export_name = st.session_state.export_name

        traditional = st.session_state.df_traditional
        social = st.session_state.df_social
        # dupes = st.session_state.df_dupes
        # uncleaned = st.session_state.df_untouched
        auth_outlet_table = st.session_state.auth_outlet_table


        # Split datetime back to 2 columns  - $$$  Maybe optional  $$$
        # df['Date'] = df.Datetime.dt.date
        # df['Time'] = df.Datetime.dt.time
        # df.drop(["Datetime"], axis = 1, inplace=True, errors='ignore')

        # Tag exploder
        if "Tags" in st.session_state.df_traditional:
            traditional['Tags'] = traditional['Tags'].astype(str)  # needed if column there but all blank
            traditional = traditional.join(traditional["Tags"].str.get_dummies(sep=",").astype('category'), how='left', rsuffix=' (tag)')


        if "Tags" in social:
            social['Tags'] = social['Tags'].astype(str)  # needed if column there but all blank
            social = social.join(social["Tags"].str.get_dummies(sep=",").astype('category'), how='left', rsuffix=' (tag)')


        with st.form("my_form_download"):
            st.subheader("Generate your cleaned data workbook")
            submitted = st.form_submit_button("Go!")
            if submitted:
                with st.spinner('Building workbook now...'):

                    output = io.BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter', datetime_format='yyyy-mm-dd',
                                            options={'in_memory': True})
                    workbook = writer.book
                    cleaned_dfs = []
                    cleaned_sheets = []

                    # Add some cell formats.
                    number_format = workbook.add_format({'num_format': '#,##0'})
                    currency_format = workbook.add_format({'num_format': '$#,##0'})

                    if len(traditional) > 0:
                        traditional = traditional.sort_values(by=['Impressions'], ascending=False)
                        traditional.to_excel(writer, sheet_name='CLEAN TRAD', startrow=1, header=False, index=False)
                        worksheet1 = writer.sheets['CLEAN TRAD']
                        worksheet1.set_tab_color('black')
                        cleaned_dfs.append((traditional, worksheet1))
                        cleaned_sheets.append(worksheet1)

                    if len(social) > 0:
                        social = social.sort_values(by=['Impressions'], ascending=False)
                        social.to_excel(writer, sheet_name='CLEAN SOCIAL', startrow=1, header=False, index=False)
                        worksheet2 = writer.sheets['CLEAN SOCIAL']
                        worksheet2.set_tab_color('black')
                        cleaned_dfs.append((social, worksheet2))
                        cleaned_sheets.append(worksheet2)

                    if len(auth_outlet_table) > 0:
                        authors = auth_outlet_table.sort_values(by=['Mentions', 'Impressions'], ascending=False)
                        authors.to_excel(writer, sheet_name='Authors', header=True, index=False)
                        worksheet5 = writer.sheets['Authors']
                        worksheet5.set_tab_color('green')
                        worksheet5.set_default_row(22)
                        worksheet5.set_column('A:A', 30, None)  # author
                        worksheet5.set_column('B:B', 12, None)  # mentions
                        worksheet5.set_column('C:C', 15, number_format)  # impressions
                        worksheet5.set_column('D:D', 35, None)  # outlet
                        worksheet5.freeze_panes(1, 0)

                        cleaned_dfs.append((authors, worksheet5))

                    if len(st.session_state.df_dupes) > 0:
                        st.session_state.df_dupes.to_excel(writer, sheet_name='DLTD DUPES', header=True, index=False)
                        worksheet3 = writer.sheets['DLTD DUPES']
                        worksheet3.set_tab_color('#c26f4f')
                        cleaned_dfs.append((st.session_state.df_dupes, worksheet3))
                        cleaned_sheets.append(worksheet3)

                    st.session_state.df_untouched.drop(["Mentions"],
                                                 axis=1, inplace=True, errors='ignore')
                    st.session_state.df_untouched.to_excel(writer, sheet_name='RAW', header=True, index=False)
                    # TODO: RAW tab - for top row: freeze, align left, no borders
                    worksheet4 = writer.sheets['RAW']
                    worksheet4.set_tab_color('#c26f4f')
                    cleaned_dfs.append((st.session_state.df_untouched, worksheet4))

                    for clean_df in cleaned_dfs:
                        (max_row, max_col) = clean_df[0].shape
                        column_settings = [{'header': column} for column in clean_df[0].columns]
                        clean_df[1].add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})


                    # Add the Excel table structure. Pandas will add the data.
                    for sheet in cleaned_sheets:
                        sheet.set_default_row(22)
                        sheet.set_column('A:A', 12, None)  # datetime
                        sheet.set_column('B:B', 22, None)  # outlet
                        sheet.set_column('C:C', 10, None)  # type
                        sheet.set_column('D:D', 12, None)  # author
                        sheet.set_column('E:E', 0, None)  # mentions
                        sheet.set_column('F:F', 12, number_format)  # impressions
                        sheet.set_column('G:G', 40, None)  # headline
                        sheet.set_column('Q:Q', 12, currency_format)  # AVE
                        sheet.freeze_panes(1, 0)

                    writer.save()

        if submitted:
            st.download_button('Download', output, file_name=export_name)
