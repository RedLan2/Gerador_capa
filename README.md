# Gerador de Capa de Recebimento DANFE

## Instalação

Clone o projeto:
```bash
git clone <repo-url>
cd gerador-danfe
```

Instale as dependências:

Com uv:
```bash
uv add streamlit pdfplumber reportlab python-docx
```

Ou com pip:
```bash
pip install streamlit pdfplumber reportlab python-docx
```

## Executar

```bash
streamlit run app.py --server.port 5000
```

Acesse: `http://localhost:5000`