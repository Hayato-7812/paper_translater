from googletrans import Translator
import os
import sys
import argparse
import PDF2txt

class PDF_Translator():
    def __init__(self, argv: list):
        if not argv:
            return

        # コマンドライン引数の解析
        parser = argparse.ArgumentParser()
        parser.add_argument('pdf_path', type=str, help="入力ファイル名")
        parser.add_argument("-s", '--src_lang', type=str, metavar="n", default="en", help="翻訳ファイルの言語")
        parser.add_argument("-d", '--dest_lang', type=str, metavar="n", default="ja", help="翻訳先の言語")
        args = parser.parse_args(argv)

        self.pdf_path = args.pdf_path
        self.txt_path = f"{os.path.splitext(os.path.basename(self.pdf_path))[0]}.txt"
        self.output_path = f"translated_{os.path.splitext(os.path.basename(self.pdf_path))[0]}.txt"
        self.src_lang = args.src_lang
        self.dest_lang = args.dest_lang

    def get_text(self):
        cnv = PDF2txt.ConvertPDF2text(self.pdf_path, self.txt_path)
        cnv.convert_pdf_to_text()
        if not os.path.exists(self.txt_path):
            print(f"Error: File {self.txt_path} does not exist.")
            return ""
        else:
            with open(self.txt_path, 'r', encoding='utf-8') as f:
                data = f.read()
            return data

    def translate(self):
        txt = self.get_text()
        translator = Translator()
        translated_lines = []

        for line in txt.split('\n'):
            try:
                translated_line = translator.translate(line, src=self.src_lang, dest=self.dest_lang).text
                print(translated_line)
                translated_lines.append(translated_line)
            except Exception as e:
                print(f"Translation error: {e}")

        with open(self.output_path, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(translated_lines))

if __name__ == "__main__":
    translator = PDF_Translator(sys.argv[1:])
    translator.translate()
