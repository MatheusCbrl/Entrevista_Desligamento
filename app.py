import streamlit as st
from supabase import create_client, Client
import plotly.express as px
import pandas as pd

# Configurando a conexão com Supabase
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)

# Dados de login (usuário e senha para autenticação)
USUARIO = st.secrets["login"]["usuario"]
SENHA = st.secrets["login"]["senha"]


# Função para inserir dados no Supabase
def inserir_dados(dados):
    supabase.table("pesquisa_desligamento").insert(dados).execute()

# Função para buscar dados com filtros
def buscar_dados(natureza=None, tempo_empresa=None, setor=None, genero=None):
    query = supabase.table("pesquisa_desligamento").select("*")
    
    if natureza:
        query = query.eq("natureza", natureza)
    if tempo_empresa:
        query = query.ilike("tempo_empresa", f"%{tempo_empresa}%")
    if setor:
        query = query.ilike("setor", f"%{setor}%")
    if genero:
        query = query.eq("genero", genero)
        
    response = query.execute()
    return pd.DataFrame(response.data)

# Função para mostrar tela de login
def mostrar_login():
    st.title("Login")
    usuario = st.text_input("Usuário:")
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if usuario == USUARIO and senha == SENHA:
            st.session_state.authenticated = True
        else:
            st.error("Usuário ou senha incorretos")

# Verificar autenticação
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    mostrar_login()
else:
    # Título do site
    st.title("Pesquisa de Desligamento - WCM")
    
    # Tabs para navegação
    tab1, tab2 = st.tabs(["Preencher Pesquisa", "Consultar Respostas"])
    
    # Tab 1 - Preencher Pesquisa
    with tab1:
        # Campos de preenchimento
        nome = st.text_input("Nome:")
        genero = st.selectbox("Gênero:", ["Masculino", "Feminino", "Outro"])
        idade = st.number_input("Idade:", min_value=18, max_value=100, step=1)
        tempo_empresa = st.text_input("Tempo de empresa:")
        setor = st.selectbox("Setor:", ["administração","recursos humanos","financeiro","contábil","marketing e vendas","produção","logística","tecnologia da informação","jurídico, pesquisa","compras","suprimentos","atendimento ao cliente"])
        
        cargo = st.text_input("Cargo:")
        data = st.date_input("Data de Desligamento:", format="DD/MM/YYYY")
        
        # Natureza do desligamento
        st.subheader("Natureza do Desligamento:")
        natureza = st.radio("", 
                            ["Exoneração", "Aposentadoria compulsória", "Demissão", "Término de Contrato",
                             "Aposentadoria voluntária", "Posse em outro cargo inacumulável", 
                             "Aposentadoria por invalidez", "Outro"])
        
        # Perguntas
        st.subheader("Perguntas")
        motivos_desligamento = st.text_area("Quais são os motivos que levaram o seu desligamento?")
        q1 = st.radio("01. Você voltaria a trabalhar na WCM?", ["Sim", "Não"])
        q2 = st.text_area("02. Se sim, o que precisaria ser mudado para o seu retorno?")
        q3 = st.text_area("03. Você gostaria de retornar em outro cargo ou setor? Se sim, qual?")
        q4 = st.text_area("04. Você já tem em vista alguma nova possibilidade de trabalho? Se sim, qual seria?")
        q5 = st.text_area("05. Aspectos POSITIVOS da empresa?")
        q6 = st.text_area("06. Aspectos NEGATIVOS da empresa?")
        q7 = st.radio("07. Você acha que seu potencial foi bem aproveitado?", ["Sim", "Não"])
        q8 = st.text_area("08. Você foi exigido demais ou aquém das suas capacidades?")
        q9 = st.radio("09. A empresa ofereceu oportunidades de crescimento?", ["Sim", "Não"])
        q10 = st.text_area("10. Opinião sobre o programa de treinamento da empresa?"),
        q11 = st.text_area("O trabalho que você realizava era reconhecido e valorizado? Por quê?")
        q12 = st.text_area("Durante o tempo que esteve trabalhando na empresa como foi o seu relacionamento com os colegas de trabalho?")
        q13 = st.text_area("Qual a sua percepção sobre a Qualidade de Vida no Trabalho no ambiente onde você atuava?")
        q14 = st.text_area("Qual a sua opinião em relação aos canais de comunicação internos?")
        q15 = st.text_area("Qual a sua opinião sobre as condições de trabalho do seu setor?(estrutura física, iluminação, equipamentos, mobiliário, suporte técnico, informática, etc.)")
        q16 = st.text_area("Qual a sua opinião sobre a organização do trabalho no seu setor?(prazos, pausas, ritmo e distribuição das tarefas, desgaste, etc.)")
        q17 = st.text_area("Como você avalia a sua relação com o seu ex-gestor no período em que atuaram juntos?")
        q18 = st.text_area("Faça algum comentário POSITIVO sobre o trabalho desenvolvido pela Direção, gestores ou coordenadores?")
        q18 = st.text_area("Faça algum comentário NEGATIVO sobre o trabalho desenvolvido pela Direção, gestores ou coordenadores?")
        q19 = st.text_area("Qual sua sugestão de melhoria para mudança na empresa?")
        q20 = st.text_area("Se você abrisse a sua empresa, qual colega de trabalho você contrataria para trabalhar com você? Por que?")
        q21 = st.text_area("E qual colega de trabalho você NÂO contrataria para trabalhar com você? Por que?")
        q22 = st.text_area("O que você mudaria no seu modo de trabalho no período que trabalhou na WCM?")
        q23 = st.text_area("Você indicaria a WCM para algum amigo ou conhecido trabalhar? Por quê?")
        
        # (continua com as demais perguntas...)
        
        # Avaliação da empresa
        st.subheader("Avalie a Empresa WCM:")
        avaliacao = {
            "Empresa WCM": st.slider("Como você avalia a empresa WCM", 5, 10),
            "Superior Imediato": st.slider("Como você avalia seu superior imediato", 5, 10),
            "Colegas de Setor": st.slider("Como você avalia seus colegas de setor", 5, 10),
            "RH": st.slider("Como você avalia o RH da WCM", 5, 10),
            # Adicionar mais avaliações conforme necessário
        }
        
        # Recontratação
        st.subheader("Indicação para Recontratação:")
        recontratacao = st.radio("Você seria indicado para recontratação?", ["Sim", "Não"])
        
        # Botão para enviar respostas
        if st.button("Enviar Respostas"):
            dados = {
                "nome": nome,
                "genero": genero,
                "idade": idade,
                "tempo_empresa": tempo_empresa,
                "setor": setor,
                "cargo": cargo,
                "data":  data.strftime("%d-%m-%Y"),  # Convertendo a data para string no formato DD-MM-YYYY,
                "natureza": natureza,
                "motivos_desligamento": motivos_desligamento,
                "q1": q1, 
                "q2": q2, 
                "q3": q3, 
                "q4": q4, 
                "q5": q5, 
                "q6": q6, 
                "q7": q7, 
                "q8": q8, 
                "q9": q9, 
                "q10": q10,
                "q11": q11,
                "q12": q12,
                "q13": q13,
                "q14": q14,
                "q15": q15,
                "q16": q16,
                "q17": q17,
                "q18": q18,
                "q18": q18,
                "q19": q19,
                "q20": q20,
                "q21": q21,
                "q22": q22,
                "q23": q23,
                "avaliacao": avaliacao,
                "recontratacao": recontratacao
            }
            inserir_dados(dados)
            st.success("Respostas enviadas com sucesso!")
        
        # Gráfico de avaliação
        st.subheader("Gráfico da Avaliação:")
        avaliacao_df = pd.DataFrame(list(avaliacao.items()), columns=["Aspecto", "Nota"])
        grafico = px.bar(avaliacao_df, x="Aspecto", y="Nota", title="Avaliação da Empresa")
        st.plotly_chart(grafico)
    # Tab 2 - Consultar Respostas
    with tab2:
        st.header("Consultar Respostas da Pesquisa")
    
        # Filtros
        filtro_natureza = st.selectbox("Filtrar por Natureza do Desligamento:", [""] + ["Exoneração", "Aposentadoria compulsória", "Demissão", "Término de Contrato", "Aposentadoria voluntária", "Posse em outro cargo inacumulável", "Aposentadoria por invalidez", "Outro"])
        filtro_tempo_empresa = st.text_input("Filtrar por Tempo de Empresa (ex: '3 anos'):")
        filtro_setor = st.selectbox("Setor da empresa:", ["administração","recursos humanos","financeiro","contábil","marketing e vendas","produção","logística","tecnologia da informação","jurídico, pesquisa","compras","suprimentos","atendimento ao cliente"])
        filtro_genero = st.selectbox("Filtrar por Gênero:", ["", "Masculino", "Feminino", "Outro"])
    
        # Botão para aplicar filtros
        if st.button("Aplicar Filtros"):
            # Buscar dados com os filtros aplicados
            dados_filtrados = buscar_dados(
                natureza=filtro_natureza if filtro_natureza != "" else None,
                tempo_empresa=filtro_tempo_empresa if filtro_tempo_empresa != "" else None,
                setor=filtro_setor if filtro_setor != "" else None,
                genero=filtro_genero if filtro_genero != "" else None
            )
    
            # Verificar se existem dados
            if not dados_filtrados.empty:
                # Exibir os dados filtrados
                st.dataframe(dados_filtrados)
    
                # Converter o campo 'avaliacao' de JSON para colunas separadas
                avaliacao_df = dados_filtrados['avaliacao'].apply(pd.Series)
    
                # Calcular médias das avaliações
                medias_avaliacoes = avaliacao_df.mean()
    
                # Gráfico de barras das médias das avaliações
                st.subheader("Média das Avaliações dos Aspectos da Empresa")
                grafico_avaliacoes = px.bar(
                    x=medias_avaliacoes.index,
                    y=medias_avaliacoes.values,
                    labels={'x': 'Aspecto', 'y': 'Média da Avaliação'},
                    title='Média das Avaliações'
                )
                st.plotly_chart(grafico_avaliacoes)
    
                # Gráfico de pizza para Natureza do Desligamento
                st.subheader("Distribuição por Natureza do Desligamento")
                grafico_natureza = px.pie(
                    dados_filtrados,
                    names='natureza',
                    title='Natureza do Desligamento'
                )
                st.plotly_chart(grafico_natureza)
    
                # Gráfico de pizza para Gênero
                if 'genero' in dados_filtrados.columns:
                    grafico_genero = px.pie(
                        dados_filtrados.groupby('genero').size().reset_index(name='count'),
                        names='genero',
                        values='count',
                        title='Distribuição por Gênero'
                    )
                    st.plotly_chart(grafico_genero)
                else:
                    st.write("Nenhuma resposta disponível para o gráfico de Gênero.")
    
                # Gráfico de barras para Setor
                grafico_setor = px.bar(dados_filtrados.groupby('setor').size().reset_index(name='count'),
                                       x='setor',
                                       y='count',
                                       title='Distribuição por Setor')
                st.plotly_chart(grafico_setor)
    
            
            
    with st.sidebar:
          st.markdown(
              "## Como Usar:\n"
              "1. Vá respondendo as perguntas📄\n"
              "2. Salve! As perguntas serão salvas no Banco de dados que poderá ser consultada mais tarde💬\n"
          )
          st.markdown("---")
          st.markdown("# Sobre")
          with st.expander("Eng. IA 📖"):
              st.markdown("Matheus Cabral\n\n"
                      "+55 54 999307783. ")
