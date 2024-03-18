# Project: Custom Chatbot

## Introduction
In today's fast-paced business environment, custom chatbots have emerged as indispensable tools for enhancing customer interactions and streamlining operations. Leveraging advanced technologies such as natural language processing and machine learning, custom chatbots offer businesses unprecedented opportunities to engage customers, drive sales, and improve efficiency.

Designed to address specific business needs and scenarios, custom chatbots serve as virtual assistants, guiding users through inquiries, resolving issues, and delivering personalized experiences. From customer service to sales and marketing, chatbots play a pivotal role in fostering seamless interactions and building lasting relationships with customers.

This project aims to empower businesses to harness the power of custom chatbots by providing a flexible platform for building and customizing chatbot solutions.

## Project Summary
This project involves creating a unique chatbot using OpenAI by incorporating a specific dataset tailored to the project's needs. The dataset is carefully chosen to fit the context of the project and is seamlessly integrated into the chatbot's codebase. The goal is to justify why this dataset is important, how it improves the chatbot's functionality, and to develop thoughtful questions to evaluate the chatbot's performance.

At the beginning of the project, the chosen dataset is introduced with a brief explanation of its relevance and how it aligns with the project's objectives. Furthermore, the chatbot's question-and-answer abilities are demonstrated before and after the dataset integration, highlighting the improvements made possible by the customized dataset. This showcases how the chatbot becomes more effective and insightful in responding to user queries within the defined scenario.

## Implementation
For this Custom Chatbot project, a provided Fashion Trends dataset of articles, crawled from websites for digital media and entertainment, has been used. This dataset contains text information about fashion trends from the year 2023, including popular styles, colors, fabric types, and other key fashion details. As of the time the project has been set up, OpenAI does not have access to real-time or future data beyond January 2022, so it does not have information about Fashion trends of 2023. With the use of the OpenAI API, the chatbot calculates relevance by computing the similarity score between text embeddings using cosine similarity. This method will be employed to compare the performance of an OpenAI model (which does not go beyond January 2022) with the same OpenAI model ingesting context as textual information from the fashion trends 2023 dataset. By incorporating a custom dataset and employing Prompt Engineering for the custom query, the chatbot enhances its ability to generate responses that are contextually relevant and tailored to user inquiries.

The project consists of following steps:

1. **Choosing a Dataset and Explain the Scenario**: Selecting a dataset from the choices described in the Project Overview page and justifing the selection in the second cell of the notebook. Explaining why have choosen the dataset and its relevance to the project's scenario.

2. **Preparing the Dataset for the Custom Query Process**: Format the data to be loaded as a pandas dataframe with a column called "text".

3. **Performing the Custom Query Process**: Integrating the dataset and ensuring using the custom dataset.

4. **Writing Questions to Demonstrate Custom Performance**: Proving at least two questions that showcase how the model's responses differ without and with a custom prompt.

The contrasting responses vividly illustrate the impact of using a custom prompt when integrating the fashion trends 2023 dataset, showcasing discernible differences in the model's outputs, revealing new patterns and insights that the original OpenAI model, with its data cutoff in January 2022, cannot access.