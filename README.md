# Setup Environment

## Install condas
conda create --name main-ds python=3.9
conda activate main-ds

## Install libs
pip install numpy
pip install pandas
pip install matplotlib
pip install jupyter
pip install streamlit

# Run streamlit app
streamlit run dashboard/app.py
