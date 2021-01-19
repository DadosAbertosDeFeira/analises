from scripts.ops.check_notebooks import check, read_files


def test_check_notebooks():
    notebooks, scripts, htmls = read_files()
    missing_py_files, missing_htmls, has_proper_naming, has_clean_outputs = check(
        notebooks, scripts, htmls
    )
    nb_vs_py = f"({len(notebooks)} vs {len(scripts)})"
    missing_py_message = f"Você precisa gerar arquivos .py em `analysis` {nb_vs_py}"
    nb_vs_html = f"({len(notebooks)} vs {len(htmls)})"
    missing_htmls_message = f"Você precisa gerar arquivos html em `docs` {nb_vs_html}"

    assert missing_py_files is False, missing_py_message
    assert missing_htmls is False, missing_htmls_message
    assert has_proper_naming is True, "Verifique o padrão dos nomes dos notebooks"
    assert has_clean_outputs is True, "Os outputs não estão limpos"
