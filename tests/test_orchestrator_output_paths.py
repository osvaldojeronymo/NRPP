from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

import orchestrator


def _write_file(path: Path, content: str = "ok"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _fake_a1(pdf_path, output_path, *args, **kwargs):
    _write_file(Path(output_path), "1 Item\nconteudo")


def _fake_a2(input_txt, output_csv):
    _write_file(Path(output_csv), "id;texto\n1;conteudo")


def _fake_a3(a2_csv, out_csv):
    _write_file(out_csv, "id;texto;termo;classe\n1;conteudo;termo;classe")


def _fake_a4(a3_csv, glossary_path, out_csv, audit_csv, isdf_path):
    _write_file(out_csv, "id;texto;termo;classe\n1;conteudo;termo;classe")
    _write_file(audit_csv, "termo\noutro")


def _fake_a5(a4_csv, out_xlsx):
    _write_file(out_xlsx, "xlsx")


class ProcessarPdfOutputPathTests(TestCase):
    def _processar_pdf_com_mocks(self, pdf_relative_path: str):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            origem_dir = root / Path(pdf_relative_path).parent
            origem_dir.mkdir(parents=True)

            pdf_path = root / pdf_relative_path
            pdf_path.write_text("pdf", encoding="utf-8")

            with patch.object(orchestrator, "a1", _fake_a1), patch.object(
                orchestrator, "a2", _fake_a2
            ), patch.object(orchestrator, "a3", _fake_a3), patch.object(
                orchestrator, "a4", _fake_a4
            ), patch.object(orchestrator, "a5", _fake_a5):
                result = orchestrator.processar_pdf((pdf_path, root))

            result_dir = root / "NRPP_RESULTADOS" / Path(pdf_relative_path).with_suffix("")
            expected_files = {
                result_dir / "EXTRACAO_TEXTO" / f"{pdf_path.stem}.txt",
                result_dir / "INTERMEDIARIOS" / "segmentos_texto.csv",
                result_dir / "INTERMEDIARIOS" / "evidencias_semanticas.csv",
                result_dir / "INTERMEDIARIOS" / "evidencias_normalizadas.csv",
                result_dir / "AUDITORIA_PIPELINE" / "termos_fora_do_glossario.csv",
                result_dir / "PRODUTO_FINAL" / "tabela_validacao_nrpp.xlsx",
                result_dir / "README.md",
            }

            for expected_file in expected_files:
                self.assertTrue(expected_file.exists(), f"Arquivo ausente: {expected_file}")

            source_side_effects = sorted(
                str(path.relative_to(root))
                for path in origem_dir.rglob("*")
                if path.is_file() and path != pdf_path
            )

            return result, source_side_effects

    def test_processar_pdf_writes_only_under_result_directory(self):
        result, source_side_effects = self._processar_pdf_com_mocks("entrada/teste.pdf")

        self.assertEqual(result["resultado"], "NRPP_RESULTADOS/entrada/teste")
        self.assertEqual(source_side_effects, [])

    def test_processar_pdf_preserves_relative_hierarchy_for_nested_pdf(self):
        result, source_side_effects = self._processar_pdf_com_mocks(
            "entrada/setor_a/subsetor_b/teste.pdf"
        )

        self.assertEqual(
            result["resultado"],
            "NRPP_RESULTADOS/entrada/setor_a/subsetor_b/teste",
        )
        self.assertEqual(source_side_effects, [])