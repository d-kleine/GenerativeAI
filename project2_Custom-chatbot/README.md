# Project: Custom Chatbot

## Introduction
In today's fast-paced business environment, custom chatbots have emerged as indispensable tools for enhancing customer interactions and streamlining operations. Leveraging advanced technologies such as natural language processing and machine learning, custom chatbots offer businesses unprecedented opportunities to engage customers, drive sales, and improve efficiency.

Designed to address specific business needs and scenarios, custom chatbots serve as virtual assistants, guiding users through inquiries, resolving issues, and delivering personalized experiences. From customer service to sales and marketing, chatbots play a pivotal role in fostering seamless interactions and building lasting relationships with customers.

This project aims to empower businesses to harness the power of custom chatbots by providing a flexible platform for building and customizing chatbot solutions.

## Project Summary
This project involves creating a unique chatbot using OpenAI by incorporating a specific dataset tailored to the project's needs. The dataset is carefully chosen to fit the context of the project and is seamlessly integrated into the chatbot's codebase. The goal is to justify why this dataset is important, how it improves the chatbot's functionality, and to develop thoughtful questions to evaluate the chatbot's performance.

At the beginning of the project, the chosen dataset is introduced with a brief explanation of its relevance and how it aligns with the project's objectives. Furthermore, the chatbot's question-and-answer abilities are demonstrated before and after the dataset integration, highlighting the improvements made possible by the customized dataset. This showcases how the chatbot becomes more effective and insightful in responding to user queries within the defined scenario.

## Requirements

**Step 1: Setup Python**

Ensure Python 3.11 is installed on your system. If not, download and install it from the official Python website.

**Step 2: Setup a Virtual Environment**

Create Virtual Environment:

```bash
python -m venv genai
```
Activate on Windows:

```bash
genai\Scripts\activate
```

Activate on Unix/MacOS:
```bash
source genai/bin/activate
```

**Step 3: Install Dependencies**

Install the dependencies from the *requirements.txt* file:
```bash
pip install -r requirements.txt
```

**Step 4: Set up OpenAI API key**

You can either add the API key for all projects globally as an environment variable or setting the API key for a single project.

To set up an API key for a single project, create a local *.env* file in the project folder and add the key as OPENAI_API_KEY. Also, create a *.gitignore* file in the project root to ensure the *.env file* is not included in version control. After creating the files, copy the secret API key into the .env file.

The *.env* file should look like the following:

```OPENAI_API_KEY=sk-...```

For further information to step 1 to 4, please visit [Get up and running with the OpenAI API](https://platform.openai.com/docs/quickstart?context=python).

**Step 5: Run the code**

To run the code, make sure the project folder it the root folder. Run the Python code provided in `project.ipynb`.

## Implementation
For this Custom Chatbot project, a provided Fashion Trends dataset of articles, crawled from websites for digital media and entertainment, has been used. This dataset contains text information about fashion trends from the year 2023, including popular styles, colors, fabric types, and other key fashion details. As of the time the project has been set up, OpenAI does not have access to real-time or future data beyond January 2022, so it does not have information about Fashion trends of 2023. With the use of the OpenAI API, the chatbot calculates relevance by computing the similarity score between text embeddings using cosine similarity. This method will be employed to compare the performance of an OpenAI model (which does not go beyond January 2022) with the same OpenAI model ingesting context as textual information from the fashion trends 2023 dataset. By incorporating a custom dataset and employing Prompt Engineering for the custom query, the chatbot enhances its ability to generate responses that are contextually relevant and tailored to user inquiries.

The project consists of following steps:

1. **Choosing a Dataset and Explain the Scenario**: Selecting a dataset from the choices described in the Project Overview page and justifing the selection in the second cell of the notebook. Explaining why have choosen the dataset and its relevance to the project's scenario.

2. **Preparing the Dataset for the Custom Query Process**: Format the data to be loaded as a pandas dataframe with a column called "text".

3. **Performing the Custom Query Process**: Integrating the dataset and ensuring using the custom dataset.

4. **Writing Questions to Demonstrate Custom Performance**: Proving at least two questions that showcase how the model's responses differ without and with a custom prompt.

The contrasting responses vividly illustrate the impact of using a custom prompt when integrating the fashion trends 2023 dataset, showcasing discernible differences in the model's outputs, revealing new patterns and insights that the original OpenAI model, with its data cutoff in January 2022, cannot access.