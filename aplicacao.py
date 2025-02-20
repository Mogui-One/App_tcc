import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from sympy import sympify, lambdify, integrate, symbols, Rational, sqrt, sin, cos

# Definir a variável simbólica
x = symbols('x')

# Função para gerar gráfico da função e os retângulos
def plot_function_and_rectangles(func, a, b, n):
    x_vals = np.linspace(a, b, 500)
    y_vals = func(x_vals)

    fig, ax = plt.subplots(1, 2, figsize=(14, 6))

    # Gráfico da função
    ax[0].plot(x_vals, y_vals, label='Função', color='blue')
    ax[0].fill_between(x_vals, y_vals, color='skyblue', alpha=0.5)
    ax[0].set_title('Função e a área sob ela')
    ax[0].set_xlabel('x')
    ax[0].set_ylabel('f(x)')
    ax[0].grid(True)
    ax[0].legend()

    # Gráfico dos retângulos
    if n > 0:
        dx = (b - a) / n
        for i in range(n):
            x0 = a + i * dx  # Base do retângulo
            x_mid = x0 + dx / 2  # Ponto médio do retângulo
            y0 = func(x_mid)  # Avaliação da função no ponto médio
            ax[1].add_patch(Rectangle((x0, 0), dx, y0, linewidth=1, edgecolor='black', facecolor='orange', alpha=0.6))

    # Mostrando a função no gráfico de aproximação
    ax[1].plot(x_vals, y_vals, label='Função', color='blue')
    ax[1].set_xlim(a, b)
    ax[1].set_ylim(0, np.max(y_vals) + 1)
    ax[1].set_title(f'Aproximação da Integral com {n} retângulos')
    ax[1].set_xlabel('x')
    ax[1].set_ylabel('f(x)')
    ax[1].grid(True)

    plt.tight_layout()
    return fig

# Função para calcular a aproximação da integral com n retângulos
def approximate_integral(func, a, b, n):
    if n == 0:
        return 0
    dx = (b - a) / n
    x_vals = np.linspace(a + dx / 2, b - dx / 2, n)  # Ponto médio de cada subintervalo
    y_vals = func(x_vals)
    area = np.sum(y_vals * dx)
    return area

# Título e explicação inicial
st.title('Aproximação da Integral com Retângulos')
st.write('Digite uma função para visualizar e calcular sua área sob a curva usando retângulos.')

# Entrada da função
user_input = st.text_input('Digite uma função f(x):', 'x^2')

try:
    # Converter a entrada do usuário em uma função matemática
    func_sympy = sympify(user_input)
    func = lambdify('x', func_sympy, 'numpy')
    
    # Intervalo de integração
    a = st.number_input('Limite inferior (a):', value=0)
    b = st.number_input('Limite superior (b):', value=5)

    # Variável para controlar a exibição do gráfico
    if 'show_graph' not in st.session_state:
        st.session_state.show_graph = False

    if 'n_rects' not in st.session_state:
        st.session_state.n_rects = 0

    # Botão de solução
    if st.button('Calcular a Integral'):
        st.session_state.show_graph = True  # Habilitar a exibição do gráfico quando o botão for clicado
        
    if st.session_state.show_graph:
        # Habilitar controle deslizante para número de retângulos
        n = st.slider('Número de retângulos (0 a 100):', 0, 100, st.session_state.n_rects)
        st.session_state.n_rects = n  # Armazenar o número de retângulos no estado da sessão

        # Gerando gráfico com o número de retângulos ajustado
        fig = plot_function_and_rectangles(func, a, b, n)
        st.pyplot(fig)
        
        # Calculando a área aproximada
        area = approximate_integral(func, a, b, n)
        st.write(f'A área aproximada sob a curva é: {area:.4f}')
        
        # Cálculo da integral exata
        integral_exact = integrate(func_sympy, (x, a, b))
        st.write(f'O valor exato da integral é: {integral_exact.evalf()}')

        # Exibindo a forma fracionária
        if isinstance(integral_exact, Rational):
            st.write(f'A forma fracionária da integral é: {integral_exact}')
        else:
            st.write(f'A integral não possui uma forma fracionária exata.')

        # Botão SOLUÇÃO para exibir explicação passo a passo
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

            # Passo 4: Substituição dos limites
            st.write('**Passo 4: Substituição dos limites**')
            st.write('Agora, aplicamos o Teorema Fundamental do Cálculo para substituir os limites de integração (a e b).')

            # Calcular os valores de F(b) e F(a)
            F_b = integral_indefinida.subs(x, b)
            F_a = integral_indefinida.subs(x, a)

            # Mostrar a substituição
            st.write(f'Primeiro, substituímos os limites na integral indefinida:')
            st.latex(f'F(b) = {str(F_b)}')
            st.latex(f'F(a) = {str(F_a)}')

            # Calcular a diferença para encontrar a área exata
            area_exata = F_b - F_a
            st.write(f'A área exata sob a curva é dada pela diferença F(b) - F(a):')
            st.latex(f'Área = F(b) - F(a) = {str(F_b)} - {str(F_a)} = {str(area_exata)}')

            # Exibir o valor da área exata
            st.write(f'O valor exato da integral calculado é: {area_exata.evalf()}')

except Exception as e:
    st.error(f'Ocorreu um erro ao processar a função. Verifique a sintaxe da função inserida. Erro: {str(e)}')
