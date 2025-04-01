from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Configurar credenciais do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(r"E:\FGV\DGPE\credenciais.json", scope)
client = gspread.authorize(creds)

# Abrir a planilha
spreadsheet = client.open("Base_Cursistas")
sheet = spreadsheet.sheet1  # Pegando a primeira aba

# Obter todos os dados da planilha
dados_planilha = sheet.get_all_records()

@app.route('/buscar', methods=['GET'])
def buscar_cursista():
    cpf_procurado = request.args.get('cpf', '').strip()

    if not cpf_procurado:
        return jsonify({"status": "Erro", "mensagem": "CPF não fornecido"}), 400

    print(f"🔎 Buscando CPF: {cpf_procurado}")

    for linha in dados_planilha:
        cpf_formatado = str(linha.get("CPF", "")).strip()  # Garantindo que é string
        print(f"Comparando com: {cpf_formatado}")  

        if cpf_procurado == cpf_formatado:
            print("✅ Cursista encontrado!")
            return jsonify({
                "status": "Cursista encontrado",
                "dados": {
                    "Nome": linha.get("Nome", "Desconhecido"),
                    "CPF": linha.get("CPF", "Desconhecido"),
                    "Curso": linha.get("Curso", "Não informado"),
                    "Data de Inscrição": linha.get("Data de Inscrição", "Não informado")
                }
            }), 200

    print("❌ Cursista não encontrado.")
    return jsonify({"status": "Erro", "mensagem": "Cursista não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
