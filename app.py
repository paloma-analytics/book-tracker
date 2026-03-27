
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata



def normalizar(texto):
    
    texto = str(texto).lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def normalizar_colunas(df):
   
    df.columns = [normalizar(col) for col in df.columns]
    return df



st.markdown("""
<style>

/* FONTE */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

/* FUNDO DA PÁGINA */
.stApp {
    background-color: #fff5f8;
    background-image: radial-gradient(#ffd6e7 1px, transparent 1px);
    background-size: 30px 30px;
}

/* TÍTULO PRINCIPAL */
h1 {
    color: #d45c7a !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
}

/* SUBTÍTULOS */
h2, h3 {
    color: #c2486a !important;
}

/* CARDS DE MÉTRICA */
[data-testid="stMetric"] {
    background-color: #ffe4ef;
    border: 2px solid #ffaacb;
    border-radius: 18px;
    padding: 16px;
}

/* ABAS */
[data-testid="stTabs"] button {
    color: #c2486a !important;
    font-weight: 700 !important;
}

/* BOTÃO */
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

/* CAIXA DE UPLOAD */
[data-testid="stFileUploader"] {
    background-color: #fff0f5 !important;
    border: 2px dashed #ffaacb !important;
    border-radius: 18px !important;
    padding: 20px !important;
}

/* EXPANDER */
[data-testid="stExpander"] {
    background-color: #fff0f5 !important;
    border: 2px solid #ffaacb !important;
    border-radius: 18px !important;
}

/* TABELA */
[data-testid="stDataFrame"] {
    border: 2px solid #ffaacb !important;
    border-radius: 14px !important;
}

/* DIVISOR */
hr {
    border-color: #ffaacb !important;
}

</style>
""", unsafe_allow_html=True)



st.set_page_config(page_title="🌸 Book Tracker", page_icon="🌸", layout="wide")



st.markdown("# 🌸 Book Tracker")
st.markdown("""
### Transforme sua planilha de leituras em análises personalizadas

Faça upload da sua planilha e em segundos você terá:

🌸 **Biblioteca completa** com filtros por gênero e nota  
📊 **Estatísticas do seu perfil** — gênero favorito, média de notas, modo de leitura  
📅 **Evolução mensal** — veja como foram suas leituras mês a mês  
🎯 **Acompanhamento de meta** — defina sua meta e veja seu progresso  
🔮 **Recomendador** — descubra seus melhores livros por gênero  
""")

st.divider()



with st.expander("🌸 Como usar — clique aqui para ver o formato da planilha"):
    st.markdown("""
    Sua planilha precisa ter **essas colunas** (não precisa se preocupar com maiúsculas ou acentos):

    | titulo | mes | ano | autor | genero | nota | modo | tempo |
    |---|---|---|---|---|---|---|---|
    | A Metamorfose | 5 | 2024 | Franz Kafka | Existencialismo | 10 | Kindle | 2 semanas |

    **Regras importantes:**
    - O arquivo deve ser **.xlsx** ou **.csv**
    - A coluna **mes** deve ser número sem zero na frente (ex: 9, não 09)
    - A coluna **nota** deve ser número (ex: 8 ou 7.5)
    - Livros sem nota deixe a célula vazia
    """)


arquivo = st.file_uploader("🌸 Faça upload da sua planilha aqui", type=["xlsx", "csv"])

if arquivo is not None:

   
    if arquivo.name.endswith(".csv"):
        df = pd.read_csv(arquivo)
    else:
        df = pd.read_excel(arquivo)

    
    df = normalizar_colunas(df)

   
    colunas_necessarias = ["titulo", "mes", "ano", "autor", "genero", "nota", "modo", "tempo"]
    colunas_faltando = [col for col in colunas_necessarias if col not in df.columns]

    if colunas_faltando:
        st.error(f"🌸 Sua planilha está faltando as colunas: {', '.join(colunas_faltando)}")
        st.stop()

 
    df["nota"] = pd.to_numeric(df["nota"], errors="coerce")
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    df["mes"] = pd.to_numeric(df["mes"], errors="coerce")

    st.success(f"🌸 Planilha carregada com sucesso! {len(df)} livros encontrados.")

   

    aba1, aba2, aba3 = st.tabs(["🌸 Biblioteca", "📊 Estatísticas", "🔮 Recomendador"])


    with aba1:

        st.subheader("🌸 Todos os livros")

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

        st.caption(f"🌸 Mostrando {len(df_filtrado)} livros")

   

    with aba2:

        st.subheader("📊 Seu perfil de leitora")

       
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🌸 Total de livros", len(df))
        m2.metric("⭐ Média geral", f"{df['nota'].mean(skipna=True):.1f}")
        m3.metric("📚 Gênero favorito", df["genero"].value_counts().idxmax())
        m4.metric("✍️ Autor(a) mais lido", df["autor"].value_counts().idxmax())

        st.divider()

        
        g1, g2 = st.columns(2)

        with g1:
            st.markdown("**🌸 Livros por gênero**")
            generos_count = df["genero"].value_counts()
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
            st.markdown("**⭐ Média de nota por gênero**")
            media_genero = df.groupby("genero")["nota"].mean(numeric_only=True).sort_values(ascending=False)
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
            st.markdown("**📅 Livros lidos por ano**")
            por_ano = df["ano"].value_counts().sort_index()
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
            st.markdown("**💝 Modo de leitura favorito**")
            modos = df["modo"].value_counts()
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            fig4.patch.set_facecolor("#fff5f8")
            modos.plot(kind="pie", autopct="%1.1f%%", colors=["#ffaacb", "#c87d87", "#ec9c9d", "#f0c4cb", "#ffd6e7"], ax=ax4)
            ax4.set_ylabel("")
            plt.tight_layout()
            st.pyplot(fig4)

        st.divider()

      
        st.markdown("**📅 Livros lidos por mês**")

        anos_disponiveis = sorted(df["ano"].dropna().unique().astype(int).tolist(), reverse=True)
        ano_selecionado = st.selectbox("Selecione o ano", anos_disponiveis)

        df_ano = df[df["ano"] == ano_selecionado]
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

        st.divider()

        
        st.markdown("**🎯 Acompanhamento de meta**")

        col_meta1, col_meta2 = st.columns(2)

        with col_meta1:
            tipo_meta = st.radio("Tipo de meta", ["Anual", "Mensal"])

        with col_meta2:
            meta = st.number_input("Quantos livros é sua meta?", min_value=1, max_value=500, value=20)

        if tipo_meta == "Anual":
            ano_meta = st.selectbox("Ano da meta", anos_disponiveis, key="ano_meta")
            lidos = len(df[df["ano"] == ano_meta])
            label_meta = f"Meta anual {ano_meta}"
        else:
            ano_meta = st.selectbox("Ano", anos_disponiveis, key="ano_meta2")
            mes_meta = st.selectbox("Mês", list(range(1, 13)), format_func=lambda x: nomes_meses[x-1])
            lidos = len(df[(df["ano"] == ano_meta) & (df["mes"] == mes_meta)])
            label_meta = f"Meta mensal — {nomes_meses[mes_meta-1]}/{ano_meta}"

        faltam = max(0, meta - lidos)
        progresso = min(lidos / meta, 1.0)

       
        fig6, ax6 = plt.subplots(figsize=(8, 3))
        fig6.patch.set_facecolor("#fff5f8")
        ax6.set_facecolor("#fff5f8")

        ax6.barh(["Meta"], [meta], color="#ffd6e7", height=0.4)
        ax6.barh(["Meta"], [lidos], color="#ffaacb", height=0.4)

        ax6.set_xlim(0, max(meta, lidos) * 1.1)
        ax6.set_title(f"🎯 {label_meta} — {lidos} de {meta} livros ({progresso*100:.0f}%)", color="#d45c7a", fontweight="bold")
        ax6.set_xlabel("Livros")

        if faltam > 0:
            ax6.text(lidos + 0.3, 0, f"Faltam {faltam} 🌸", va="center", color="#d45c7a", fontweight="bold")
        else:
            ax6.text(lidos * 0.5, 0, "Meta batida! 🎉", va="center", ha="center", color="#d45c7a", fontweight="bold", fontsize=12)

        plt.tight_layout()
        st.pyplot(fig6)

  

    with aba3:

        st.subheader("🔮 Recomendador de leitura")
        st.markdown("Escolha um gênero e veja os melhores livros dessa categoria!")

        genero_rec = st.selectbox("🌸 Escolha um gênero", sorted(df["genero"].dropna().unique().tolist()))

        if st.button("🌸 Recomendar"):
            resultado = df[df["genero"] == genero_rec].dropna(subset=["nota"]).sort_values("nota", ascending=False)

            if resultado.empty:
                st.warning("Nenhum livro encontrado nesse gênero.")
            else:
                for _, livro in resultado.iterrows():
                    st.markdown(f"⭐ **{livro['nota']}** — {livro['titulo']} *({livro['autor']})*")

else:
    st.markdown("""
    <div style='text-align:center; padding: 60px 20px;'>
        <div style='font-size: 60px;'>🌸</div>
        <h2 style='color:#d45c7a;'>Bem-vinda ao Book Tracker!</h2>
        <p style='color:#c2486a; font-size:18px;'>Faça upload da sua planilha acima para começar sua análise 🌸</p>
    </div>
    """, unsafe_allow_html=True)
