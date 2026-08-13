import pandas as pd
import re

PRIVACY_LIST = ['abusivo', 'adware', 'comportamento', 'comportamental', 'consentimento', 'permissão', 'duvidoso', 'suspeito', 'criptografar', 'criptografia', 'criptografa', 'ético', 'ética', 'moral', 'fraude', 'hack', 'hackeado', 'invadido', 'hacking', 'pirataria', 'hacks', 'inseguro', 'software livre', 'código aberto', 'permissão', 'autorização', 'permissões', 'autorizações', 'phishing', 'privacidade', 'protegido', 'seguro', 'proteção', 'defesa', 'enganar', 'seguro', 'fraude', 'golpe', 'enganado', 'golpista', 'golpistas', 'fraude', 'seguro', 'protegido', 'segurança', 'código-fonte', 'spyware', 'espião', 'terceiro', 'terceiros', 'confiavelmente', 'confiança', 'credibilidade', 'confiável', 'antiético', 'antiética', 'desprotegido', 'desproteção', 'inseguro', 'perigoso', 'inseguro', 'desonesto', 'não confiável']

CATEGORIES = {
    'politica': {
        'keywords': ["políticas", "política", "regulamento", "regulamentos", "regulatório"]
    },
    'localizacao': {
        'keywords': ["gps", "localização", "localizações", "mapa", "localiza", "localizando"]
    },
    'dados': {
        'keywords': ["comportamento", "comportamental", "dado", "dados",
                     "informação", "informações", "pessoal", "pessoais",
                     "privado", "compartilhando", "compartilhamento", "compartilha",
                     "segue", "seguindo"]
    },
    'permissao': {
        'keywords': ["autorização", "autorizar", "autoriza", "consentimento",
                     "consentir", "consentindo", "permissão", "permitir", "permissões"]
    },
    'propaganda': {
        'keywords': ["propaganda", "propagandas", "anúncio", "anúncios",
                     "publicidade", "publicidades", "adware"]
    },
    'seguranca': {
        'keywords': ["criptografar", "criptografa", "criptografia", "hackear",
                     "hackeando", "hackeado", "hackeada", "hackeia", "inseguro",
                     "insegura", "insegurança", "seguro", "segura", "segurança", "spyware"]
    },
    'confianca': {
        'keywords': ["abusivo", "abusiva", "ético", "ética", "código aberto",
                     "código livre", "protegido", "protegida", "proteção", "código-fonte",
                     "confiar", "confia", "confio", "confiável", "antiético",
                     "desprotegida", "desprotegido", "desproteção"]
    },
    'fraude': {
        'keywords': ["fraude", "fraudulento", "engano", "enganação", "enganar",
                     "enganado", "enganada", "golpe", "golpista", "golpistas", "engana",
                     "paga", "pago", "pagar", "pagamento", "pagamentos",
                     "comprar", "compra", "compro", "comprado", "comprada",
                     "assinar", "assinatura", "assinado", "assinante"]
    }
}

def normalize_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = s.lower()
    s = re.sub(r"[^\w\s\-]", " ", s)   
    s = re.sub(r"\s+", " ", s).strip()
    return s

def contains_any(text: str, keywords) -> bool:
    return any(k in text for k in keywords)

def classify_and_filter(input_csv, output_csv):
    print(f'Loading data from {input_csv}...')
    try:
        df = pd.read_csv(input_csv, sep=';')
    except FileNotFoundError:
        print(f"Error: The file {input_csv} was not found.")
        return

    filtered_rows = []

    print('Classifying and filtering reviews...')
    for index, row in df.iterrows():
        raw = row.get('review')
        if pd.isna(raw):
            continue
            
        text = normalize_text(str(raw))
        

        if not contains_any(text, PRIVACY_LIST):
            continue
            
        new_row = row.to_dict()
        
        # check for each category and add a new column with 'Yes' if any keyword is found
        for category_name, category in CATEGORIES.items():
            if contains_any(text, category['keywords']):
                new_row[category_name] = 'Yes'
            else:
                new_row[category_name] = ''
                
        filtered_rows.append(new_row)

    filtered_df = pd.DataFrame(filtered_rows)
    

    for category_name in CATEGORIES.keys():
        if category_name not in filtered_df.columns:
            filtered_df[category_name] = ''
            
    filtered_df.to_csv(output_csv, sep=';', index=False)
    print(f'Classification for the whole file done! The file has been saved as {output_csv}.')

if __name__ == "__main__":
    INPUT_CSV = "app_reviews_part_1.csv"
    OUTPUT_CSV = "categorized_reviews.csv"
    classify_and_filter(INPUT_CSV, OUTPUT_CSV)