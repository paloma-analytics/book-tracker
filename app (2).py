
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title="📚 Book Tracker", page_icon="📚", layout="wide")

st.title("📚 Book Tracker")
st.markdown("Faça upload da sua planilha de leituras e descubra seu perfil de leitora!")


with st.expander("📋 Como usar — clique aqui para ver o formato da planilha"):
    st.markdown("""
    Sua planilha precisa ter **exatamente essas colunas**, nessa ordem:
    
    | titulo | mes | ano | autor | genero | nota | modo | tempo |
    |---|---|---|---|---|---|---|---|
    | A Metamorfose | 5 | 2024 | Franz Kafka | Existencialismo | 10 | Kindle | 2 semanas |
    
    **Regras importantes:**
    - O arquivo deve ser **.xlsx** ou **.csv**
    - A coluna **mes** deve ser número sem zero na frente (ex: 9, não 09)
    - A coluna **nota** deve ser número (ex: 8 ou 7.5)
    - Livros sem nota deixe a célula vazia
    """)


arquivo = st.file_uploader("📂 Faça upload da sua planilha", type=["xlsx", "csv"])


if arquivo is not None:

  
    if arquivo.name.endswith(".csv"):
        df = pd.read_csv(arquivo)
    else:
        df = pd.read_excel(arquivo)

    
    colunas_necessarias = ["titulo", "mes", "ano", "autor", "genero", "nota", "modo", "tempo"]
    colunas_faltando = [col for col in colunas_necessarias if col not in df.columns]

    if colunas_faltando:
        
        st.error(f"Sua planilha está faltando as colunas: {', '.join(colunas_faltando)}")
        st.stop()

    
    st.success(f"Planilha carregada com sucesso! {len(df)} livros encontrados.")

   

    aba1, aba2, aba3 = st.tabs(["📖 Biblioteca", "📊 Estatísticas", "🔮 Recomendador"])

 # biblioteca

    with aba1:

        st.subheader("Todos os livros")

        col1, col2 = st.columns(2)

        with col1:
            generos = ["Todos"] + sorted(df["genero"].dropna().unique().tolist())
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

   
# coluna estatistica
    with aba2:

        st.subheader("Seu perfil de leitora")

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
        st.markdown("Escolha um gênero e veja os melhores livros dessa categoria!")

        genero_rec = st.selectbox("Escolha um gênero", sorted(df["genero"].dropna().unique().tolist()))

        if st.button("Recomendar"):
            resultado = df[df["genero"] == genero_rec].dropna(subset=["nota"]).sort_values("nota", ascending=False)

            if resultado.empty:
                st.warning("Nenhum livro encontrado nesse gênero.")
            else:
                for _, livro in resultado.iterrows():
                    st.markdown(f"⭐ **{livro['nota']}** — {livro['titulo']} *({livro['autor']})*")

else:
    
    st.info("👆 Faça o upload da sua planilha para começar!")
