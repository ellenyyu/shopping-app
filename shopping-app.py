'''
Additional things to implement: 
- Filter out Twitter, Youtube aka social media links
- Integrate LTK, Instagram, Google, Pinterest
- Use cases: for style discovery, for brand discovery, for product recommendations
- return images instead of opening new browser windows
'''
import streamlit as st 
from datetime import datetime
from channel_url import get_channel_id_from_url , get_video_data
from search_string import search_youtube_videos
from app_utils import reset_start_stop, generate_open_urls_script
import pandas as pd
#import webbrowser
#import os 
#from dotenv import load_dotenv 
import streamlit.components.v1 as components

#load_dotenv() 

st.set_page_config(layout="wide")

API_KEY = st.secrets['YOUTUBE_API_KEY']

with st.expander('(Optional) Enter your Youtube API Key'):
	api_key = st.text_input('Youtube API Key', value = None, label_visibility='collapsed')

if api_key is None:
	api_key = API_KEY

adv_select = st.radio('Choose your adventure', 
	['enter a channel url', 'enter a search string'], 
	horizontal = True, 
	on_change=reset_start_stop)

if adv_select == 'enter a channel url': 

	channel_url = st.text_input('Please enter a channel url', value = 'https://www.youtube.com/@HelloDavid', on_change=reset_start_stop)

	with st.expander('Options'):
		step_select = int(st.text_input('enter a customized step size', value = '10'))
		max_select = int(st.text_input('enter a customized number of returns', value = '999999999'))
		format_string = '%m/%d/%Y'
		start_select = datetime.strptime(st.text_input('enter a customized start time in mm/dd/yyyy format', value = '01/01/2023'), format_string)
		end_select = datetime.strptime(st.text_input('enter a customized end time in mm/dd/yyyy format', value = '12/31/2023'), format_string)

	if len(channel_url) > 0: 

		channel_id = get_channel_id_from_url(channel_url)

		video_data = get_video_data(api_key=api_key, start_date=start_select, end_date=end_select, channel_id=channel_id, max_results=max_select)

		# Because I'm more used to working with pandas dataframe
		df = pd.DataFrame(video_data)
		df['number_of_links'] = df.links.apply(lambda x: len(x))
		df = df[df['number_of_links']>0]

		start = 0
		stop = start

		if 'start' not in st.session_state:
			st.session_state.start = 0

		if 'stop' not in st.session_state:
			st.session_state.stop = st.session_state.start

		launch = st.button(f'Launch {step_select} links')

		if launch:
			st.session_state.start = st.session_state.stop
			st.session_state.stop += step_select

			# st.write('start', st.session_state.start)
			# st.write('stop', st.session_state.stop)

			for link in df.links.explode().drop_duplicates()[st.session_state.start : st.session_state.stop]:     
			    #webbrowser.open(link)
			    html_script = generate_open_urls_script(link)
			    components.html(html_script)

if adv_select == 'enter a search string': 

	search_string = st.text_input('Please enter what you want to search', value = 'chairs for coding', on_change=reset_start_stop)

	with st.expander('Options'):
		metric_select = st.selectbox('enter a customized sort metric',
			options=['relevance', 'searchSortUnspecified', 'date', 'rating', 'viewCount','title', 'videoCount'], index=0)
		step_select = int(st.text_input('enter a customized step size', value = '10'))
		max_select = int(st.text_input('enter a customized number of returns', value = '999999999'))

	if len(search_string) > 0: 

		video_data = search_youtube_videos(api_key=api_key, search_term=search_string, return_by=metric_select, max_results=max_select)

		# Because I'm more used to working with pandas dataframe
		df = pd.DataFrame(video_data)
		df['number_of_links'] = df.links.apply(lambda x: len(x))
		df = df[df['number_of_links']>0].reset_index(drop=True)

		with st.expander("Thumbnails"):
			videos_to_keep = df.index.tolist()
			#st.write('first', videos_to_keep)
			col1, col2, col3 = st.columns(3)
			with col1: 
				df = df.iloc[videos_to_keep]
				for row in df.iloc[::3].itertuples():
					st.image(row[4], use_column_width=True)
					remove = st.checkbox(f"remove {row[1]}")
					if remove: 
						videos_to_keep.remove(row.Index)
	
			with col2: 
				for row in df.iloc[1::3].itertuples():
					st.image(row[4], use_column_width=True)
					remove = st.checkbox(f"remove {row[1]}")
					if remove: 
						videos_to_keep.remove(row.Index)
			with col3: 
				for row in df.iloc[2::3].itertuples():
					st.image(row[4], use_column_width=True)
					remove = st.checkbox(f"remove {row[1]}")
					if remove: 
						videos_to_keep.remove(row.Index)
			#st.write('second', videos_to_keep)
			df = df.iloc[videos_to_keep]		

		if 'start' not in st.session_state:
			st.session_state.start = 0

		if 'stop' not in st.session_state:
			st.session_state.stop = st.session_state.start

		launch = st.button(f'Launch {step_select} links')

		if launch:
			st.session_state.start = st.session_state.stop
			st.session_state.stop += step_select

			# st.write('start', st.session_state.start)
			# st.write('stop', st.session_state.stop)

			for link in df.links.explode().drop_duplicates()[st.session_state.start : st.session_state.stop]:     
			    #webbrowser.open(link)
			    html_script = generate_open_urls_script(link)
			    components.html(html_script)

			
			