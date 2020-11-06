from scripts.ops.check_notebooks import check, read_files


def test_check_notebooks():
    notebooks, scripts, htmls = read_files()
    missing_py_files, missing_htmls, has_proper_naming, has_clean_outputs = check(
        notebooks, scripts, htmls
    )

    assert missing_py_files is False, "Você precisa gerar arquivos .py em `analysis`"
    assert missing_htmls is False, "Você precisa gerar arquivos html em `docs`"
    assert has_proper_naming is True, "Verifique o padrão dos nomes dos notebooks"
    assert has_clean_outputs is True, "Os outputs não estão limpos"
