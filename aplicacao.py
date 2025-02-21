# Importação das bibliotecas necessárias

import streamlit as st  # Para criar a interface do usuário
import numpy as np  # Para funções matemáticas numéricas e operações com arrays
import matplotlib.pyplot as plt  # Para gerar gráficos
from matplotlib.patches import Rectangle  # Para desenhar retângulos nos gráficos
from sympy import sympify, lambdify, integrate, symbols, Rational  # Para manipulação simbólica e integração
import sympy as sp

# Definindo a variável simbólica 'x' para usar em expressões matemáticas
x = symbols('x')
f_expr = x**2  # Altere a função aqui, se desejar
f = sp.lambdify(x, f_expr, 'numpy')  # Converte para função numérica
df_expr = sp.diff(f_expr, x)  # Derivada simbólica
df = sp.lambdify(x, df_expr, 'numpy')  # Converte para função numérica


# Configuração do estado da interface utilizando a sessão do Streamlit
if 'selected_tool' not in st.session_state:
    st.session_state.selected_tool = None  # Nenhuma ferramenta selecionada inicialmente

# Título da aplicação na interface
st.title('Calculadora Matemática')

# Criação de botões para seleção da ferramenta que o usuário deseja usar
col1, col2, col3 = st.columns(3)  # Organiza os botões em colunas
with col1:
    if st.button("Integrar"):  # Botão de integração
        st.session_state.selected_tool = "Integrar"  # Seleciona a ferramenta de integrar
with col2:
    if st.button("Derivar"):  # Botão de derivada
        st.session_state.selected_tool = "Derivar"  # Seleciona a ferramenta de derivar
with col3:
    if st.button("Limites"):  # Botão de funcionalidade "Limites"
        st.session_state.selected_tool = "Limites"  # Seleciona a ferramenta "Limites"

# Adicionando mais botões para futuras funcionalidades
col4, col5, col6 = st.columns(3)
with col4:
    if st.button("Em Breve 2"):
        st.session_state.selected_tool = "Em Breve"
with col5:
    if st.button("Em Breve 3"):
        st.session_state.selected_tool = "Em Breve"
with col6:
    if st.button("Em Breve 4"):
        st.session_state.selected_tool = "Em Breve"

# Verifica qual ferramenta foi selecionada e executa as ações correspondentes

#======================================================================================================================

#INTEGRAR

if st.session_state.selected_tool == "Integrar":  # Quando a ferramenta de integração for selecionada
    st.subheader('Aproximação da Integral com Retângulos')  # Subtítulo para a seção de integração

    # Entrada do usuário para a função a ser integrada
    user_input = st.text_input('Digite uma função f(x):', 'x^2')  # Pede ao usuário a função (exemplo: x^2)

    try:
        # Converte a entrada do usuário para uma expressão simbólica
        func_sympy = sympify(user_input)
        func = lambdify('x', func_sympy, 'numpy')  # Transforma a função simbólica em função numérica para cálculos

        # Limites da integral fornecidos pelo usuário
        a = st.number_input('Limite inferior (a):', value=0)  # Limite inferior
        b = st.number_input('Limite superior (b):', value=5)  # Limite superior

        # Inicializa a configuração para mostrar ou não o gráfico
        if 'show_graph' not in st.session_state:
            st.session_state.show_graph = False

        # Inicializa o número de retângulos para a aproximação
        if 'n_rects' not in st.session_state:
            st.session_state.n_rects = 0

        # Botão para calcular a integral
        if st.button('Calcular a Integral'):
            st.session_state.show_graph = True  # Ativa a exibição do gráfico

        if st.session_state.show_graph:
            # Slider para o número de retângulos na aproximação
            n = st.slider('Número de retângulos (0 a 100):', 0, 100, st.session_state.n_rects)
            st.session_state.n_rects = n

            # Função para plotar a função e os retângulos
            def plot_function_and_rectangles(func, a, b, n):
                x_vals = np.linspace(a, b, 500)  # Gera os valores de x entre a e b
                y_vals = func(x_vals)  # Calcula os valores de y para a função

                fig, ax = plt.subplots(1, 2, figsize=(14, 6))  # Cria uma figura com 2 subgráficos

                # Gráfico da função
                ax[0].plot(x_vals, y_vals, label='Função', color='blue')
                ax[0].fill_between(x_vals, y_vals, color='skyblue', alpha=0.5)
                ax[0].set_title('Função e a área sob ela')
                ax[0].set_xlabel('x')
                ax[0].set_ylabel('f(x)')
                ax[0].grid(True)
                ax[0].legend()

                # Gráfico da aproximação com retângulos
                if n > 0:
                    dx = (b - a) / n  # Largura de cada retângulo
                    for i in range(n):
                        x0 = a + i * dx  # Posição inicial do retângulo
                        x_mid = x0 + dx / 2  # Ponto médio do retângulo
                        y0 = func(x_mid)  # Avaliação da função no ponto médio
                        ax[1].add_patch(Rectangle((x0, 0), dx, y0, linewidth=1, edgecolor='black', facecolor='orange', alpha=0.6))

                ax[1].plot(x_vals, y_vals, label='Função', color='blue')
                ax[1].set_xlim(a, b)
                ax[1].set_ylim(0, np.max(y_vals) + 1)
                ax[1].set_title(f'Aproximação da Integral com {n} retângulos')
                ax[1].set_xlabel('x')
                ax[1].set_ylabel('f(x)')
                ax[1].grid(True)

                plt.tight_layout()  # Ajusta o layout para não sobrepor os gráficos
                return fig

            # Função para calcular a integral aproximada utilizando os retângulos
            def approximate_integral(func, a, b, n):
                if n == 0:
                    return 0
                dx = (b - a) / n  # Largura de cada retângulo
                x_vals = np.linspace(a + dx / 2, b - dx / 2, n)  # Posição dos retângulos
                y_vals = func(x_vals)  # Avaliação da função nos pontos dos retângulos
                area = np.sum(y_vals * dx)  # Soma das áreas dos retângulos
                return area

            fig = plot_function_and_rectangles(func, a, b, n)  # Gera o gráfico com retângulos
            st.pyplot(fig)  # Exibe o gráfico na interface

            area = approximate_integral(func, a, b, n)  # Calcula a área aproximada
            st.write(f'A área aproximada sob a curva é: {area:.4f}')  # Exibe a área calculada

            # Cálculo da integral exata
            integral_exact = integrate(func_sympy, (x, a, b))  
            st.write(f'O valor exato da integral é: {integral_exact.evalf()}')  # Exibe o valor exato

            if isinstance(integral_exact, Rational):  # Se o valor exato for uma fração
                st.write(f'A forma fracionária da integral é: {integral_exact}')
            else:
                st.write(f'A integral não possui uma forma fracionária exata.')

        # Botão de SOLUÇÃO para exibir explicação passo a passo da integral
        if st.button('SOLUÇÃO'):
            st.subheader('Explicação passo a passo:')
            st.write('**Passo 1: Definição da integral**')
            st.write(f'Queremos calcular a integral definida de f(x) = {user_input} no intervalo de {a} a {b}. A integral definida é dada por:')
            st.latex(r'\int_{a}^{b} f(x) \, dx')

            st.write('**Passo 2: Simplificação da função**')
            st.write(f'A função não necessita de simplificação. Ela é: {user_input}.')
            st.write('A função que vamos integrar é: ' + user_input)

            st.write('**Passo 3: Cálculo da integral indefinida**')
            st.write(f'Agora, vamos calcular a integral indefinida de f(x). A regra de integração que usamos aqui é a regra de potências, que diz o seguinte:')
            st.latex(r'\int x^n \, dx = \frac{x^{n+1}}{n+1} + C')

            # Cálculo da integral indefinida
            integral_indefinida = integrate(func_sympy, x)
            st.write(f'A integral indefinida de f(x) = {user_input} é:')
            st.latex(r'\int f(x) \, dx = ' + str(integral_indefinida))

            # Passo 4: Substituição dos limites de integração
            st.write('**Passo 4: Substituição dos limites**')
            st.write('Agora, aplicamos o Teorema Fundamental do Cálculo para substituir os limites de integração (a e b).')

            # Cálculo dos valores F(b) e F(a)
            F_b = integral_indefinida.subs(x, b)
            F_a = integral_indefinida.subs(x, a)

            # Exibição da substituição
            st.write(f'Primeiro, substituímos os limites na integral indefinida:')
            st.latex(f'F(b) = {str(F_b)}')
            st.latex(f'F(a) = {str(F_a)}')

            # Cálculo da diferença para obter a área exata
            area_exata = F_b - F_a
            st.write(f'A área exata sob a curva é dada pela diferença F(b) - F(a):')
            st.latex(f'Área = F(b) - F(a) = {str(F_b)} - {str(F_a)} = {str(area_exata)}')

            # Exibe o valor da área exata
            st.write(f'O valor exato da integral calculado é: {area_exata.evalf()}')

    except Exception as e:
        st.error(f'Ocorreu um erro ao processar a função. Verifique a sintaxe da função inserida. Erro: {str(e)}')

#======================================================================================================================

#======================================================================================================================

#DERIVADA


# Caso a ferramenta de Derivada seja selecionada
elif st.session_state.selected_tool == "Derivar":
    st.subheader("Calculadora de Derivadas")

 # Campo para inserir a função
    func_str = st.text_input("Digite a função f(x):", "x**2")

    # Definir x como símbolo e converter a string da função para expressão simbólica
    x = sp.Symbol('x')
    try:
        f_expr = sp.sympify(func_str)  # Converte a string para uma expressão simbólica
        f = sp.lambdify(x, f_expr, 'numpy')  # Converte para função numérica
        df_expr = sp.diff(f_expr, x)  # Derivada simbólica
        df_expr_simplified = sp.simplify(df_expr)  # Simplifica a derivada
        df = sp.lambdify(x, df_expr, 'numpy')  # Converte para função numérica
    except:
        st.error("Função inválida! Tente novamente.")
        st.stop()

# Mostrar a derivada simbólica da função
    st.write(f"A derivada da função f(x) = {func_str} é f'(x) = {df_expr_simplified}")

    # Slider para selecionar o ponto x0
    x0 = st.slider("Escolha o ponto x:", -5.0, 5.0, 0.0, step=0.1)

    # Calcula f(x0) e f'(x0)
    f_x0 = f(x0)
    df_x0 = df(x0)

    # Define o intervalo para o gráfico
    x_vals = np.linspace(-5, 5, 400)
    y_vals = f(x_vals)
    df_vals = df(x_vals)

    # Equação da reta tangente: y = f'(x0) * (x - x0) + f(x0)
    tangent_line = df_x0 * (x_vals - x0) + f_x0

    # Criando o gráfico
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label="f(x)", color='blue')
    ax.plot(x_vals, df_vals, label="f'(x)", color='green', linestyle='dashed')
    ax.plot(x_vals, tangent_line, label="Reta Tangente", color='red', linestyle='dotted')

    # Destacando o ponto de tangência
    ax.scatter([x0], [f_x0], color='black', zorder=3, label="Ponto de Tangência")

    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    # Mostrando os valores de f(x0) e f'(x0)
    st.write(f"**Valor da função no ponto {x0}:** f({x0}) = {f_x0:.4f}")
    st.write(f"**Valor da derivada no ponto {x0}:** f'({x0}) = {df_x0:.4f}")

#======================================================================================================================

#LIMITES

# Caso a ferramenta "Limites" seja selecionada
elif st.session_state.selected_tool == "Limites":
    st.subheader("Limites")

    # Campo para inserir a função
    func_str = st.text_input("Digite a função f(x):", "(1 - cos(x))/(2*sin(x)**2)")  # exemplo: (1 - cos(x))/(2*sin(x)**2)

    # Definir x como símbolo e converter a string da função para expressão simbólica
    x = sp.Symbol('x')

    try:
        f_expr = sp.sympify(func_str)  # Converte a string para uma expressão simbólica
    except:
        st.error("Função inválida! Tente novamente.")
        st.stop()

    # Campo para escolher o ponto de limite
    limite_tipo = st.selectbox("Escolha o tipo de limite:", ["Limite Finito", "Limite no Infinito"])

    if limite_tipo == "Limite Finito":
        # Slider para selecionar o ponto x0
        x0 = st.slider("Escolha o ponto x0:", -5.0, 5.0, 0.0, step=0.1)

        # Calcular o limite
        try:
            limite = sp.limit(f_expr, x, x0)
        except Exception as e:
            st.error(f"Erro ao calcular o limite: {e}")
            st.stop()

        # Exibir o resultado
        st.write(f"O limite de f(x) quando x tende a {x0} é: {limite}")

        # Gerar o gráfico
        x_vals = np.linspace(-5, 5, 400)
        y_vals = []

        for val in x_vals:
            try:
                y_value = f_expr.subs(x, val)
                # Verificar se o valor é infinito ou indeterminado
                if y_value == sp.oo or y_value == -sp.oo or np.isnan(float(y_value)):
                    y_vals.append(np.nan)  # Usar NaN para valores infinitos
                else:
                    y_vals.append(float(y_value))
            except:
                y_vals.append(np.nan)  # Caso o valor não seja válido, adicionar NaN

        # Criar o gráfico
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label="f(x)", color='blue')

        # Escurecer os eixos
        ax.axhline(0, color='black', linewidth=2)  # Eixo X mais escuro
        ax.axvline(0, color='black', linewidth=2)  # Eixo Y mais escuro

        # Destacar o ponto de limite, se possível
        limite_y = float(f_expr.subs(x, x0))  # Valor da função no ponto x0
        ax.scatter([x0], [limite_y], color='red', zorder=5, label=f'Limite em x = {x0}')

        # Adicionar linha conectando o ponto ao eixo x
        ax.plot([x0, x0], [limite_y, 0], color='red', linestyle='--', label=f'x')
        
        # Linha conectando o ponto de limite ao eixo Y
        ax.plot([0, x0], [limite_y, limite_y], color='green', linestyle='--', label=f'y')

        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

    elif limite_tipo == "Limite no Infinito":
        # Opções para limites em +∞ ou -∞
        infinito_tipo = st.selectbox("Escolha o infinito:", ["+∞", "-∞"])

        if infinito_tipo == "+∞":
            # Calcular o limite quando x tende a +∞
            limite = sp.limit(f_expr, x, sp.oo)
        else:
            # Calcular o limite quando x tende a -∞
            limite = sp.limit(f_expr, x, -sp.oo)

        # Exibir o resultado
        st.write(f"O limite de f(x) quando x tende a {infinito_tipo} é: {limite}")

        # Gerar o gráfico para limites no infinito
        x_vals = np.linspace(-5, 5, 400)
        y_vals = []

        for val in x_vals:
            try:
                y_value = f_expr.subs(x, val)
                if y_value == sp.oo or y_value == -sp.oo or np.isnan(float(y_value)):
                    y_vals.append(np.nan)  # Usar NaN para valores infinitos
                else:
                    y_vals.append(float(y_value))
            except:
                y_vals.append(np.nan)  # Caso o valor não seja válido, adicionar NaN

        # Criar o gráfico
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label="f(x)", color='blue')

        # Linha horizontal mostrando o valor de y no limite assintótico
        if limite != sp.oo and limite != -sp.oo:
            ax.axhline(y=float(limite), color='green', linestyle='dashed', label=f'Limite: {limite}')

        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)



#======================================================================================================================

#EM BREVE

# Caso a ferramenta "Em Breve" seja selecionada
elif st.session_state.selected_tool == "Em Breve":
    st.warning("Esta ferramenta estará disponível em breve!")

#======================================================================================================================



# Adicionar a marca de copyright no final
st.markdown("<br><hr><p style='text-align: center;'>© 2025 Lucas Matias. Todos os direitos reservados.</p>", unsafe_allow_html=True)

#arrumando tudo