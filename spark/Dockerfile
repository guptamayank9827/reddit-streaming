FROM spark:3.5.0-python3
USER root
COPY requirements.txt /app/requirements.txt
WORKDIR /app

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm

# Copy the rest of the files to the working directory
COPY . /app/

# Make the script executable
RUN chmod +x script.sh
RUN sed -i -e 's/\r$//' script.sh

# Run the script with spark-submit
CMD ["/app/script.sh"]