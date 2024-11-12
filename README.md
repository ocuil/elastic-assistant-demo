# 🏦 ElasticBank Assistant | Asistente ElasticBank

[English](#english) | [Español](#español)

---
## 📋 Table of Contents | Tabla de Contenidos
- [🏦 ElasticBank Assistant | Asistente ElasticBank](#-elasticbank-assistant--asistente-elasticbank)
  - [📋 Table of Contents | Tabla de Contenidos](#-table-of-contents--tabla-de-contenidos)
- [English](#english)
  - [🎯 Description](#-description)
  - [✨ Features](#-features)
  - [🛠️ Requirements](#️-requirements)
  - [📥 Installation](#-installation)
  - [🚀 Usage](#-usage)
  - [📁 Project Structure](#-project-structure)
  - [⚙️ Configuration](#️-configuration)
  - [👥 Contributing](#-contributing)
- [Español](#español)
  - [🎯 Descripción](#-descripción)
  - [✨ Características](#-características)
  - [🛠️ Requisitos](#️-requisitos)
  - [📥 Instalación](#-instalación)
  - [🚀 Uso](#-uso)
  - [📁 Estructura del Proyecto](#-estructura-del-proyecto)
  - [⚙️ Configuración](#️-configuración)
  - [👥 Contribuir](#-contribuir)
  - [📝 License | Licencia](#-license--licencia)
  - [🙋‍♂️ Contact | Contacto](#️-contact--contacto)

---
# English

## 🎯 Description
ElasticBank Assistant is an intelligent chatbot powered by Azure OpenAI and Elasticsearch. It provides banking information through FAQs and helps users manage their transactions and account information.

## ✨ Features
- 🤖 AI-powered conversational interface
- 💬 FAQ search with semantic understanding
- 💳 Transaction and balance queries
- 📊 Spending analysis and categorization
- 🔄 Recurring transaction identification
- 👥 Multi-user support
- 🔐 Secure authentication system
- 📱 Responsive web interface

## 🛠️ Requirements
- Python 3.8+
- Azure OpenAI API access
- Elasticsearch cluster
- Required Python packages (see requirements.txt)

## 📥 Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/elasticbank-assistant.git
cd elasticbank-assistant
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file with required credentials
```bash
cp .env.example .env
# Edit .env with your credentials
```

## 🚀 Usage
Run the Streamlit application:
```bash
streamlit run elasticbank/main.py
```

## 📁 Project Structure
```
elasticbank/
├── config/          # Configuration settings
├── core/            # Core functionality
├── services/        # External services integration
├── tools/           # LangChain tools
├── ui/              # User interface components
└── utils/           # Utility functions
```

## ⚙️ Configuration
Set up your environment variables in `.env`:
```env
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_key
API_VERSION=your_version
DEPLOYMENT_ID=your_deployment
ES_API_KEY=your_elasticsearch_key
```

## 👥 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---
# Español

## 🎯 Descripción
El Asistente ElasticBank es un chatbot inteligente impulsado por Azure OpenAI y Elasticsearch. Proporciona información bancaria a través de FAQs y ayuda a los usuarios a gestionar sus transacciones e información de cuenta.

## ✨ Características
- 🤖 Interfaz conversacional con IA
- 💬 Búsqueda de FAQs con comprensión semántica
- 💳 Consultas de transacciones y saldos
- 📊 Análisis y categorización de gastos
- 🔄 Identificación de transacciones recurrentes
- 👥 Soporte multi-usuario
- 🔐 Sistema de autenticación seguro
- 📱 Interfaz web responsive

## 🛠️ Requisitos
- Python 3.8+
- Acceso a Azure OpenAI API
- Cluster de Elasticsearch
- Paquetes Python requeridos (ver requirements.txt)

## 📥 Instalación
1. Clonar el repositorio
```bash
git clone https://github.com/yourusername/elasticbank-assistant.git
cd elasticbank-assistant
```

2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Crear archivo `.env` con las credenciales requeridas
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

## 🚀 Uso
Ejecutar la aplicación Streamlit:
```bash
streamlit run elasticbank/main.py
```

## 📁 Estructura del Proyecto
```
elasticbank/
├── config/          # Configuraciones
├── core/            # Funcionalidad principal
├── services/        # Integración con servicios externos
├── tools/           # Herramientas de LangChain
├── ui/              # Componentes de interfaz de usuario
└── utils/           # Funciones de utilidad
```

## ⚙️ Configuración
Configura tus variables de entorno en `.env`:
```env
AZURE_OPENAI_ENDPOINT=tu_endpoint
AZURE_OPENAI_API_KEY=tu_key
API_VERSION=tu_version
DEPLOYMENT_ID=tu_deployment
ES_API_KEY=tu_key_elasticsearch
```

## 👥 Contribuir
¡Las contribuciones son bienvenidas! No dudes en enviar un Pull Request.

---

## 📝 License | Licencia
This project is licensed under the Apache License Version 2.0 - see the [LICENSE](LICENSE) file for details.

Este proyecto está licenciado bajo la Licencia Apache License Version 2.0 - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙋‍♂️ Contact | Contacto
- 🌐 Website: https://[alejandrosl.com](https://www.alejandrosl.com/)
- 💼 LinkedIn: [AlejandroSL](https://www.linkedin.com/in/alejandrosl/)

---

⭐️ If this project helped you, please consider giving it a star!

⭐️ Si este proyecto te ayudó, ¡considera darle una estrella!