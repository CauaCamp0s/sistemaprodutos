from PyQt5 import uic, QtWidgets
import mysql.connector
import csv
import time
from reportlab.pdfgen import canvas


class TerminalColors:
    # Estilos de texto
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Cores do texto
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    WHITE = "\033[37m"


# Conectar ao banco de dados
database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Substitua pela sua senha real
    database="cad_produto",
)


def gerar_pdf():
    print(TerminalColors.BLACK + "GERANDO PDF..." + TerminalColors.RESET)
    time.sleep(3)

    cursor = database.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    y = 0
    pdf = canvas.Canvas("cadastro_produto.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos cadastrados: ")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "CODIGO")
    pdf.drawString(210, 750, "PRODUTO")
    pdf.drawString(310, 750, "PREÇO")
    pdf.drawString(410, 750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print(TerminalColors.RED + "PFD FOI GERADO COM SUCESSO!!!" + TerminalColors.RESET)


def gerar_txt():
    print(TerminalColors.BLACK + "GERANDO TXT..." + TerminalColors.RESET)
    time.sleep(3)

    cursor = database.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    with open("produtos.txt", "w") as arquivo_txt:
        arquivo_txt.write("Produtos cadastrados:\n\n")
        arquivo_txt.write("ID\tCÓDIGO\t\tPRODUTO\t\tPREÇO\t\tCATEGORIA\n")
        for dados in dados_lidos:
            linha = (
                f"{dados[0]}\t{dados[1]}\t\t{dados[2]}\t\t{dados[3]}\t\t{dados[4]}\n"
            )
            arquivo_txt.write(linha)

    print(TerminalColors.WHITE + "TXT FOI GERADO COM SUCESSO!!!" + TerminalColors.RESET)


def gerar_csv():
    print(TerminalColors.BLACK + "GERANDO CSV..." + TerminalColors.RESET)
    time.sleep(3)

    cursor = database.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    with open("produtos.csv", "w", newline="") as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["ID", "CÓDIGO", "PRODUTO", "PREÇO", "CATEGORIA"])
        writer.writerows(dados_lidos)

    print(TerminalColors.GREEN + "CSV FOI GERADO COM SUCESSO!!!" + TerminalColors.RESET)


def primary_function():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()

    categoria = None

    if formulario.radioButton.isChecked():
        print("Categoria Selecionada: Informática")
        categoria = "Informática"

    elif formulario.radioButton_2.isChecked():
        print("Categoria Selecionada: Alimentos")
        categoria = "Alimentos"

    elif formulario.radioButton_3.isChecked():
        print("Categoria Selecionada: Eletrônicos")
        categoria = "Eletrônicos"

    print("Código do Produto:", linha1)
    print("Preço do produto:", linha2)
    print("Descrição do produto:", linha3)

    cursor = database.cursor()
    comando_SQL = "INSERT INTO produtos (codigo, preco, descricao, categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1), str(linha2), str(linha3), categoria)
    cursor.execute(comando_SQL, dados)
    database.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")


def call_second_screen():
    second_screen.show()
    cursor = database.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    # print(dados_lidos[0][0])
    second_screen.tableWidget.setRowCount(len(dados_lidos))
    second_screen.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            second_screen.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))
            )


# Carregar o arquivo de interface de usuário (UI)
app = QtWidgets.QApplication([])
formulario = uic.loadUi("formulario.ui")
second_screen = uic.loadUi("listar.ui")
formulario.pushButton.clicked.connect(primary_function)
formulario.pushButton_2.clicked.connect(call_second_screen)
second_screen.pushButton.clicked.connect(gerar_pdf)
second_screen.pushButton_2.clicked.connect(gerar_txt)
second_screen.pushButton_3.clicked.connect(gerar_csv)

formulario.show()
app.exec()
