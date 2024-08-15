# import all libraries
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Depl Analytics",
    page_icon='📊'
)

st.title(':rainbow[DEPL Analytics Portal]')
st.header(':grey[Explore data and generate insights to take data driven decision]', divider='rainbow')

# file uploader to import file
file = st.file_uploader(':rainbow[Import CSV or Excel file]', type=['csv', 'xlsx'])
if(file != None):
    if(file.name.endswith('csv')):
        data = pd.read_csv(file)
        st.info('Your csv file is uploaded', icon='analysis.png')
    else:
        data = pd.read_excel(file)

    st.info('File uploaded successfully', icon='✅')
    st.dataframe(data)

    #basic information dashboard
    st.subheader(':rainbow[Basic information of the dataset]', divider='rainbow')
    tab1, tab2, tab3, tab4 = st.tabs(['Summary', 'Top and Bottom Rows', 'Datatypes', 'Columns'])

    with tab1:
        st.write(f':blue[There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset.]')
        st.subheader(':grey[Statistical Summary of the dataset]')
        st.dataframe(data.describe())

    with tab2:
        #for top rows
        st.subheader(':grey[Top Rows]')
        topRows = st.slider('Select the number of rows you want', 1, data.shape[0], key='topslider')
        st.dataframe(data.head(topRows))

        #for bottom rows
        st.subheader(':grey[Bottom Rows]')
        bottomRows = st.slider('Select the number of rows you want', 1, data.shape[0], key='bottomslider')
        st.dataframe(data.tail(bottomRows))

    with tab3:
        st.subheader(':grey[Columns of the dataset]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader(':grey[Column name of the dataset]')
        st.dataframe(data.columns)
    
    st.subheader(':rainbow[Column value to count]', divider='rainbow')
    with st.expander('Value Count'):
        col1, col2 = st.columns(2)
        with col1:
            column = st.selectbox('Choose column name', options=list(data.columns))
        with col2:
            topRows = st.number_input('Top Rows', min_value=1, step=1)
        submit = st.button('Submit')
        if(submit == True):
            result = data[column].value_counts().reset_index().head(topRows)
            st.dataframe(result)
            st.subheader('Data Visualisation', divider='grey')
            fig = px.bar(data_frame=result, x=column, y='count', text='count', template='plotly_white')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result, x=column, y= 'count', text='count', template='plotly_white')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result, names=column, values='count', template='plotly_white')
            st.plotly_chart(fig)

    st.subheader(':rainbow[Groupby: Simplify your data]', divider='rainbow')
    st.write(':grey[Groupby lets you summarize data by specific categories or group]')
    with st.expander('Data Visualization'):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose your columns', options=list(data.columns))
        with col2:
            operation_cols = st.selectbox('Coose your operation column', options=list(data.columns))
        with col3:
            operation = st.selectbox('Select Operation', options=['sum', 'max', 'min', 'mean', 'median', 'count'])

        if(groupby_cols):
            result = data.groupby(groupby_cols).agg(
                newcol = (operation_cols, operation)
            ).reset_index()

            st.dataframe(result)

            st.subheader(':rainbow[Visualization: make your data understandable]', divider='rainbow')
            graphs = st.selectbox('Select Chart', options=['line', 'bar', 'scatter', 'pie', 'sunburst'])
            if(graphs == 'line'):
                x_axis = st.selectbox('Select X Axis', options=list(result.columns))
                y_axis = st.selectbox('Select Y Axis', options=list(result.columns))
                colour_info = st.selectbox('Select Coloured Axis', options=[None] + list(result.columns))
                fig  = px.line(data_frame=result, x = x_axis, y = y_axis, color=colour_info, markers='o')
                st.plotly_chart(fig)

            if(graphs == 'bar'):
                x_axis = st.selectbox('Select X Axis', options=list(result.columns))
                y_axis = st.selectbox('Select Y Axis', options=list(result.columns))
                colour_info = st.selectbox('Select Coloured Axis', options=[None] + list(result.columns))
                col_info = st.selectbox('Select column information', options=[None] + list(result.columns))
                fig  = px.bar(data_frame=result, x = x_axis, y = y_axis, color=colour_info, facet_col=col_info, barmode='group')
                st.plotly_chart(fig)

            elif(graphs == 'scatter'):
                x_axis = st.selectbox('Select X Axis', options=list(result.columns))
                y_axis = st.selectbox('Select Y Axis', options=list(result.columns))
                colour_info = st.selectbox('Select Coloured Axis', options=[None] + list(result.columns))
                size_info = st.selectbox('Size', options=[None] + list(result.columns))
                fig  = px.scatter(data_frame=result, x = x_axis, y = y_axis, color=colour_info, size=size_info)
                st.plotly_chart(fig)

            elif(graphs == 'pie'):
                values = st.selectbox('Select numerical value', options=list(result.columns))
                names = st.selectbox('Select labels', options=list(result.columns))
                fig  = px.pie(data_frame=result, values=values, names=names, template='plotly_white')
                st.plotly_chart(fig)

            elif(graphs == 'sunburst'):
                path_col = st.multiselect('Select your path', options=list(result.columns))
                values_col = st.selectbox('Slect numerical column', options=[None] + list(result.columns))
                fig = px.sunburst(data_frame=result, path=path_col, values=values_col)
                st.plotly_chart(fig)




            

        




