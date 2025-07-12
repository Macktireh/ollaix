# Ollaix 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to the Ollaix API! This is the backend component of the Ollaix project, designed to serve as a versatile bridge between your applications and various Large Language Models (LLMs). 🤖

This API provides a unified interface to interact with different AI providers, including local models via [Ollama](https://ollama.com/) and powerful cloud models like Google's [Gemini](https://deepmind.google/technologies/gemini/). It is built with performance and ease of use in mind, using the modern [Litestar](https://litestar.dev/) Python framework.

The full Ollaix stack includes this backend, the [Ollaix UI](https://github.com/Macktireh/ollaix-ui) frontend, and a service for running Ollama models, all containerized for simple deployment.

---

## ✨ Features

- 🌐 **Unified API Gateway**: Single endpoint for multiple LLM providers.
- 🤝 **Multi-Provider Support**: Out-of-the-box integration for Ollama and Google Gemini.
- 🌊 **Streaming Support**: Real-time, non-blocking streaming for chat completions.
- 🔍 **Model Discovery**: An endpoint to dynamically list all available models from the configured providers.
- 🐳 **Containerized**: Fully containerized with Docker and Docker Compose for easy setup and deployment.
- ⚡ **Modern & Fast**: Built with Python and the high-performance Litestar web framework.
- 📈 **Scalable Design**: A clean, service-oriented architecture that is easy to extend with new AI providers.

---

## 🛠️ Tech Stack

The complete Ollaix project stack includes:

- 🐍 **Backend**: [Python](https://www.python.org/), [Litestar](https://litestar.dev/)
- 🧠 **LLM Integrations**: [Ollama](https://ollama.com/), [Google Gen AI SDK](https://github.com/googleapis/python-genai)
- 🐳 **Containerization**: [Docker](https://www.docker.com/)
- 📦 **Package Management**: [PDM](https://pdm-project.org/)
- ⚛️ **Frontend**: [React](https://react.dev/), [TypeScript](https://www.typescriptlang.org/), [Vite](https://vitejs.dev/), [Tailwind CSS](https://tailwindcss.com/), [DaisyUI](https://daisyui.com/)

---

## 🚀 Getting Started

To get the Ollaix API up and running on your local machine, follow these steps.

### ✅ Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose
- A [Google AI Studio API Key](https://aistudio.google.com/app/apikey) for Gemini integration.

### 💻 Installation

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/Macktireh/ollaix.git
    cd ollaix
    ```

2.  **Create an environment file:**
    Create a `.env` file in the root of the project by copying the example file:

    ```sh
    cp .env.example .env
    ```

3.  **Configure your environment:**
    Open the `.env` file and add your Google Gemini API key:

    ```
    # .env
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```

4.  **Launch the application:**
    Use Docker Compose to build and start all the services (API, Ollama, and UI):

    ```sh
    docker-compose up --build
    ```

    The services will be available at the following URLs:

    - **Ollaix API**: `http://localhost:8000`
    - **API Documentation (Scalar)**: `http://localhost:8000/`
    - **Ollaix UI**: `http://localhost:3000`

---

## 🌐 API Endpoints

Once the service is running, you can interact with the following main endpoints:

| Method | Path                   | Description                                         |
| :----- | :--------------------- | :-------------------------------------------------- |
| `GET`  | `/`                    | Displays the API documentation (Scalar).            |
| `GET`  | `/v1/models`           | Lists all available models from all providers.      |
| `POST` | `/v1/chat/completions` | Main endpoint to stream chat responses from an LLM. |

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

### How to Contribute

1.  **Fork the Project**
2.  **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3.  **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4.  **Push to the Branch** (`git push origin feature/AmazingFeature`)
5.  **Open a Pull Request**

Please ensure your pull request provides a clear description of the problem and solution. Include the relevant issue number if applicable.

---

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

---

Made with ❤️ by [Macktireh](https://github.com/Macktireh)
