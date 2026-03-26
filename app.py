
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


dados = [
    {"titulo": "A Cachorra", "mes": 2, "ano": 2026, "autor": "Pilar Quintana", "genero": "Existencialismo", "nota": 10, "modo": "Livro Físico", "tempo": "5 dias"},
    {"titulo": "A Mulher em Silêncio", "mes": 1, "ano": 2026, "autor": "Freida McFadden", "genero": "Suspense", "nota": 9, "modo": "Audio Livro", "tempo": "2 dias"},
    {"titulo": "A Professora", "mes": 3, "ano": 2026, "autor": "Freida McFadden", "genero": "Suspense", "nota": 5, "modo": "Audio Livro", "tempo": "1 semana"},
    {"titulo": "A Psiquiatra", "mes": 1, "ano": 2026, "autor": "Andrea del Fuego", "genero": "Existencialismo", "nota": 9, "modo": "Livro Físico", "tempo": "2 semanas"},
    {"titulo": "A Sete Chaves", "mes": 1, "ano": 2026, "autor": "Freida McFadden", "genero": "Suspense", "nota": 6, "modo": "Audio Livro", "tempo": "5 dias"},
    {"titulo": "Até o Último de Nós", "mes": 2, "ano": 2026, "autor": "Freida McFadden", "genero": "Suspense", "nota": 6, "modo": "Audio Livro", "tempo": "4 dias"},
    {"titulo": "Convite para um Homicídio", "mes": 2, "ano": 2026, "autor": "Agatha Christie", "genero": "Suspense", "nota": 8, "modo": "Audio Livro", "tempo": "3 dias"},
    {"titulo": "Eu que Nunca Conheci os Homens", "mes": 3, "ano": 2026, "autor": "Jacqueline Harpman", "genero": "Distópico", "nota": 9, "modo": "Audio Livro", "tempo": "4 dias"},
    {"titulo": "O Alquimista", "mes": 1, "ano": 2026, "autor": "Paulo Coelho", "genero": "Existencialismo", "nota": 10, "modo": "Audio Livro", "tempo": "4 dias"},
    {"titulo": "O Detento", "mes": 2, "ano": 2026, "autor": "Freida McFadden", "genero": "Suspense", "nota": 6, "modo": "Audio Livro", "tempo": "5 dias"},
    {"titulo": "O Misterioso Caso de Styles", "mes": 1, "ano": 2026, "autor": "Agatha Christie", "genero": "Suspense", "nota": 10, "modo": "Audio Livro", "tempo": "2 dias"},
    {"titulo": "Olhos d'Água", "mes": 1, "ano": 2026, "autor": "Conceição Evaristo", "genero": "Contos", "nota": 9, "modo": "Audio Livro", "tempo": "1 semana"},
    {"titulo": "Era uma Vez um Coração Partido", "mes": 3, "ano": 2026, "autor": "Stephanie Garber", "genero": "Fantasia", "nota": 9, "modo": "Kindle", "tempo": "1 semana"},
    {"titulo": "A Balada do Felizes Para Nunca", "mes": 3, "ano": 2026, "autor": "Stephanie Garber", "genero": "Fantasia", "nota": 8, "modo": "Kindle", "tempo": "5 dias"},
    {"titulo": "1984", "mes": 12, "ano": 2025, "autor": "George Orwell", "genero": "Romance", "nota": 9, "modo": "Audio Livro", "tempo": "2 dias"},
    {"titulo": "A Empregada", "mes": 1, "ano": 2025, "autor": "Freida McFadden", "genero": "Suspense", "nota": 10, "modo": "Kindle", "tempo": "5 dias"},
    {"titulo": "A Escolha", "mes": 10, "ano": 2025, "autor": "Kiera Cass", "genero": "Romance", "nota": 7, "modo": "Audio Livro", "tempo": "3 semanas"},
    {"titulo": "A Paciente Silenciosa", "mes": 1, "ano": 2025, "autor": "Alex Michedelis", "genero": "Suspense", "nota": 7, "modo": "Kindle", "tempo": "2 semanas"},
    {"titulo": "A Pequena Coreografia do Adeus", "mes": 7, "ano": 2025, "autor": "Aline Bei", "genero": "Existencialismo", "nota": 10, "modo": "Livro Físico", "tempo": "1 dia"},
    {"titulo": "A Queda da Casa Usher", "mes": 2, "ano": 2025, "autor": "Edgar Allan Poe", "genero": "Gótico", "nota": 10, "modo": "Livro Físico", "tempo": "1 dia"},
    {"titulo": "A Seleção", "mes": 10, "ano": 2025, "autor": "Kiera Cass", "genero": "Romance", "nota": 7, "modo": "Audio Livro", "tempo": "3 semanas"},
    {"titulo": "Assistente do Vilão", "mes": 5, "ano": 2025, "autor": "Hannah Nicole Maehrer", "genero": "Fantasia", "nota": 7, "modo": "Livro Físico", "tempo": "4 dias"},
    {"titulo": "Corte de Espinhos e Rosas", "mes": 12, "ano": 2025, "autor": "Sarah J. Maas", "genero": "Fantasia", "nota": 8, "modo": "Audio Livro", "tempo": "7 dias"},
    {"titulo": "Corte de Névoa e Fúria", "mes": 12, "ano": 2025, "autor": "Sarah J. Maas", "genero": "Fantasia", "nota": 9, "modo": "Audio Livro", "tempo": "3 semanas"},
    {"titulo": "Crime e Castigo", "mes": 1, "ano": 2025, "autor": "Fiódor Dostoiévski", "genero": "Existencialismo", "nota": 9, "modo": "Kindle", "tempo": "6 meses"},
    {"titulo": "Maxton Hall - Salve-me", "mes": 4, "ano": 2025, "autor": "Mona Kasten", "genero": "Romance", "nota": 7, "modo": "Livro Físico", "tempo": "4 meses"},
    {"titulo": "Maxton Hall - Salve-se", "mes": 7, "ano": 2025, "autor": "Mona Kasten", "genero": "Romance", "nota": 8, "modo": "Livro Físico", "tempo": "1 mês"},
    {"titulo": "Memórias do Subsolo", "mes": 7, "ano": 2025, "autor": "Fiódor Dostoiévski", "genero": "Existencialismo", "nota": 8, "modo": "Livro Físico/Kindle", "tempo": "1 mês"},
    {"titulo": "Meu Pé de Laranja Lima", "mes": 6, "ano": 2025, "autor": "José Mauro de Vasconcelos", "genero": "Romance", "nota": None, "modo": "Livro Físico", "tempo": "3 semanas"},
    {"titulo": "Nunca Minta", "mes": 7, "ano": 2025, "autor": "Freida McFadden", "genero": "Suspense", "nota": 7.5, "modo": "Livro Físico", "tempo": "6 dias"},
    {"titulo": "O Corvo", "mes": 2, "ano": 2025, "autor": "Edgar Allan Poe", "genero": "Gótico", "nota": 6, "modo": "Livro Físico", "tempo": "1 dia"},
    {"titulo": "O Crime do Bom Nazista", "mes": 12, "ano": 2025, "autor": "Samir Machado de Machado", "genero": "Suspense", "nota": 10, "modo": "Audio Livro", "tempo": "3 dias"},
    {"titulo": "O Declínio de um Homem", "mes": 3, "ano": 2025, "autor": "Osamu Dazai", "genero": "Existencialismo", "nota": 10, "modo": "Livro Físico", "tempo": "3 dias"},
    {"titulo": "O Filho Perfeito", "mes": 12, "ano": 2025, "autor": "Freida McFadden", "genero": "Suspense", "nota": 6.5, "modo": "Audio Livro", "tempo": "2 dias"},
    {"titulo": "O Gato Preto", "mes": 2, "ano": 2025, "autor": "Edgar Allan Poe", "genero": "Terror Psicológico", "nota": 10, "modo": "Livro Físico", "tempo": "1 dia"},
    {"titulo": "O Herdeiro Roubado", "mes": 6, "ano": 2025, "autor": "Holly Black", "genero": "Fantasia", "nota": 8, "modo": "Livro Físico", "tempo": "2 meses"},
    {"titulo": "O Massacre da Família Hope", "mes": 12, "ano": 2025, "autor": "Riley Sager", "genero": "Suspense", "nota": 8, "modo": "Audio Livro", "tempo": "3 dias"},
    {"titulo": "O Natal de Poirot", "mes": 12, "ano": 2025, "autor": "Agatha Christie", "genero": "Suspense", "nota": 7, "modo": "Audio Livro", "tempo": "5 dias"},
    {"titulo": "O Segredo da Empregada", "mes": 2, "ano": 2025, "autor": "Freida McFadden", "genero": "Suspense", "nota": 8, "modo": "Kindle", "tempo": "5 dias"},
    {"titulo": "O Trono do Prisioneiro", "mes": 6, "ano": 2025, "autor": "Holly Black", "genero": "Fantasia", "nota": 6, "modo": "Livro Físico", "tempo": "3 meses"},
    {"titulo": "Quarto de Despejo", "mes": 12, "ano": 2025, "autor": "Carolina Maria de Jesus", "genero": "Diário", "nota": 10, "modo": "Livro Físico", "tempo": "4 dias"},
    {"titulo": "Uma Vida Pequena", "mes": 8, "ano": 2025, "autor": "Hanya Yanagihara", "genero": "Romance", "nota": 10, "modo": "Livro Físico", "tempo": "2 meses"},
    {"titulo": "A Metamorfose", "mes": 5, "ano": 2024, "autor": "Franz Kafka", "genero": "Existencialismo", "nota": 10, "modo": "Kindle", "tempo": "2 semanas"},
    {"titulo": "A Morte de Ivan Ilitch", "mes": 11, "ano": 2024, "autor": "Liev Tolstói", "genero": "Existencialismo", "nota": 9, "modo": "Kindle", "tempo": "4 dias"},
    {"titulo": "A Rainha do Nada", "mes": 4, "ano": 2024, "autor": "Holly Black", "genero": "Fantasia", "nota": 7, "modo": "Kindle", "tempo": "5 dias"},
    {"titulo": "Mil Beijos de Garotos", "mes": 10, "ano": 2024, "autor": "Tillie Cole", "genero": "Romance", "nota": 6, "modo": "Kindle", "tempo": "3 meses"},
    {"titulo": "Noites Brancas", "mes": 10, "ano": 2024, "autor": "Fiódor Dostoiévski", "genero": "Romance", "nota": 8, "modo": "Kindle", "tempo": "1 dia"},
    {"titulo": "O Jardim dos Esquecidos", "mes": 1, "ano": 2024, "autor": "V.C Andrews", "genero": "Suspense", "nota": 9, "modo": "Livro Físico", "tempo": "1 semana"},
    {"titulo": "O Príncipe Cruel", "mes": 2, "ano": 2024, "autor": "Holly Black", "genero": "Fantasia", "nota": 10, "modo": "Kindle", "tempo": "1 mês"},
    {"titulo": "O Rei Perverso", "mes": 3, "ano": 2024, "autor": "Holly Black", "genero": "Fantasia", "nota": 10, "modo": "Kindle", "tempo": "2 semanas"},
    {"titulo": "Pétalas ao Vento", "mes": 2, "ano": 2024, "autor": "V.C Andrews", "genero": "Suspense", "nota": 5, "modo": "Kindle", "tempo": "1 semana"},
    {"titulo": "Trono de Vidro", "mes": 9, "ano": 2024, "autor": "Sarah J. Maas", "genero": "Fantasia", "nota": 6, "modo": "Livro Físico", "tempo": "3 meses"},
    {"titulo": "Mais Forte que o Sol", "mes": 10, "ano": 2023, "autor": "Julia Quinn", "genero": "Romance", "nota": 6, "modo": "Livro Físico", "tempo": "1 semana"},
    {"titulo": "Mais Lindo que a Lua", "mes": 11, "ano": 2023, "autor": "Julia Quinn", "genero": "Romance", "nota": 5, "modo": "Livro Físico", "tempo": "1 semana"},
    {"titulo": "O Duque e Eu", "mes": 5, "ano": 2023, "autor": "Julia Quinn", "genero": "Romance", "nota": 8, "modo": "Kindle", "tempo": "7 dias"},
    {"titulo": "O Visconde Que Me Amava", "mes": 8, "ano": 2023, "autor": "Julia Quinn", "genero": "Romance", "nota": 8, "modo": "Kindle", "tempo": "5 dias"},
    {"titulo": "Os Segredos de Colin Bridgerton", "mes": 9, "ano": 2023, "autor": "Julia Quinn", "genero": "Romance", "nota": 7, "modo": "Kindle", "tempo": "2 semanas"},
    {"titulo": "Um Perfeito Cavalheiro", "mes": 7, "ano": 2023, "autor": "Julia Quinn", "genero": "Romance", "nota": 10, "modo": "Kindle", "tempo": "2 dias"},
    {"titulo": "Cartas ao Pai", "mes": 5, "ano": 2024, "autor": "Franz Kafka", "genero": "Diário", "nota": 10, "modo": "Kindle", "tempo": "5 dias"}, 
    {"titulo": "Cartas para Milena", "mes": 8, "ano": 2024, "autor": "Franz Kafka", "genero": "Diário", "nota": 10, "modo": "Kindle", "tempo": " 1 semana"},
    {"titulo": "A Hipótese do Amor", "mes": 12, "ano": 2024, "autor": "Ali Hazelwood", "genero": "Romance", "nota": 7, "modo": "Kindle", "tempo": " 3 semanas"},
    {"titulo": "Como o Rei de Elfhame Aprendeu a Odiar Histórias", "mes": 6, "ano": 2024, "autor": "Holly Black", "genero": "Fantasia", "nota": 9, "modo": "Kindle", "tempo": "4 dias"},
    {"titulo": "O Canto mais Escuro da Floresta", "mes": 9, "ano": 2024, "autor": "Holly Black", "genero": "Fantasia", "nota": 6, "modo": "Kindle", "tempo": "2 semanas"},
    {"titulo": "Os Relógios", "mes": 1, "ano": 2026, "autor": "Agatha Christie", "genero": "Suspense", "nota": 8, "modo": "Kindle", "tempo": "2 semanas"},
    {"titulo": "Convite para um Homicidio", "mes": 11, "ano": 2025, "autor": "Agatha Christie", "genero": "Suspense", "nota": 7, "modo": "Audio Livro", "tempo": "5 dias"},
    {"titulo": "O Morro dos Ventos Uivantes", "mes": 10, "ano": 2024, "autor": "Emily Bronte", "genero": "Gótico", "nota": 8, "modo": "Livro Físico/Kindle", "tempo": "2 semanas"},
    {"titulo": "Vidas Secas", "mes": 9, "ano": 2025, "autor": "Graciliano Ramos", "genero": "Realismo", "nota": 10, "modo": "Livro Físico/Kindle", "tempo": "1 semana"},
    {"titulo": "Coroa da Meias-Noite", "mes": 11, "ano": 2024, "autor": "Sarah J. Maas.", "genero": "Fantasia", "nota": 7, "modo": "Kindle", "tempo": "2 semanas"},
    {"titulo": "O Alienista", "mes": 1, "ano": 2026, "autor": "Machado de Assis", "genero": "Contos", "nota": 10, "modo": "Audio Livro", "tempo": "2 dias"},
    {"titulo": "Orgulho e Preconceito", "mes": 1, "ano": 2026, "autor": "Jane Austen", "genero": "Romance", "nota": 10, "modo": "Audio Livro", "tempo": "1 dia"},
    {"titulo": "Persuasão", "mes": 1, "ano": 2022, "autor": "Jane Austen", "genero": "Romance", "nota": 10, "modo": "Livro Físico", "tempo": " 4 semanas"},
    {"titulo": "Razão e Sensibilidade", "mes": 4, "ano": 2022, "autor": "Jane Austen", "genero": "Romance", "nota": 10, "modo": "Livro Físico", "tempo": "1 mês"},
    {"titulo": "A Dama Mais Apaixonada", "mes": 7, "ano": 2022, "autor": "Julia Quinn", "genero": "Romance", "nota": 4, "modo": "Livro Físico", "tempo": "2 meses"},
    {"titulo": "A Quarta Asa", "mes": 7, "ano": 2025, "autor": "Rebecca Yarros", "genero": "Fantasia", "nota": 8, "modo": "Livro Físico/Kindle", "tempo": "2 semanas"},
    {"titulo": "Anna Kariênina", "mes": 1, "ano": 2024, "autor": "Liev Tolstói", "genero": "Romance", "nota": 9, "modo": "Livro Físico/Kindle", "tempo": "3 meses"},
    {"titulo": "A Evolução de Calpúrnia Tate", "mes": 3, "ano": 2018, "autor": "Jacqueline Kelly", "genero": "Infantil", "nota": 8, "modo": "Livro Físico", "tempo": "4 meses"},
]

df = pd.DataFrame(dados)


st.set_page_config(page_title="📚 Book Tracker", page_icon="📚", layout="wide")

st.title("📚 Minha Biblioteca Pessoal")
st.markdown("Explore os livros que já li, filtre por gênero e descubra meu perfil de leitora.")


aba1, aba2, aba3 = st.tabs(["📖 Biblioteca", "📊 Estatísticas", "🔮 Recomendador"])



with aba1:

    st.subheader("Todos os livros")

   
    col1, col2 = st.columns(2)

    with col1:
       
        generos = ["Todos"] + sorted(df["genero"].unique().tolist())
        genero_filtro = st.selectbox("Filtrar por gênero", generos)

    with col2:
      
        nota_minima = st.slider("Nota mínima", 0, 10, 0)


    df_filtrado = df.copy()

    if genero_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["genero"] == genero_filtro]

    df_filtrado = df_filtrado[df_filtrado["nota"] >= nota_minima]

    df_filtrado = df_filtrado.sort_values("nota", ascending=False)

    st.dataframe(
        df_filtrado[["titulo", "autor", "genero", "nota", "modo", "tempo", "ano"]],
        use_container_width=True,
        hide_index=True
    )

    st.caption(f"Mostrando {len(df_filtrado)} livros")



with aba2:

    st.subheader("Meu perfil de leitora")


    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total de livros", len(df))
    m2.metric("Média geral", f"{df['nota'].mean(skipna=True):.1f}")
    m3.metric("Gênero favorito", df["genero"].value_counts().idxmax())
    m4.metric("Autor(a) mais lido", df["autor"].value_counts().idxmax())

    st.divider()

  
    g1, g2 = st.columns(2)

    with g1:
        st.markdown("**Livros por gênero**")
        generos_count = df["genero"].value_counts()
        fig, ax = plt.subplots(figsize=(6, 4))
        generos_count.plot(kind="bar", color="#ffaacb", ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("Quantidade")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig)

    with g2:
        st.markdown("**Média de nota por gênero**")
        media_genero = df.groupby("genero")["nota"].mean(numeric_only=True).sort_values(ascending=False)
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        media_genero.plot(kind="bar", color="#c87d87", ax=ax2)
        ax2.set_xlabel("")
        ax2.set_ylabel("Média")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig2)

    g3, g4 = st.columns(2)

    with g3:
        st.markdown("**Livros lidos por ano**")
        por_ano = df["ano"].value_counts().sort_index()
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        por_ano.plot(kind="bar", color="#ec9c9d", ax=ax3)
        ax3.set_xlabel("")
        ax3.set_ylabel("Quantidade")
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig3)

    with g4:
        st.markdown("**Modo de leitura favorito**")
        modos = df["modo"].value_counts()
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        modos.plot(kind="pie", autopct="%1.1f%%", colors=["#ffaacb", "#c87d87", "#ec9c9d", "#f0c4cb"], ax=ax4)
        ax4.set_ylabel("")
        plt.tight_layout()
        st.pyplot(fig4)



with aba3:

    st.subheader("🔮 Recomendador de leitura")
    st.markdown("Escolha um gênero e veja os melhores livros que já li nessa categoria!")

    genero_rec = st.selectbox("Escolha um gênero", sorted(df["genero"].unique().tolist()))

    if st.button("Recomendar"):
        resultado = df[df["genero"] == genero_rec].dropna(subset=["nota"]).sort_values("nota", ascending=False)

        if resultado.empty:
            st.warning("Nenhum livro encontrado nesse gênero.")
        else:
            for _, livro in resultado.iterrows():
                st.markdown(f"⭐ **{livro['nota']}** — {livro['titulo']} *({livro['autor']})*")
