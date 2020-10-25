import glob
import json
import os
import re

NAMING_PATTERN = r"\d{4}-\d{2}-\d{2}-\S+\.ipynb"

current_dir = os.getcwd()
notebooks = glob.glob(f"{current_dir}/analysis/*.ipynb")
scripts = glob.glob(f"{current_dir}/analysis/*.py")
htmls = glob.glob(f"{current_dir}/analysis/*.html")

has_missing_files = len(notebooks) != len(scripts) or len(notebooks) != len(htmls)
has_clean_outputs = True
naming = []

for notebook in notebooks:
    # checa padrão de nomes
    naming.extend([True if re.search(NAMING_PATTERN, notebook) else False])

    # checa se os outputs estão limpos
    notebook = json.load(open(notebook))
    for cell in notebook["cells"]:
        if cell.get("outputs", None):
            has_clean_outputs = False

has_proper_naming = all(naming)

missing_files = " " if has_missing_files else "x"
proper_naming = "x" if has_proper_naming else " "
clean_outputs = "x" if has_clean_outputs else " "

checklist = f"""
```
Obrigada pela sua contribuição! 🎉

Esse checklist vai te ajudar a saber quando o seu notebook está pronto:

- [{clean_outputs}] Os _outputs_ dos _notebooks_ estão limpos
- [{missing_files}] Os arquivos `.py` e `.html` foram criados
- [{proper_naming}] Os nomes dos _notebooks_ estão de acordo com o padrão

Se tiver dúvidas, veja o nosso [guia de contribuição](https://github.com/DadosAbertosDeFeira/analises/blob/main/CONTRIBUTING.md).
Certifique-se que os testes estão passando e que o seu código
está de acordo com as regras de qualidade.
```
"""  # noqa

print(checklist)
