import os
import django
from django.utils import timezone
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

from article.models import ArticleV2, Category, Author, Tag


def create_sample_data():
    # Create categories
    categories = [
        Category.objects.create(name="Web Development"),
        Category.objects.create(name="Data Science"),
        Category.objects.create(name="Machine Learning"),
        Category.objects.create(name="Backend Development"),
    ]

    # Create authors
    authors = [
        Author.objects.create(name="John Doe", age=35),
        Author.objects.create(name="Jane Smith", age=28),
        Author.objects.create(name="Bob Johnson", age=42),
    ]

    # Create tags
    tags = [
        Tag.objects.create(name="Python"),
        Tag.objects.create(name="JavaScript"),
        Tag.objects.create(name="Django"),
        Tag.objects.create(name="Elasticsearch"),
        Tag.objects.create(name="RAG"),
        Tag.objects.create(name="AI"),
        Tag.objects.create(name="Web"),
        Tag.objects.create(name="Database"),
    ]

    # Create articles
    articles = [
        {
            "title": "Introduction to Django: Building Web Applications with Python",
            "category": categories[0],
            "author": authors[0],
            "tags": [tags[0], tags[2], tags[6]],
            "content": {
                "content": [
                    {"text": "Introduction to Django", "type": "h1"},
                    {
                        "text": "Django is a high-level Python web framework that enables rapid development of secure and maintainable websites.",
                        "type": "p",
                    },
                    {"text": "Key Features of Django", "type": "h2"},
                    {
                        "type": "ul",
                        "items": [
                            "ORM (Object-Relational Mapping)",
                            "URL routing",
                            "Template engine",
                            "Forms framework",
                        ],
                    },
                ]
            },
        },
        {
            "title": "JavaScript Fundamentals for Modern Web Development",
            "category": categories[0],
            "author": authors[1],
            "tags": [tags[1], tags[6]],
            "content": {
                "content": [
                    {"text": "JavaScript Fundamentals", "type": "h1"},
                    {
                        "text": "JavaScript is a versatile programming language that powers the interactive elements of modern websites.",
                        "type": "p",
                    },
                    {"text": "Core Concepts", "type": "h2"},
                    {
                        "type": "ul",
                        "items": [
                            "Variables and data types",
                            "Functions and scope",
                            "DOM manipulation",
                            "Asynchronous programming",
                        ],
                    },
                ]
            },
        },
        {
            "title": "Elasticsearch: Powering Advanced Search Functionality",
            "category": categories[3],
            "author": authors[2],
            "tags": [tags[3], tags[7]],
            "content": {
                "content": [
                    {"text": "Elasticsearch Fundamentals", "type": "h1"},
                    {
                        "text": "Elasticsearch is a distributed, RESTful search and analytics engine capable of addressing a growing number of use cases.",
                        "type": "p",
                    },
                    {"text": "Key Features", "type": "h2"},
                    {
                        "type": "ul",
                        "items": [
                            "Full-text search",
                            "Distributed architecture",
                            "Real-time analytics",
                            "RESTful API",
                        ],
                    },
                ]
            },
        },
        {
            "title": "Retrieval-Augmented Generation (RAG): Enhancing AI with External Knowledge",
            "category": categories[2],
            "author": authors[0],
            "tags": [tags[4], tags[5]],
            "content": {
                "content": [
                    {"text": "Understanding RAG", "type": "h1"},
                    {
                        "text": "Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with text generation to produce more accurate and contextually relevant outputs.",
                        "type": "p",
                    },
                    {"text": "Components of RAG", "type": "h2"},
                    {
                        "type": "ul",
                        "items": [
                            "Information retrieval system",
                            "Large language model",
                            "Integration mechanism",
                        ],
                    },
                ]
            },
        },
        {
            "title": "Python for Data Science: Essential Libraries and Techniques",
            "category": categories[1],
            "author": authors[1],
            "tags": [tags[0], tags[1], tags[5]],
            "content": {
                "content": [
                    {"text": "Python in Data Science", "type": "h1"},
                    {
                        "text": "Python has become the de facto language for data science due to its rich ecosystem of libraries and ease of use.",
                        "type": "p",
                    },
                    {"text": "Essential Libraries", "type": "h2"},
                    {
                        "type": "ul",
                        "items": ["NumPy", "Pandas", "Matplotlib", "Scikit-learn"],
                    },
                ]
            },
        },
        {
            "title": "Building RESTful APIs with Django Rest Framework",
            "category": categories[3],
            "author": authors[2],
            "tags": [tags[0], tags[2], tags[6]],
            "content": {
                "content": [
                    {"text": "Django Rest Framework", "type": "h1"},
                    {
                        "text": "Django Rest Framework (DRF) is a powerful and flexible toolkit for building Web APIs in Django applications.",
                        "type": "p",
                    },
                    {"text": "Key Features of DRF", "type": "h2"},
                    {
                        "type": "ul",
                        "items": [
                            "Serialization",
                            "Authentication",
                            "Viewsets and routers",
                            "Pagination",
                        ],
                    },
                ]
            },
        },
        {
            "title": "Machine Learning Basics: Algorithms and Applications",
            "category": categories[2],
            "author": authors[0],
            "tags": [tags[0], tags[5]],
            "content": {
                "content": [
                    {"text": "Introduction to Machine Learning", "type": "h1"},
                    {
                        "text": "Machine Learning is a subset of AI that focuses on the development of algorithms that can learn from and make predictions or decisions based on data.",
                        "type": "p",
                    },
                    {"text": "Common ML Algorithms", "type": "h2"},
                    {
                        "type": "ul",
                        "items": [
                            "Linear Regression",
                            "Decision Trees",
                            "Support Vector Machines",
                            "Neural Networks",
                        ],
                    },
                ]
            },
        },
        {
            "title": "Integrating Elasticsearch with Django for Advanced Search",
            "category": categories[3],
            "author": authors[1],
            "tags": [tags[0], tags[2], tags[3]],
            "content": {
                "content": [
                    {"text": "Elasticsearch and Django Integration", "type": "h1"},
                    {
                        "text": "Combining the power of Django and Elasticsearch can significantly enhance the search capabilities of your web application.",
                        "type": "p",
                    },
                    {"text": "Integration Steps", "type": "h2"},
                    {
                        "type": "ol",
                        "items": [
                            "Install necessary packages",
                            "Configure Elasticsearch connection",
                            "Index Django models",
                            "Implement search views",
                        ],
                    },
                ]
            },
        },
        {
            "title": "Modern JavaScript Frameworks: React vs Vue vs Angular",
            "category": categories[0],
            "author": authors[2],
            "tags": [tags[1], tags[6]],
            "content": {
                "content": [
                    {"text": "Comparing Modern JS Frameworks", "type": "h1"},
                    {
                        "text": "React, Vue, and Angular are the top three JavaScript frameworks for building modern web applications. Each has its strengths and use cases.",
                        "type": "p",
                    },
                    {"text": "Comparison Criteria", "type": "h2"},
                    {
                        "type": "ul",
                        "items": [
                            "Learning curve",
                            "Performance",
                            "Community support",
                            "Ecosystem",
                        ],
                    },
                ]
            },
        },
        {
            "title": "Implementing RAG Systems: Challenges and Best Practices",
            "category": categories[2],
            "author": authors[0],
            "tags": [tags[4], tags[5], tags[0]],
            "content": {
                "content": [
                    {"text": "RAG Implementation Guide", "type": "h1"},
                    {
                        "text": "Implementing a Retrieval-Augmented Generation (RAG) system involves overcoming several challenges and following best practices to ensure optimal performance.",
                        "type": "p",
                    },
                    {"text": "Key Challenges", "type": "h2"},
                    {
                        "type": "ul",
                        "items": [
                            "Efficient information retrieval",
                            "Seamless integration with LLMs",
                            "Maintaining up-to-date knowledge",
                            "Handling context and relevance",
                        ],
                    },
                ]
            },
        },
    ]

    for article_data in articles:
        article = ArticleV2.objects.create(
            title=article_data["title"],
            category=article_data["category"],
            author=article_data["author"],
            content=article_data["content"],
        )
        article.tags.set(article_data["tags"])

        # Download a placeholder image and set it as the cover
        img_url = f"https://picsum.photos/800/600"
        response = requests.get(img_url)
        if response.status_code == 200:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()
            article.cover.save(
                f"cover_{article.article_id}.jpg", File(img_temp), save=True
            )

        print(f"Created article: {article.title}")


if __name__ == "__main__":
    create_sample_data()
    print("Sample data creation completed.")
