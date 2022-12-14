# User Story Validator With NLP
# _English_
<p> This work was developed as my final work at UFSC to receive the Bachelor of Information Systems degree.

## _Requirements_
- python 3.10+
- pip 22.2+
- Microsoft Visual C++ (only Windows)

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

# _Portugu??s_
<p> Este trabalho foi desenvolvido como meu trabalho de conclus??o de curso na UFSC para receber o t??tulo de Bacharel em Sistemas de Informa????o.

## _Requisitos_
- python 3.10+
- pip 22.2+
- Microsoft Visual C++ (apenas no Windows)

## _Descri????o_
<p> Esta API tem como o objetivo avaliar hist??rias de usu??rio escritas utilizando o template de Mike Cohn e o template de Gherkin. As hist??rias s??o avaliadas dentro de tr??s crit??rios de qualidade sint??ticos:
<p> Bem formada: uma hist??ria ?? bem formada quando h?? um ator e uma a????o. A finalidade ?? opcional.
<p> At??mica: uma hist??ria ?? at??mica quando h?? apenas uma a????o sendo executada.
<p> M??nima: uma hist??ria ?? m??nima quando ?? bem formada e n??o tem informa????es extras, ou seja, notas e informa????es adicionais.

## _Prepara????o das frases_
<p> Uma  hist??ria de usu??rio ?? frase curta e semi-estruturada capaz de ilustrar os requisitos de um software na perspectiva do usu??rio, ou seja, pode ser usada para identificar o desejo do usu??rio com rela????o ao produto. Mike Cohn sugeriu o seguinte template para escrever uma hist??ria de usu??rio:
<p> "Como [tipo de usu??rio], quero [algum objetivo] para que [algum motivo]."
<p>
<p> Esta aplica????o ?? capaz de processar hist??rias seguindo o template de Cohn e tamb??m o template de Gherkin:
<p> "Dado [pr??-condi????o], quando [a????o que ser?? executada] ent??o [resultado esperado]".
<p>
<p> Mas para que isso seja poss??vel, ?? necess??rio adequar as hist??rias atrav??s de palavras chave para que seja poss??vel segmentar a frase. Sendo assim, segue os templates sugerido logo abaixo:
<p> "Eu como [tipo de usu??rio], gostaria [algum objetivo] para que [algum motivo]."
<p> "Dado [pr??-condi????o], quando [a????o que ser?? executada] ent??o [resultado esperado]".
<p>

## _Como rodar a aplica????o_
<p> Com o python e o pip instalado, instale o virtualenv:

```bash
pip install virtualenv
```

<p> Ap??s instalado o virtualenv, acesse o diret??rio do projeto e crie o ambiente virtual:

```bash
virtualenv venv
```

<p> Ative a virtualenv:

```bash
source venv/bin/activate (Linux ou macOS)
venv/Scripts/Activate (Windows)
```

<p> Ap??s ativado, instale as depend??ncias:

```bash
pip install -r requirements.txt
```

<p> Por fim, inicie a aplica????o:

```bash
python app.py
```

## _Executando a avalia????o_
<p> Ap??s iniciado a aplica????o acesse:

```bash
localhost:5000/analisador
```

<p> O endpoint /historia utiliza hist??rias de usu??rio no template de Cohn, j?? o /cenario utiliza ao template de Gherkin. Utilize os arquivos JSON dispon??veis na pasta de exemplos para testar e tomar como exemplo para criar suas pr??prias hist??rias de usu??rio.
