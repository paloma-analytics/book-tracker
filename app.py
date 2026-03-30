
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import re
import requests
import io


def normalizar(texto):
    texto = str(texto).lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def normalizar_colunas(df):
    df.columns = [normalizar(col) for col in df.columns]
    return df

def converter_tempo(tempo):
    try:
        tempo = str(tempo).lower().strip()
        numero = float(re.findall(r'\d+\.?\d*', tempo)[0])
        if 'mes' in tempo or 'mês' in tempo:
            return numero * 30
        elif 'semana' in tempo:
            return numero * 7
        elif 'dia' in tempo:
            return numero
        else:
            return None
    except:
        return None

def dias_no_mes(mes, ano):
    import calendar
    return calendar.monthrange(int(ano), int(mes))[1]

def perfil_leitora_dinamico(genero, autor):
    perfis = {
        "romance": "Você é uma leitora romântica 💖 — se apaixona pelas histórias e vive cada emoção dos personagens.",
        "fantasia": "Você é uma leitora sonhadora ✨ — adora mundos mágicos e aventuras que vão além da realidade.",
        "suspense": "Você é uma leitora investigativa 🔍 — adora um mistério e não consegue parar até descobrir o final.",
        "existencialismo": "Você é uma leitora reflexiva 🌙 — busca profundidade nas leituras e gosta de questionar o mundo.",
        "gotico": "Você é uma leitora sombria 🖤 — se atrai pelo obscuro, pelo misterioso e pelo perturbador.",
        "distopico": "Você é uma leitora crítica 🌍 — gosta de histórias que questionam a sociedade e o futuro.",
        "terror psicologico": "Você é uma leitora corajosa 😱 — não tem medo de explorar os cantos mais sombrios da mente humana.",
        "contos": "Você é uma leitora eclética 📖 — aprecia histórias curtas e intensas que dizem muito em pouco.",
        "infantil": "Você é uma leitora nostálgica 🌈 — guarda no coração a magia das histórias da infância.",
        "diario": "Você é uma leitora humanista 🤍 — se conecta com histórias reais e experiências de vida.",
        "ficcao cientifica": "Você é uma leitora futurista 🚀 — adora explorar o que ainda está por vir e os limites da ciência.",
        "classico": "Você é uma leitora clássica 🏛️ — valoriza obras que atravessaram o tempo e continuam relevantes.",
        "young adult": "Você é uma leitora apaixonada 💫 — se conecta com histórias de descoberta, identidade e crescimento.",
        "misterio": "Você é uma leitora detetive 🕵️ — adora desvendar pistas e chegar à resposta antes do autor revelar.",
        "nao ficcao": "Você é uma leitora curiosa 🧠 — busca conhecimento real e aprender com histórias verdadeiras.",
        "literatura brasileira": "Você é uma leitora brasileira 🌿 — valoriza histórias que refletem nossa cultura e realidade.",
        "romance gotico": "Você é uma leitora sombria e apaixonada 🌹 — ama histórias que misturam amor e obscuridade.",
        "realismo": "Você é uma leitora realista 🌎 — aprecia histórias que refletem a vida com profundidade e verdade.",
        "cronicas": "Você é uma leitora observadora 🗞️ — gosta de narrativas que capturam momentos e a essência do cotidiano.",
        "poesia": "Você é uma leitora sensível 🌸 — se conecta com a beleza das palavras e a profundidade dos sentimentos.",
        "sociologia": "Você é uma leitora pensadora 🔬 — gosta de entender como a sociedade funciona e questionar estruturas.",
        "ficcao literaria": "Você é uma leitora literária 📜 — aprecia narrativas densas, bem escritas e cheias de significado.",
    }
    genero_norm = normalizar(genero)
    frase = perfis.get(genero_norm)
    if not frase:
        for chave, valor in perfis.items():
            if chave in genero_norm or genero_norm in chave:
                frase = valor
                break
    if not frase:
        frase = f"Você é uma leitora de {genero} 📚 — explora universos únicos e continua expandindo seu repertório."
    return frase + f"\n\n✍️ Sua autora favorita é **{autor}**."

def gerar_planilha_exemplo():
    dados_exemplo = [
        {"Titulo": "O Principe Cruel", "Mês": 2, "Ano": 2024, "Autor": "Holly Black", "Genero": "Fantasia", "Nota": 10, "Modo de Leitura": "Kindle", "Motivo de Leitura": "Hype", "Quantidade de Paginas": 336, "Categoria": "Fantasia", "tempo": "1 mês"},
        {"Titulo": "A Empregada", "Mês": 1, "Ano": 2025, "Autor": "Freida McFadden", "Genero": "Suspense", "Nota": 10, "Modo de Leitura": "Kindle", "Motivo de Leitura": "Hype", "Quantidade de Paginas": 304, "Categoria": "Suspense/Thriller", "tempo": "5 dias"},
        {"Titulo": "A Metamorfose", "Mês": 5, "Ano": 2024, "Autor": "Franz Kafka", "Genero": "Existencialismo", "Nota": 10, "Modo de Leitura": "Kindle", "Motivo de Leitura": "Curiosidade", "Quantidade de Paginas": 96, "Categoria": "Clássico", "tempo": "2 semanas"},
        {"Titulo": "Crime e Castigo", "Mês": 1, "Ano": 2025, "Autor": "Fiódor Dostoiévski", "Genero": "Existencialismo", "Nota": 9, "Modo de Leitura": "Kindle", "Motivo de Leitura": "Indicação", "Quantidade de Paginas": 592, "Categoria": "Clássico", "tempo": "6 meses"},
        {"Titulo": "Corte de Névoa e Fúria", "Mês": 12, "Ano": 2025, "Autor": "Sarah J. Mass", "Genero": "Fantasia", "Nota": 9, "Modo de Leitura": "Audio Livro", "Motivo de Leitura": "Hype", "Quantidade de Paginas": 656, "Categoria": "Fantasia", "tempo": "3 semanas"},
        {"Titulo": "Uma Vida Pequena", "Mês": 8, "Ano": 2025, "Autor": "Hanya Yanagihara", "Genero": "Romance", "Nota": 10, "Modo de Leitura": "Livro Fisíco", "Motivo de Leitura": "Hype", "Quantidade de Paginas": 720, "Categoria": "Ficção contemporânea", "tempo": "2 meses"},
        {"Titulo": "O Alquimista", "Mês": 1, "Ano": 2026, "Autor": "Paulo Coelho", "Genero": "Romance", "Nota": 10, "Modo de Leitura": "Audio Livro", "Motivo de Leitura": "Curiosidade", "Quantidade de Paginas": 208, "Categoria": "Ficção contemporânea", "tempo": "4 dias"},
        {"Titulo": "A Cachorra", "Mês": 2, "Ano": 2026, "Autor": "Pilar Quintana", "Genero": "Existencialismo", "Nota": 10, "Modo de Leitura": "Livro Fisíco", "Motivo de Leitura": "Indicação", "Quantidade de Paginas": 168, "Categoria": "Ficção contemporânea", "tempo": "5 dias"},
        {"Titulo": "A Hipótese do Amor", "Mês": 2, "Ano": 2025, "Autor": "Ali Hazelwood", "Genero": "Romance", "Nota": 7, "Modo de Leitura": "Kindle", "Motivo de Leitura": "Hype", "Quantidade de Paginas": 336, "Categoria": "Romance", "tempo": "1 mês"},
        {"Titulo": "Noites Brancas", "Mês": 10, "Ano": 2024, "Autor": "Fiódor Dostoiévski", "Genero": "Romance", "Nota": 8, "Modo de Leitura": "Kindle", "Motivo de Leitura": "Hype", "Quantidade de Paginas": 96, "Categoria": "Clássico", "tempo": "1 dia"},
        {"Titulo": "Orgulho e Preconceito", "Mês": 10, "Ano": 2023, "Autor": "Jane Austen", "Genero": "Romance", "Nota": 10, "Modo de Leitura": "Kindle", "Motivo de Leitura": "Indicação", "Quantidade de Paginas": 424, "Categoria": "Clássico", "tempo": "2 semanas"},
        {"Titulo": "A Professora", "Mês": 4, "Ano": 2026, "Autor": "Freida McFadden", "Genero": "Suspense", "Nota": 0, "Modo de Leitura": "Não Lido", "Motivo de Leitura": "Hype", "Quantidade de Paginas": 336, "Categoria": "Suspense/Thriller", "tempo": None},
        {"Titulo": "Grande Sertão", "Mês": 0, "Ano": 2026, "Autor": "João Guimarães Rosa", "Genero": "Romance", "Nota": 0, "Modo de Leitura": "Não Lido", "Motivo de Leitura": "Indicação", "Quantidade de Paginas": 624, "Categoria": "Clássico", "tempo": None},
        {"Titulo": "Os Irmãos Karamazov", "Mês": 0, "Ano": 2026, "Autor": "Fiódor Dostoiévski", "Genero": "Romance", "Nota": 0, "Modo de Leitura": "Não Lido", "Motivo de Leitura": "Curiosidade", "Quantidade de Paginas": 824, "Categoria": "Clássico", "tempo": None},
    ]
    df_exemplo = pd.DataFrame(dados_exemplo)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_exemplo.to_excel(writer, index=False, sheet_name="Livros")
    output.seek(0)
    return output, df_exemplo

RECOMENDACOES = {
    "fantasia": ["O Nome do Vento — Patrick Rothfuss", "O Hobbit — J.R.R. Tolkien", "A Guerra das Papoulas — Rebecca F. Kuang", "Cidade dos Ossos — Cassandra Clare", "Eragon — Christopher Paolini", "Neverwhere — Neil Gaiman", "O Ladrão de Raios — Rick Riordan", "Filha da Floresta — Juliet Marillier", "A Rainha Vermelha — Victoria Aveyard", "Flores para Algernon — Daniel Keyes", "Senhor das Moscas — William Golding", "O Mago — Trudi Canavan", "Sabriel — Garth Nix", "Uprooted — Naomi Novik", "The Cruel Prince — Holly Black"],
    "suspense": ["Garota Exemplar — Gillian Flynn", "A Menina no Trem — Paula Hawkins", "Big Little Lies — Liane Moriarty", "A Mulher na Janela — A.J. Finn", "O Silêncio dos Inocentes — Thomas Harris", "Desaparecida — Gillian Flynn", "Tudo Isso é Passado — Harlan Coben", "A Paciente Silenciosa — Alex Michaelides", "Os Suspeitos — Agatha Christie", "E Não Sobrou Nenhum — Agatha Christie", "A Testemunha — Harlan Coben", "O Homem do Castelo Alto — Philip K. Dick", "Rebecca — Daphne du Maurier", "In the Woods — Tana French", "O Estranho — Harlan Coben"],
    "romance": ["Orgulho e Preconceito — Jane Austen", "Normal People — Sally Rooney", "O Casamento de Conveniência — Beth O'Leary", "A Proposta — Kennedy Ryan", "Me Chame pelo Seu Nome — André Aciman", "Razão e Sensibilidade — Jane Austen", "Pessoas Normais — Sally Rooney", "Conversas com Amigos — Sally Rooney", "Outlander — Diana Gabaldon", "A Escolha — Nicholas Sparks", "Um Homem Chamado Ove — Fredrik Backman", "O Elo Perdido — Jojo Moyes", "Antes de Você — Jojo Moyes", "Eleanor Oliphant Está Completamente Bem — Gail Honeyman", "O Amor nos Tempos do Cólera — Gabriel García Márquez"],
    "existencialismo": ["O Estrangeiro — Albert Camus", "A Náusea — Jean-Paul Sartre", "O Processo — Franz Kafka", "Cartas a um Jovem Poeta — Rainer Maria Rilke", "O Mito de Sísifo — Albert Camus", "Sidarta — Hermann Hesse", "O Lobo da Estepe — Hermann Hesse", "Assim Falou Zaratustra — Friedrich Nietzsche", "A Morte de Ivan Ilitch — Liev Tolstói", "O Declínio de um Homem — Osamu Dazai", "Noite — Elie Wiesel", "As Horas — Michael Cunningham", "Steppenwolf — Hermann Hesse", "O Caminho de Swann — Marcel Proust", "Demian — Hermann Hesse"],
    "gotico": ["Drácula — Bram Stoker", "Frankenstein — Mary Shelley", "O Retrato de Dorian Gray — Oscar Wilde", "Rebecca — Daphne du Maurier", "A Volta do Parafuso — Henry James", "O Fantasma da Ópera — Gaston Leroux", "Jane Eyre — Charlotte Brontë", "O Morro dos Ventos Uivantes — Emily Brontë", "O Caso de Charles Dexter Ward — H.P. Lovecraft", "Nos Bastidores do Mal — Shirley Jackson", "A Queda da Casa Usher — Edgar Allan Poe", "Carmilla — Sheridan Le Fanu", "O Médico e o Monstro — Robert Louis Stevenson", "A Ilha do Doutor Moreau — H.G. Wells", "Picnic no Pendurado — Joan Lindsay"],
    "distopico": ["Admirável Mundo Novo — Aldous Huxley", "Fahrenheit 451 — Ray Bradbury", "O Conto da Aia — Margaret Atwood", "Nós — Yevgeny Zamyatin", "A Estrada — Cormac McCarthy", "Station Eleven — Emily St. John Mandel", "Os Testamentos — Margaret Atwood", "O Poder — Naomi Alderman", "Jogos Vorazes — Suzanne Collins", "Divergente — Veronica Roth", "O Homem do Castelo Alto — Philip K. Dick", "A Zona Morta — Stephen King", "Parable of the Sower — Octavia Butler", "O Conto de Dois Futuros — Kim Stanley Robinson"],
    "classico": ["Dom Quixote — Miguel de Cervantes", "Anna Kariênina — Liev Tolstói", "Guerra e Paz — Liev Tolstói", "Madame Bovary — Gustave Flaubert", "O Grande Gatsby — F. Scott Fitzgerald", "Em Busca do Tempo Perdido — Marcel Proust", "Ulisses — James Joyce", "O Som e a Fúria — William Faulkner", "Moby Dick — Herman Melville", "As Vinhas da Ira — John Steinbeck", "O Sol Também se Levanta — Ernest Hemingway", "A Letra Escarlate — Nathaniel Hawthorne", "Middlemarch — George Eliot", "Vanity Fair — William Thackeray"],
    "literatura brasileira": ["Dom Casmurro — Machado de Assis", "Vidas Secas — Graciliano Ramos", "Grande Sertão: Veredas — João Guimarães Rosa", "A Hora da Estrela — Clarice Lispector", "Capitães da Areia — Jorge Amado", "O Cortiço — Aluísio Azevedo", "Memórias Póstumas de Brás Cubas — Machado de Assis", "Laços de Família — Clarice Lispector", "Quarto de Despejo — Carolina Maria de Jesus", "O Quinze — Rachel de Queiroz", "Menino de Engenho — José Lins do Rego", "Gabriela, Cravo e Canela — Jorge Amado", "Um Defeito de Cor — Ana Maria Gonçalves", "Torto Arado — Itamar Vieira Junior", "Bom Criolo — Adolfo Caminha"],
    "contos": ["A Hora da Estrela — Clarice Lispector", "O Aleph — Jorge Luis Borges", "Ficciones — Jorge Luis Borges", "Homens Sem Mulheres — Haruki Murakami", "Os Mortos — James Joyce", "Dublinenses — James Joyce", "Noite — Clarice Lispector", "Depois do Terremoto — Haruki Murakami", "O Jardim de Veredas que se Bifurcam — Jorge Luis Borges", "Os Contos de Sherlock Holmes — Arthur Conan Doyle", "Todos os Fogos o Fogo — Julio Cortázar", "A Conferência de Negócios — Anton Tchekhov"],
    "young adult": ["Harry Potter — J.K. Rowling", "Percy Jackson — Rick Riordan", "O Labirinto — James Dashner", "Divergente — Veronica Roth", "A Culpa é das Estrelas — John Green", "Cidade de Ossos — Cassandra Clare", "Feyre e a Corte das Rosas — Sarah J. Maas", "Caçadores de Sombras — Cassandra Clare", "An Ember in the Ashes — Sabaa Tahir", "Scythe — Neal Shusterman", "The Cruel Prince — Holly Black", "The Poppy War — Rebecca F. Kuang", "Six of Crows — Leigh Bardugo", "Children of Blood and Bone — Tomi Adeyemi"],
    "misterio": ["E Não Sobrou Nenhum — Agatha Christie", "O Assassinato no Expresso do Oriente — Agatha Christie", "Morte no Nilo — Agatha Christie", "O Cão dos Baskervilles — Arthur Conan Doyle", "A Liga dos Carecas — Arthur Conan Doyle", "O Nome da Rosa — Umberto Eco", "A Sombra do Vento — Carlos Ruiz Zafón", "Em Busca da Criança Perdida — Elena Ferrante", "A Mulher que Desapareceu — Agatha Christie", "O Caso dos Dez Negrinhos — Agatha Christie"],
    "nao ficcao": ["Sapiens — Yuval Noah Harari", "O Poder do Hábito — Charles Duhigg", "Thinking Fast and Slow — Daniel Kahneman", "Educated — Tara Westover", "O Diário de Anne Frank — Anne Frank", "A Longa Jornada até a Liberdade — Nelson Mandela", "Becoming — Michelle Obama", "O Mundo de Sofia — Jostein Gaarder", "Surely You're Joking Mr. Feynman — Richard Feynman", "A Revolução dos Bichos — George Orwell"],
    "romance gotico": ["Rebecca — Daphne du Maurier", "Jane Eyre — Charlotte Brontë", "O Morro dos Ventos Uivantes — Emily Brontë", "Drácula — Bram Stoker", "A Virada do Parafuso — Henry James", "Carmilla — Sheridan Le Fanu", "O Fantasma da Ópera — Gaston Leroux", "Wuthering Heights — Emily Brontë", "Picnic no Pendurado — Joan Lindsay"],
    "realismo": ["Vidas Secas — Graciliano Ramos", "O Cortiço — Aluísio Azevedo", "Madame Bovary — Gustave Flaubert", "Anna Kariênina — Liev Tolstói", "Dom Casmurro — Machado de Assis", "Memórias Póstumas de Brás Cubas — Machado de Assis", "As Vinhas da Ira — John Steinbeck", "Middlemarch — George Eliot", "O Quinze — Rachel de Queiroz", "Capitães da Areia — Jorge Amado"],
    "sociologia": ["Sapiens — Yuval Noah Harari", "O Segundo Sexo — Simone de Beauvoir", "A Origem da Família — Friedrich Engels", "Vigiar e Punir — Michel Foucault", "A Distinção — Pierre Bourdieu", "Raízes do Brasil — Sérgio Buarque de Holanda", "Casa Grande e Senzala — Gilberto Freyre", "O Povo Brasileiro — Darcy Ribeiro"],
    "poesia": ["Drummond — Carlos Drummond de Andrade", "Morte e Vida Severina — João Cabral de Melo Neto", "Poemas — Fernando Pessoa", "Odes — Pablo Neruda", "Leaves of Grass — Walt Whitman", "Poemas da Recordação — Conceição Evaristo", "Toda Poesia — Paulo Leminski", "Antologia Poética — Vinicius de Moraes"],
    "cronicas": ["A Alma Encantadora das Ruas — João do Rio", "Para Gostar de Ler — vários autores", "Crônicas — Fernando Sabino", "A Vida como Ela É — Nelson Rodrigues", "Beijos e Abraços — Rubem Braga", "O Homem Nu — Fernando Sabino"],
    "ficcao literaria": ["O Ano do Pensamento Mágico — Joan Didion", "As Correções — Jonathan Franzen", "A Estrada — Cormac McCarthy", "Beloved — Toni Morrison", "Americanah — Chimamanda Ngozi Adichie", "Uma Vida Pequena — Hanya Yanagihara", "Normal People — Sally Rooney", "A Balada do Pássaro e da Serpente — Suzanne Collins"],
}


st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background-color: #fff5f8;
    background-image: radial-gradient(#ffd6e7 1px, transparent 1px);
    background-size: 30px 30px;
}

h1 {
    color: #d45c7a !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #c2486a !important;
}

p, li, span, label, div {
    color: inherit;
}

[data-testid="stMetric"] {
    background-color: #ffe4ef;
    border: 2px solid #ffaacb;
    border-radius: 18px;
    padding: 16px;
}

[data-testid="stMetricLabel"] {
    color: #d45c7a !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"] {
    color: #c2486a !important;
}

[data-testid="stTabs"] button {
    color: #c2486a !important;
    font-weight: 700 !important;
}

.stButton > button {
    background-color: #ffaacb !important;
    color: #fff !important;
    border: none !important;
    border-radius: 30px !important;
    font-weight: 700 !important;
    padding: 10px 28px !important;
    transition: 0.3s !important;
}

.stButton > button:hover {
    background-color: #d45c7a !important;
    transform: translateY(-2px) !important;
}

[data-testid="stFileUploader"] {
    background-color: #fff0f5 !important;
    border: 2px dashed #ffaacb !important;
    border-radius: 18px !important;
    padding: 20px !important;
}

[data-testid="stExpander"] {
    background-color: #fff0f5 !important;
    border: 2px solid #ffaacb !important;
    border-radius: 18px !important;
}

[data-testid="stDataFrame"] {
    border: 2px solid #ffaacb !important;
    border-radius: 14px !important;
}

hr {
    border-color: #ffaacb !important;
}

@media (prefers-color-scheme: dark) {
    .stApp {
        background-color: #2d1a22 !important;
        background-image: radial-gradient(#4a2535 1px, transparent 1px) !important;
    }
    h1, h2, h3 {
        color: #ffaacb !important;
    }
    [data-testid="stMetric"] {
        background-color: #3d1f2d !important;
    }
    [data-testid="stMetricLabel"] {
        color: #ffaacb !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffd6e7 !important;
    }
}

</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Book Tracker", page_icon="🌸", layout="wide")


st.markdown("# 🌸 Book Tracker")
st.markdown("""
### Transforme sua planilha de leituras em análises personalizadas

Faça upload da sua planilha e em segundos você terá:

🌸 **Biblioteca completa** com filtros por gênero e nota  
📊 **Estatísticas do seu perfil** — gênero favorito, média de notas, modo de leitura  
📅 **Evolução mensal** — veja como foram suas leituras mês a mês  
🎯 **Acompanhamento de meta** — defina sua meta e veja seu progresso  
🔮 **Recomendador** — descubra novas leituras com base no que você já amou  
""")

st.divider()


with st.expander("🌸 Como usar — clique aqui para ver o formato da planilha"):
    st.markdown("""
    Sua planilha pode ter **qualquer combinação dessas colunas**:

    | Titulo | Mês | Ano | Autor | Genero | Nota | Modo de Leitura | Motivo de Leitura | Quantidade de Paginas | Categoria | tempo |
    |---|---|---|---|---|---|---|---|---|---|---|

    **Regras importantes:**
    - O arquivo deve ser **.xlsx** ou **.csv**
    - A coluna **Mês** deve ser número sem zero na frente (ex: 9, não 09)
    - A coluna **Nota** deve ser número (ex: 8 ou 7.5)
    - Livros sem nota ou com nota 0 serão classificados como **Leituras futuras**
    - Colunas opcionais: **Motivo de Leitura**, **Quantidade de Paginas**, **Categoria**
    """)

    planilha_bytes, df_exemplo_preview = gerar_planilha_exemplo()

    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        st.download_button(
            label="📥 Baixar planilha de exemplo",
            data=planilha_bytes,
            file_name="planilha_exemplo_book_tracker.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col_exp2:
        if st.button("🌸 Carregar planilha de exemplo no app"):
            st.session_state["usar_exemplo"] = True


arquivo = st.file_uploader("🌸 Faça upload da sua planilha aqui", type=["xlsx", "csv"])

usar_exemplo = st.session_state.get("usar_exemplo", False)

if arquivo is not None or usar_exemplo:

    if usar_exemplo and arquivo is None:
        _, df = gerar_planilha_exemplo()
        st.info("🌸 Usando a planilha de exemplo! Faça upload da sua para ver suas análises personalizadas.")
    else:
        st.session_state["usar_exemplo"] = False
        if arquivo.name.endswith(".csv"):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)

    df = normalizar_colunas(df)


    if "titulo" not in df.columns:
        st.error("🌸 Sua planilha precisa ter pelo menos a coluna: titulo")
        st.stop()

    for col in ["nota", "ano", "mes", "quantidade de paginas"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "tempo" in df.columns:
        df["tempo_dias"] = df["tempo"].apply(converter_tempo)
    else:
        df["tempo_dias"] = None

    if "nota" in df.columns:
        df["status"] = df["nota"].apply(
            lambda x: "Leituras futuras" if pd.isna(x) or x == 0 else "Lido"
        )
    else:
        df["status"] = "Lido"

    st.success(f"🌸 Planilha carregada com sucesso! {len(df)} livros encontrados.")

    aba1, aba2, aba3 = st.tabs(["🌸 Biblioteca", "📊 Estatísticas", "🔮 Recomendador"])


    with aba1:

        st.subheader("🌸 Todos os livros")

        col1, col2, col3 = st.columns(3)

        with col1:
            if "genero" in df.columns:
                generos = ["Todos"] + sorted(df["genero"].dropna().unique().tolist())
                genero_filtro = st.selectbox("Filtrar por gênero", generos)
            else:
                genero_filtro = "Todos"

        with col2:
            if "nota" in df.columns:
                nota_minima = st.slider("Nota mínima", 0, 10, 0)
            else:
                nota_minima = 0

        with col3:
            status_filtro = st.selectbox("Status", ["Todos", "Lidos", "Leituras futuras"])

        df_filtrado = df.copy()

        if genero_filtro != "Todos" and "genero" in df.columns:
            df_filtrado = df_filtrado[df_filtrado["genero"] == genero_filtro]

        if status_filtro == "Lidos":
            df_filtrado = df_filtrado[df_filtrado["status"] == "Lido"]
        elif status_filtro == "Leituras futuras":
            df_filtrado = df_filtrado[df_filtrado["status"] == "Leituras futuras"]

        if "nota" in df.columns:
            df_filtrado = df_filtrado[
                (df_filtrado["nota"] >= nota_minima) | (df_filtrado["nota"].isna())
            ]

        if "nota" in df.columns:
            df_filtrado = df_filtrado.sort_values("nota", ascending=False)

        colunas_exibir = [c for c in ["titulo", "autor", "genero", "nota", "modo de leitura", "tempo", "ano", "status", "categoria", "motivo de leitura", "quantidade de paginas"] if c in df_filtrado.columns]

        st.dataframe(
            df_filtrado[colunas_exibir],
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"🌸 Mostrando {len(df_filtrado)} livros")

    with aba2:

        st.subheader("📊 Seu perfil de leitora")

        df_lidos = df[df["status"] == "Lido"].copy()

        m1, m2, m3 = st.columns(3)
        m4, m5, m6 = st.columns(3)

        m1.metric("🌸 Total de livros lidos", len(df_lidos))

        if "nota" in df.columns:
            m2.metric("⭐ Média geral", f"{df_lidos['nota'].mean(skipna=True):.1f}")
        else:
            m2.metric("⭐ Média geral", "—")

        if "genero" in df.columns and len(df_lidos) > 0:
            genero_top = df_lidos["genero"].value_counts().idxmax()
            m3.metric("📚 Gênero favorito", genero_top)
        else:
            genero_top = "—"
            m3.metric("📚 Gênero favorito", "—")

        if "autor" in df.columns and len(df_lidos) > 0:
            autor_top = df_lidos["autor"].value_counts().idxmax()
            m4.metric("✍️ Autor(a) mais lido", autor_top)
        else:
            autor_top = "—"
            m4.metric("✍️ Autor(a) mais lido", "—")

        if "mes" in df.columns and "ano" in df.columns and len(df_lidos) > 0:
            meses_com_leitura = df_lidos.dropna(subset=["mes", "ano"]).groupby(["ano", "mes"]).size().reset_index()
            qtd_meses = len(meses_com_leitura)
            media_por_mes = len(df_lidos) / qtd_meses if qtd_meses > 0 else 0
            m5.metric("📅 Média de livros por mês", f"{media_por_mes:.1f}")
        else:
            m5.metric("📅 Média de livros por mês", "—")

        if "quantidade de paginas" in df.columns and "mes" in df.columns and "ano" in df.columns:
            df_paginas = df_lidos.dropna(subset=["quantidade de paginas", "mes", "ano"]).copy()
            df_paginas = df_paginas[df_paginas["mes"] > 0]
            if len(df_paginas) > 0:
                df_paginas["dias_mes"] = df_paginas.apply(
                    lambda r: dias_no_mes(r["mes"], r["ano"]), axis=1
                )
                total_paginas = df_paginas["quantidade de paginas"].sum()
                total_dias = df_paginas["dias_mes"].sum()
                media_pag_dia = total_paginas / total_dias if total_dias > 0 else 0
                m6.metric("📖 Média de páginas por dia", f"{media_pag_dia:.0f}")
            else:
                m6.metric("📖 Média de páginas por dia", "—")
        else:
            if genero_top != "—" and autor_top != "—":
                frase_perfil = perfil_leitora_dinamico(genero_top, autor_top)
                with m6:
                    st.markdown(f"""
                    <div style='background-color:#ffe4ef; border:2px solid #ffaacb; border-radius:18px; padding:16px;'>
                        <div style='color:#d45c7a; font-weight:700; font-size:13px;'>🧠 Perfil de leitora</div>
                        <div style='color:#c2486a; font-size:13px; margin-top:6px;'>{frase_perfil}</div>
                    </div>
                    """, unsafe_allow_html=True)

        if "quantidade de paginas" in df.columns and genero_top != "—" and autor_top != "—":
            frase_perfil = perfil_leitora_dinamico(genero_top, autor_top)
            st.markdown(f"""
            <div style='background-color:#ffe4ef; border:2px solid #ffaacb; border-radius:18px; padding:16px; margin-top:16px;'>
                <div style='color:#d45c7a; font-weight:700; font-size:14px;'>🧠 Perfil de leitora</div>
                <div style='color:#c2486a; font-size:13px; margin-top:6px;'>{frase_perfil}</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        if "nota" in df.columns and len(df_lidos) > 0:
            st.markdown("**🏆 Destaques de leitura**")
            d1, d2 = st.columns(2)
            df_dest = df_lidos.dropna(subset=["nota"]).copy()
            if "ano" in df.columns and "mes" in df.columns:
                df_dest = df_dest.sort_values(["ano", "mes"], ascending=[False, False])

            with d1:
                if len(df_dest) > 0:
                    maior_nota = df_dest["nota"].max()
                    melhor = df_dest[df_dest["nota"] == maior_nota].iloc[0]
                    titulo_melhor = melhor.get("titulo", "—")
                    autor_melhor = melhor.get("autor", "—") if "autor" in melhor else "—"
                    st.markdown(f"""
                    <div style='background-color:#ffe4ef; border:2px solid #ffaacb; border-radius:18px; padding:16px;'>
                        <div style='color:#d45c7a; font-weight:700; font-size:13px;'>Melhor avaliado</div>
                        <div style='color:#c2486a; font-size:18px; font-weight:800; margin-top:6px;'>⭐ {maior_nota}</div>
                        <div style='color:#c2486a; font-size:13px; margin-top:4px;'>{titulo_melhor}</div>
                        <div style='color:#d45c7a; font-size:12px;'>{autor_melhor}</div>
                    </div>
                    """, unsafe_allow_html=True)

            with d2:
                if len(df_dest) > 0:
                    menor_nota = df_dest["nota"].min()
                    pior = df_dest[df_dest["nota"] == menor_nota].iloc[0]
                    titulo_pior = pior.get("titulo", "—")
                    autor_pior = pior.get("autor", "—") if "autor" in pior else "—"
                    st.markdown(f"""
                    <div style='background-color:#ffe4ef; border:2px solid #ffaacb; border-radius:18px; padding:16px;'>
                        <div style='color:#d45c7a; font-weight:700; font-size:13px;'>Menor avaliado</div>
                        <div style='color:#c2486a; font-size:18px; font-weight:800; margin-top:6px;'>⭐ {menor_nota}</div>
                        <div style='color:#c2486a; font-size:13px; margin-top:4px;'>{titulo_pior}</div>
                        <div style='color:#d45c7a; font-size:12px;'>{autor_pior}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.divider()


        if "genero" in df.columns:
            g1, g2 = st.columns(2)

            with g1:
                st.markdown("**🌸 Livros por gênero**")
                generos_count = df_lidos["genero"].value_counts()
                fig, ax = plt.subplots(figsize=(6, 4))
                fig.patch.set_facecolor("#fff5f8")
                ax.set_facecolor("#fff5f8")
                generos_count.plot(kind="bar", color="#ffaacb", ax=ax)
                ax.set_xlabel("")
                ax.set_ylabel("Quantidade")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                st.pyplot(fig)

            with g2:
                if "nota" in df.columns:
                    st.markdown("**⭐ Média de nota por gênero**")
                    media_genero = df_lidos.groupby("genero")["nota"].mean(numeric_only=True).sort_values(ascending=False)
                    fig2, ax2 = plt.subplots(figsize=(6, 4))
                    fig2.patch.set_facecolor("#fff5f8")
                    ax2.set_facecolor("#fff5f8")
                    media_genero.plot(kind="bar", color="#c87d87", ax=ax2)
                    ax2.set_xlabel("")
                    ax2.set_ylabel("Média")
                    plt.xticks(rotation=45, ha="right")
                    plt.tight_layout()
                    st.pyplot(fig2)

        g3, g4 = st.columns(2)

        with g3:
            if "ano" in df.columns:
                st.markdown("**📅 Livros lidos por ano**")
                por_ano = df_lidos["ano"].value_counts().sort_index()
                fig3, ax3 = plt.subplots(figsize=(6, 4))
                fig3.patch.set_facecolor("#fff5f8")
                ax3.set_facecolor("#fff5f8")
                por_ano.plot(kind="bar", color="#ec9c9d", ax=ax3)
                ax3.set_xlabel("")
                ax3.set_ylabel("Quantidade")
                plt.xticks(rotation=0)
                plt.tight_layout()
                st.pyplot(fig3)

        with g4:
            col_modo = "modo de leitura" if "modo de leitura" in df.columns else "modo" if "modo" in df.columns else None
            if col_modo:
                st.markdown("**💝 Modo de leitura favorito**")
                modos = df_lidos[col_modo].value_counts()
                fig4, ax4 = plt.subplots(figsize=(6, 4))
                fig4.patch.set_facecolor("#fff5f8")
                modos.plot(kind="pie", autopct="%1.1f%%", colors=["#ffaacb", "#c87d87", "#ec9c9d", "#f0c4cb", "#ffd6e7"], ax=ax4)
                ax4.set_ylabel("")
                plt.tight_layout()
                st.pyplot(fig4)

        col_motivo = "motivo de leitura" if "motivo de leitura" in df.columns else None
        if col_motivo:
            st.divider()
            st.markdown("**💡 Motivo de leitura**")
            motivos = df_lidos[col_motivo].value_counts()
            fig_mot, ax_mot = plt.subplots(figsize=(8, 4))
            fig_mot.patch.set_facecolor("#fff5f8")
            ax_mot.set_facecolor("#fff5f8")
            motivos.plot(kind="bar", color="#f0c4cb", ax=ax_mot)
            ax_mot.set_xlabel("")
            ax_mot.set_ylabel("Quantidade")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig_mot)

        if "mes" in df.columns and "ano" in df.columns:
            st.divider()
            st.markdown("**📅 Livros lidos por mês**")
            anos_disponiveis = sorted(df_lidos["ano"].dropna().unique().astype(int).tolist(), reverse=True)
            if anos_disponiveis:
                ano_selecionado = st.selectbox("Selecione o ano", anos_disponiveis)
                df_ano = df_lidos[df_lidos["ano"] == ano_selecionado]
                livros_por_mes = df_ano.groupby("mes").size().reindex(range(1, 13), fill_value=0)
                nomes_meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
                livros_por_mes.index = nomes_meses
                fig5, ax5 = plt.subplots(figsize=(10, 4))
                fig5.patch.set_facecolor("#fff5f8")
                ax5.set_facecolor("#fff5f8")
                bars = ax5.bar(livros_por_mes.index, livros_por_mes.values, color="#ffaacb")
                for bar in bars:
                    height = bar.get_height()
                    if height > 0:
                        ax5.text(bar.get_x() + bar.get_width() / 2., height,
                                f'{int(height)}', ha='center', va='bottom', fontweight='bold', color="#d45c7a")
                ax5.set_xlabel("")
                ax5.set_ylabel("Livros lidos")
                ax5.set_title(f"Leituras mês a mês em {ano_selecionado}", color="#d45c7a", fontweight="bold")
                plt.tight_layout()
                st.pyplot(fig5)

        if "mes" in df.columns and "ano" in df.columns:
            st.divider()
            st.markdown("**Meta de leitura**")
            col_meta1, col_meta2 = st.columns(2)
            nomes_meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
            with col_meta1:
                tipo_meta = st.radio("Tipo de meta", ["Anual", "Mensal"])
            with col_meta2:
                meta = st.number_input("Quantos livros é sua meta?", min_value=1, max_value=500, value=20)

            anos_disponiveis_meta = sorted(df_lidos["ano"].dropna().unique().astype(int).tolist(), reverse=True) if len(df_lidos) > 0 else [2026]

            if tipo_meta == "Anual":
                ano_meta = st.selectbox("Ano da meta", anos_disponiveis_meta, key="ano_meta")
                df_meta = df_lidos[df_lidos["ano"] == ano_meta]
                livros_por_mes_meta = df_meta.groupby("mes").size().reindex(range(1, 13), fill_value=0)
                livros_por_mes_meta.index = nomes_meses
                lidos_total = int(livros_por_mes_meta.sum())
                import calendar
                dias_por_mes = [calendar.monthrange(ano_meta, m)[1] for m in range(1, 13)]
                total_dias_ano = sum(dias_por_mes)
                linha_meta = [(meta * d / total_dias_ano) for d in dias_por_mes]
                label_meta = f"Meta anual {ano_meta} — {lidos_total} de {meta} livros ({min(lidos_total/meta*100, 100):.0f}%)"
            else:
                ano_meta = st.selectbox("Ano", anos_disponiveis_meta, key="ano_meta2")
                mes_meta = st.selectbox("Mês", list(range(1, 13)), format_func=lambda x: nomes_meses[x-1])
                df_meta_m = df_lidos[(df_lidos["ano"] == ano_meta) & (df_lidos["mes"] == mes_meta)]
                lidos_total = len(df_meta_m)
                livros_por_mes_meta = pd.Series([lidos_total], index=[nomes_meses[mes_meta-1]])
                linha_meta = [meta]
                label_meta = f"Meta mensal {nomes_meses[mes_meta-1]}/{ano_meta} — {lidos_total} de {meta} livros"

            fig6, ax6 = plt.subplots(figsize=(10, 4))
            fig6.patch.set_facecolor("#fff5f8")
            ax6.set_facecolor("#fff5f8")
            bars6 = ax6.bar(livros_por_mes_meta.index, livros_por_mes_meta.values, color="#ffaacb", label="Livros lidos", zorder=2)
            ax6.plot(livros_por_mes_meta.index, linha_meta, color="#d45c7a", linewidth=2.5,
                    linestyle="--", marker="o", markersize=5, label="Meta", zorder=3)
            for bar in bars6:
                height = bar.get_height()
                if height > 0:
                    ax6.text(bar.get_x() + bar.get_width() / 2., height,
                            f'{int(height)}', ha='center', va='bottom', fontweight='bold', color="#d45c7a")
            ax6.set_xlabel("")
            ax6.set_ylabel("Livros")
            ax6.set_title(label_meta, color="#d45c7a", fontweight="bold")
            ax6.legend()
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig6)

    with aba3:

        st.subheader("🔮 Recomendador de leitura")
        st.markdown("Escolha um gênero e descubra novas leituras que você ainda não leu! 🌸")

        if "genero" in df.columns:
            opcoes_genero = sorted(df["genero"].dropna().unique().tolist())
        else:
            opcoes_genero = sorted(RECOMENDACOES.keys())

        genero_rec = st.selectbox("🌸 Escolha um gênero", opcoes_genero)

        if st.button("🌸 Recomendar"):

            ja_lidos = df["titulo"].str.lower().str.strip().tolist()
            genero_norm = normalizar(genero_rec)

            sugestoes_curadas = RECOMENDACOES.get(genero_norm, [])

            if not sugestoes_curadas:
                for chave, lista in RECOMENDACOES.items():
                    if chave in genero_norm or genero_norm in chave:
                        sugestoes_curadas = lista
                        break

            novos_curados = [s for s in sugestoes_curadas if s.split(" — ")[0].lower().strip() not in ja_lidos]

            if novos_curados:
                st.markdown(f"**📚 Sugestões de {genero_rec} para você explorar:**")
                st.markdown("")
                for livro in novos_curados:
                    st.markdown(f"🌸 {livro}")
                st.markdown("")
                st.caption("Sugestões cuidadosamente selecionadas — livros que ainda não estão na sua biblioteca!")

            else:
                with st.spinner("🌸 Buscando mais sugestões para você..."):
                    try:
                        termo_url = genero_norm.replace(" ", "_")
                        url = f"https://openlibrary.org/subjects/{termo_url}.json?limit=30"
                        resposta = requests.get(url, timeout=10)
                        dados_api = resposta.json()
                        livros_api = dados_api.get("works", [])
                        novos_api = []
                        for livro in livros_api:
                            titulo = livro.get("title", "")
                            autores = livro.get("authors", [])
                            autor = autores[0].get("name", "Autor desconhecido") if autores else "Autor desconhecido"
                            if titulo.lower().strip() not in ja_lidos:
                                novos_api.append(f"{titulo} — {autor}")
                        if novos_api:
                            st.markdown(f"**📚 Sugestões de {genero_rec} para você explorar:**")
                            st.markdown("")
                            for livro in novos_api[:10]:
                                st.markdown(f"🌸 {livro}")
                            st.markdown("")
                            st.caption("Sugestões buscadas automaticamente — livros que ainda não estão na sua biblioteca!")
                        else:
                            st.info(f"🌸 Você já leu tudo que temos de **{genero_rec}**! Que leitora incrível!")
                    except:
                        st.info(f"🌸 Você já leu tudo que temos de **{genero_rec}**! Que leitora incrível!")

else:
    st.markdown("""
    <div style='text-align:center; padding: 60px 20px;'>
        <div style='font-size: 60px;'>🌸</div>
        <h2 style='color:#d45c7a;'>Bem-vinda ao Book Tracker!</h2>
        <p style='color:#c2486a; font-size:18px;'>Faça upload da sua planilha acima para começar sua análise 🌸</p>
    </div>
    """, unsafe_allow_html=True)
