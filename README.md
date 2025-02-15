# LLM-Trivia-Game

## Overview
This app takes a user defined topic and creates quiz questions based on that topic to be used as a learning mechanism. The app uses ChatGPT's API to generate quiz questions and answers.

## Setup and Installation

1. **Install Flask**
    ```bash
    pip install Flask
    pip install asgiref
    ```
2. **Run the Flask app for testing**:
    ```bash
    flask --app main run
    ```

3. **Set OpenAI API Key**
    Windows:
    ```bash
    $env:OPENAI_API_KEY="your_openai_api_key"
    ```
    Mac:
    ```bash
    export OPENAI_API_KEY=your_key
    ```

4. **Launch Frontend from trivia-frontend**
    ```bash
    cd trivia-frontend
    npm start
    ```

## Technologies
- Frontend -> Vite -> ShadCN for simplified development
- ShadCN - used for simple component styling
Add components using commands such as:
```bash
npx shadcn add button
```
Install with: https://ui.shadcn.com/docs/installation/manual
