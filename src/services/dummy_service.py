import json
from asyncio import sleep
from collections.abc import AsyncGenerator
from random import choice, randint, random
from typing import Any, override

from schemas.chat_schemas import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionStreamChunk,
    ModelInfo,
)
from services.ai_service_interface import AIServiceInterface


class DummyService(AIServiceInterface):
    """
    Dummy AI service to generate random responses with streaming support.
    Used for testing or development purposes.
    """

    available_models = ["dummy-model:1.0"]
    provider_name = "dummy"

    @override
    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        if request.model not in self.available_models:
            raise ValueError(f"Modèle '{request.model}' non disponible pour DummyService")

        # Simulate a delay for the non-streamed response
        await sleep(2)

        # Generate random content
        content = self._generate_dummy_content(word_count=100)

        return ChatCompletionResponse(
            model=request.model,
            choices=[
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": content,
                    },
                    "finish_reason": "stop",
                }
            ],
            usage={
                "prompt_tokens": len(request.messages),
                "completion_tokens": len(content.split()),
                "total_tokens": len(request.messages) + len(content.split()),
            },
        )

    @override
    async def chat_completion_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncGenerator[str, Any]:
        if request.model not in self.available_models:
            raise ValueError(f"Modèle '{request.model}' non disponible pour DummyService")

        # The get_dummy_chat_stream logic is already a Generator
        # It needs to be converted into an AsyncGenerator
        async for chunk_content in self._get_dummy_chat_stream():
            stream_chunk = ChatCompletionStreamChunk(
                model=request.model,
                choices=[
                    {
                        "index": 0,
                        "delta": {
                            "role": "assistant",
                            "content": chunk_content,
                        },
                        "finish_reason": None,
                    }
                ],
            )
            yield f"data: {json.dumps(stream_chunk.__dict__, default=str)}\n\n"

        # Send stream end message
        final_chunk = ChatCompletionStreamChunk(
            model=request.model,
            choices=[
                {
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop",
                }
            ],
        )
        yield f"data: {json.dumps(final_chunk.__dict__, default=str)}\n\n"
        yield "data: [DONE]\n\n"

    @override
    def get_model_info(self) -> list[ModelInfo]:
        return [
            ModelInfo(
                id="dummy-model:1.0",
                name="Dummy Model",
                description="A placeholder model for testing and development. Does not perform real inference.",  # noqa: E501
                provider="dummy",
                context_length=2048,
            ),
        ]

    def _generate_dummy_content(self, word_count: int = 100) -> str:
        """Generates random text content."""
        WORDS = [
            "lorem",
            "ipsum",
            "dolor",
            "sit",
            "amet",
            "consectetur",
            "adipiscing",
            "elit",
            "sed",
            "do",
            "eiusmod",
            "tempor",
            "incididunt",
            "ut",
            "labore",
            "et",
            "dolore",
            "magna",
            "aliqua",
            "enim",
            "ad",
            "minim",
            "veniam",
            "quis",
            "nostrud",
            "exercitation",
            "ullamco",
            "laboris",
            "nisi",
            "aliquip",
            "ex",
            "ea",
            "commodo",
            "consequat",
            "duis",
            "aute",
            "irure",
            "in",
            "reprehenderit",
            "voluptate",
            "velit",
            "esse",
            "cillum",
            "fugiat",
            "nulla",
            "pariatur",
            "excepteur",
            "sint",
            "occaecat",
            "cupidatat",
            "non",
            "proident",
            "sunt",
            "culpa",
            "qui",
            "officia",
            "deserunt",
            "mollit",
            "anim",
            "id",
            "est",
            "laborum",
            "solution",
            "problème",
            "méthode",
            "exemple",
            "important",
            "noter",
            "voici",
            "comment",
            "fonction",
            "variable",
            "classe",
            "objet",
            "données",
            "résultat",
            "algorithme",
            "code",
        ]
        return " ".join(choice(WORDS).lower() for _ in range(word_count)) + "."

    async def _get_dummy_chat_stream(self, **kwargs) -> AsyncGenerator[str]:
        await sleep(1.5)
        WORDS = [
            "lorem",
            "ipsum",
            "dolor",
            "sit",
            "amet",
            "consectetur",
            "adipiscing",
            "elit",
            "sed",
            "do",
            "eiusmod",
            "tempor",
            "incididunt",
            "ut",
            "labore",
            "et",
            "dolore",
            "magna",
            "aliqua",
            "enim",
            "ad",
            "minim",
            "veniam",
            "quis",
            "nostrud",
            "exercitation",
            "ullamco",
            "laboris",
            "nisi",
            "aliquip",
            "ex",
            "ea",
            "commodo",
            "consequat",
            "duis",
            "aute",
            "irure",
            "in",
            "reprehenderit",
            "voluptate",
            "velit",
            "esse",
            "cillum",
            "fugiat",
            "nulla",
            "pariatur",
            "excepteur",
            "sint",
            "occaecat",
            "cupidatat",
            "non",
            "proident",
            "sunt",
            "culpa",
            "qui",
            "officia",
            "deserunt",
            "mollit",
            "anim",
            "id",
            "est",
            "laborum",
            "solution",
            "problème",
            "méthode",
            "exemple",
            "important",
            "noter",
            "voici",
            "comment",
            "fonction",
            "variable",
            "classe",
            "objet",
            "données",
            "résultat",
            "algorithme",
            "code",
        ]
        TECH_WORDS = [
            "Python",
            "JavaScript",
            "React",
            "Django",
            "FastAPI",
            "API",
            "REST",
            "JSON",
            "database",
            "SQL",
            "NoSQL",
            "MongoDB",
            "PostgreSQL",
            "Redis",
            "Docker",
            "Kubernetes",
            "microservices",
            "authentication",
            "authorization",
            "JWT",
            "HTTP",
            "HTTPS",
            "SSL",
            "TLS",
            "encryption",
            "hash",
            "algorithm",
            "framework",
        ]
        CODE_EXAMPLES = [
            "```python\ndef example_function():\n    return 'Hello World'\n```",
            "```js\nconst data = await fetch('/api/endpoint');\nconst result = await data.json();\n```",  # noqa: E501
            "```sql\nSELECT * FROM users WHERE active = true;\n```",
            "```bash\nnpm install package-name\npip install requirements.txt\n```",
            "```\nnpm install package-name\npip install requirements.txt\n```",
            '```json\n{\n  "status": "success",\n  "data": []\n}\n```',
            "![1](https://github.com/user-attachments/assets/382225ab-abdc-49ad-8497-d3d5b5c7043a)",  # noqa: E501
            "![2](https://github.com/user-attachments/assets/d9e53e85-0f06-4c80-826e-8a69d26bcc7a)",  # noqa: E501
            "![3](https://github.com/user-attachments/assets/48dabfe0-18e3-4d04-b526-9667772aefd1)",  # noqa: E501
        ]
        HEADINGS = [
            "## Solution proposée",
            "## Explication détaillée",
            "## Exemple pratique",
            "## Points importants",
            "## Configuration requise",
            "## Étapes à suivre",
            "### Méthode 1",
            "### Méthode 2",
            "### Alternative",
            "### Remarque importante",
        ]
        MARKDOWN_ELEMENTS = [
            "**important**",
            "*essentiel*",
            "`variable`",
            "`fonction()`",
            "`class MyClass`",
            "[documentation](https://example.com)",
            "> Cette approche est recommandée",
            "> **Note:** Il faut faire attention à",
        ]
        LIST_ITEMS = [
            "- Premier point à considérer",
            "- Deuxième élément important",
            "- Troisième aspect essentiel",
            "1. Première étape",
            "2. Deuxième étape",
            "3. Troisième étape",
        ]

        default_word_count = choice(range(150, 200))
        default_delay = 0.02

        try:
            word_count = int(kwargs.get("word_count", default_word_count))
            delay = float(kwargs.get("delay", default_delay))
        except (ValueError, TypeError):
            word_count = default_word_count
            delay = default_delay

        # Content structure
        content_blocks = []
        current_block = []
        words_generated = 0

        THINKING_WORDS = [
            "analyser",
            "considérer",
            "évaluer",
            "examiner",
            "réfléchir",
            "comprendre",
            "déterminer",
            "identifier",
            "explorer",
            "investigation",
            "approche",
            "méthode",
            "solution",
            "problème",
            "question",
            "aspect",
            "élément",
            "facteur",
            "paramètre",
            "contexte",
            "situation",
            "cas",
            "scénario",
            "possibilité",
            "option",
            "alternative",
            "conséquence",
            "résultat",
            "impact",
            "effet",
            "influence",
            "importance",
            "pertinence",
        ]
        thinking_block = ["<think> "]
        for paragraph in range(3):
            # Generate 3 lines per paragraph
            paragraph_lines = []
            for _line in range(3):
                line_words = []
                for _ in range(randint(6, 10)):
                    word = choice(THINKING_WORDS) if random() < 0.3 else choice(WORDS)
                    if len(line_words) == 0:
                        word = word.capitalize()

                    line_words.append(word)

                # Construct line with comma
                line_text = " ".join(line_words) + ","
                paragraph_lines.append(line_text)

            # Join the 3 lines of the paragraph with spaces
            paragraph_text = " ".join(paragraph_lines)

            # Replace the last comma with a period and add space
            if paragraph < 2:
                paragraph_text = paragraph_text[:-1] + ". \n\n"
            else:
                paragraph_text = paragraph_text[:-1] + "."

            thinking_block.append(paragraph_text)

        thinking_block.append(" </think>\n\n")
        content_blocks.append(thinking_block)
        words_generated += 60

        while words_generated < word_count:
            # Decide what type of content to generate (40% chance for code blocks)
            content_type = choice(
                [
                    "paragraph",
                    "text",
                    "heading",
                    "code",
                    "code",
                    "code",
                    "code",
                    "code",
                    "markdown",
                    "markdown",
                    "markdown",
                    "list",
                    "linebreak",
                    "linebreak",
                ]
            )

            if content_type == "paragraph" and random() < 0.6:
                # Générer un paragraphe de 70 mots
                if current_block:
                    content_blocks.append(current_block)
                    current_block = []

                paragraph_block = []
                paragraph_words = 0
                target_words = 70

                while paragraph_words < target_words and words_generated < word_count:
                    word = choice(TECH_WORDS) if random() < 0.1 else choice(WORDS)

                    # Capitalize on the first word of the paragraph
                    if paragraph_words == 0:
                        word = word.capitalize()

                    # Add internal punctuation to paragraphs
                    if (
                        paragraph_words > 0
                        and paragraph_words < target_words - 5
                        and random() < 0.12
                    ):
                        punctuation = choice([", ", ". "])
                        if punctuation == ". ":
                            paragraph_block.append(punctuation)
                            word = word.capitalize()
                        else:
                            paragraph_block.append(punctuation)

                    paragraph_block.append(word + " ")
                    paragraph_words += 1
                    words_generated += 1

                # End the paragraph with a period
                if paragraph_block and not paragraph_block[-1].rstrip().endswith((".", "!", "?")):
                    paragraph_block[-1] = paragraph_block[-1].rstrip() + "."

                # Double saut de ligne après le paragraphe
                paragraph_block.append("\n\n")
                content_blocks.append(paragraph_block)

            elif content_type == "heading" and random() < 0.3:
                if current_block:
                    content_blocks.append(current_block)
                    current_block = []
                heading = choice(HEADINGS)
                content_blocks.append(["\n\n", heading, "\n\n"])
                words_generated += len(heading.split())

            elif content_type == "code" and random() < 0.2:
                if current_block:
                    content_blocks.append(current_block)
                    current_block = []
                code = choice(CODE_EXAMPLES)
                content_blocks.append(["\n\n", code, "\n\n"])
                # Approximation for code
                words_generated += 10

            elif content_type == "list" and random() < 0.25:
                if current_block and len(current_block) > 5:
                    content_blocks.append(current_block)
                    current_block = []
                # Generate a list of 2-4 items
                list_size = randint(2, 4)
                list_block = ["\n\n"]
                for _ in range(list_size):
                    item = choice(LIST_ITEMS)
                    list_block.extend([item, "\n"])
                    words_generated += len(item.split())
                list_block.append("\n")
                content_blocks.append(list_block)

            elif content_type == "linebreak" and random() < 0.15:
                current_block.append("\n\n")

            elif content_type == "markdown" and random() < 0.2:
                element = choice(MARKDOWN_ELEMENTS)
                current_block.append(element + " ")
                words_generated += len(element.split())

            else:
                word = choice(TECH_WORDS) if random() < 0.1 else choice(WORDS)

                # Capitalize on the first word of the block
                if not current_block or (
                    current_block and current_block[-1].endswith((".", "!", "?", "\n"))
                ):
                    word = word.capitalize()

                # Add punctuation
                if words_generated > 0 and random() < 0.15:
                    punctuation = choice([", ", ". ", "! ", "? "])
                    if punctuation in [". ", "! ", "? "]:
                        current_block.append(punctuation)
                        word = word.capitalize()
                    else:
                        current_block.append(punctuation)

                current_block.append(word + " ")
                words_generated += 1

                # Limit the size of text blocks
                if len(current_block) > 30:
                    content_blocks.append(current_block)
                    current_block = []

        # Add last block
        if current_block:
            if current_block and not current_block[-1].rstrip().endswith((".", "!", "?")):
                current_block[-1] = current_block[-1].rstrip() + "."
            content_blocks.append(current_block)

        # Generate stream
        for block in content_blocks:
            for chunk in block:
                # Simulate character-by-character streaming for certain elements
                if chunk.startswith(("```", "#", "-", ">", "1.", "2.", "3.", "4.", "5.")):
                    yield chunk
                    # Longer pause for structural elements
                    await sleep(delay * 2)
                else:
                    # Stream word by word or character by character
                    if len(chunk) > 50:
                        for i in range(0, len(chunk), 10):
                            yield chunk[i : i + 10]
                            await sleep(delay)
                    else:
                        yield chunk
                        await sleep(delay)
