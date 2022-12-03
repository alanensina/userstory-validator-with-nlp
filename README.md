# User Story Validator With NLP
# _English_
<p> This work was developed as my final work at UFSC to receive the Bachelor of Information Systems degree.

## _Requirements_
- python 3.10+
- pip 22.2+
- Microsoft Visual C++ (apenas no Windows)

## _Description_
<p> This API is in charge to evaluate user stories written using Mike Cohn's template and Gherkin's template. Stories are evaluated with three syntactic quality criteria:
<p> Well formed: A story is well formed when there is an actor and an action. Purpose is optional.
<p> Atomic: A story is atomic when there is only one action being performed.
<p> Minimal: A story is minimal when it is well-formed and has no extra information, i.e. notes and additional information.

## _Preparation of sentences_
<p> A user story is a short, semi-structured sentence capable of illustrating the requirements of a software from the user's perspective, that is, it can be used to identify the user's desire for the product. Mike Cohn suggested the following template for writing a user story:
<p> "As a [user type], I want [some purpose] so [some reason]."
<p>
<p> This application is capable of processing stories following the Cohn template and also the Gherkin template:
<p> "Given [precondition], when [action to be performed] then [expected result]".
<p>
<p> To be possible, it is necessary to adapt the stories through keywords so that it is possible to segment the phrase. Therefore, follow the templates suggested below:
<p> "I as [user type], I would like [some purpose] so [some reason]."
<p> "Given [precondition], when [action to be performed] then [expected result]".
<p>

## _How to run the application_
<p> With python and pip installed, install virtualenv:

```bash
pip install virtualenv
```

<p> After installing virtualenv, access the project directory and create the virtual environment:

```bash
virtualenv venv
```

<p> Activate the virtualenv:

```bash
source venv/bin/activate (Linux or macOS)
venv/Scripts/Activate (Windows)
```

<p> Once activated, install the dependencies:

```bash
pip install -r requirements.txt
```

<p> Finally, launch the application:

```bash
python app.py
```

## _Executing the evaluation_
<p> After starting the application, go to:

```bash
localhost:5000/analisador
```

<p> The endpoint /historia uses user stories in the Cohn's template, while the /cenario uses the Gherkin's template. Use the JSON files available in the examples folder to test and use as an example to create your own user stories.

# _Português_
<p> Este trabalho foi desenvolvido como meu trabalho de conclusão de curso na UFSC para receber o título de Bacharel em Sistemas de Informação.

## _Requisitos_
- python 3.10+
- pip 22.2+
- Microsoft Visual C++ (apenas no Windows)

## _Descrição_
<p> Esta API tem como o objetivo avaliar histórias de usuário escritas utilizando o template de Mike Cohn e o template de Gherkin. As histórias são avaliadas dentro de três critérios de qualidade sintáticos:
<p> Bem formada: uma história é bem formada quando há um ator e uma ação. A finalidade é opcional.
<p> Atômica: uma história é atômica quando há apenas uma ação sendo executada.
<p> Mínima: uma história é mínima quando é bem formada e não tem informações extras, ou seja, notas e informações adicionais.

## _Preparação das frases_
<p> Uma  história de usuário é frase curta e semi-estruturada capaz de ilustrar os requisitos de um software na perspectiva do usuário, ou seja, pode ser usada para identificar o desejo do usuário com relação ao produto. Mike Cohn sugeriu o seguinte template para escrever uma história de usuário:
<p> "Como [tipo de usuário], quero [algum objetivo] para que [algum motivo]."
<p>
<p> Esta aplicação é capaz de processar histórias seguindo o template de Cohn e também o template de Gherkin:
<p> "Dado [pré-condição], quando [ação que será executada] então [resultado esperado]".
<p>
<p> Mas para que isso seja possível, é necessário adequar as histórias através de palavras chave para que seja possível segmentar a frase. Sendo assim, segue os templates sugerido logo abaixo:
<p> "Eu como [tipo de usuário], gostaria [algum objetivo] para que [algum motivo]."
<p> "Dado [pré-condição], quando [ação que será executada] então [resultado esperado]".
<p>

## _Como rodar a aplicação_
<p> Com o python e o pip instalado, instale o virtualenv:

```bash
pip install virtualenv
```

<p> Após instalado o virtualenv, acesse o diretório do projeto e crie o ambiente virtual:

```bash
virtualenv venv
```

<p> Ative a virtualenv:

```bash
source venv/bin/activate (Linux ou macOS)
venv/Scripts/Activate (Windows)
```

<p> Após ativado, instale as dependências:

```bash
pip install -r requirements.txt
```

<p> Por fim, inicie a aplicação:

```bash
python app.py
```

## _Executando a avaliação_
<p> Após iniciado a aplicação acesse:

```bash
localhost:5000/analisador
```

<p> O endpoint /historia utiliza histórias de usuário no template de Cohn, já o /cenario utiliza ao template de Gherkin. Utilize os arquivos JSON disponíveis na pasta de exemplos para testar e tomar como exemplo para criar suas próprias histórias de usuário.
