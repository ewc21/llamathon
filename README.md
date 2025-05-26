# llamathon
GemiNutrition is an AI-powered nutrition assistant designed to provide intelligent meal breakdowns and personalized food recommendations. The project was originally developed for the 8VC x Meta x HackDuke CodeFest, utilizing Llama 3.3 to perform retrieval-augmented generation (RAG) on a structured dataset of meals and nutritional information.

To enhance performance and reduce latency, the underlying model has since been updated to Gemini 2.0 Flash, which offers significantly improved response times while maintaining high accuracy.

## Features

- Natural language interface for querying meals, ingredients, and nutritional content
- Retrieval-augmented generation pipeline over a curated food dataset
- Structured output designed for easy integration into fitness or meal-tracking platforms
- Frontend interface optimized for usability and clarity

## Technology Stack

- Frontend: React
- Backend: FastAPI with integrated RAG pipeline
- AI Models: Gemini 2.0 Flash
- Database: Prisma with PostgreSQL
